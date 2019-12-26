from channels.generic.websocket import JsonWebsocketConsumer

from modules.kanban import service as kanban_sv


# JSONをクライアントとやり取りするのであればJsonWebsocketConsumerを継承
class KanbanConsumer(JsonWebsocketConsumer):

    # Consumerに独自の属性(consumer_id, user)を
    # もたせるために今回はオーバライド
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自身に一意なIDを付与する
        self.consumer_id = id(self)
        self.user = None
        self.board_id = None
        self.namespace = 'board'
        # self.action_mapにどのメッセージが来たら
        # どのメソッドを呼び出すかの対応を定義
        self.action_map = {
            'update_card_order': self.update_card_order
        }

    def connect(self):
        # 認証チェック
        if not self.scope['user'].is_authenticated:
            self.close()
            return

        self.user = self.scope['user']
        # URLに含まれているBoardのIDを取得
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        # 接続を受け入れる
        self.accept()
        # 初期データをクライアントに返送
        self.send_board_data()

    # 取得したボードの構成情報をクライアントに戻すメソッド
    # connect内で呼び出す
    def send_board_data(self):
        board_data = kanban_sv.get_board_data_by_board_id(self.board_id)
        # VueNativeWebsocketではmutation: xxxや
        # action: xxx というデータが含まれたメッセージがWebsocketに来た場合
        # 対応するmutationやactionを呼び出してくれる機能がある
        self.send_json({
            'boardData': board_data,
            'mutation': 'setBoardData',
            'namespace': self.namespace,
        })
        print(board_data)

    def update_card_order(self, content):
        """
        ボード内のカードの並び順を更新する
        {
            'type': 'update_card_order',
            'pipeLineId': 1,
            'cardIdList': [3, 1]
        }
        :return:
        """
        pipe_line_id = content['pipeLineId']
        card_id_list = content['cardIdList']
        kanban_sv.update_card_order(pipe_line_id, card_id_list)
        self.send_board_data()

    # メッセージ内のtypeに該当するものを直接呼び出し
    # 未定義のtypeを受け取った場合は例外を送出
    def receive_json(self, content, **kwargs):
        """
        Typeに応じた処理を呼び出して実行する
        :param dict content:
        :param kwargs:
        :return:
        """
        action = self.action_map.get(content['type'])
        if not action:
            raise Exception('{} is not a valid action_type'.format(content['type']))
        action(content)
