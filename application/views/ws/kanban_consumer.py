from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from modules.kanban import service as kanban_sv


# JSONをクライアントとやり取りするのであればJsonWebsocketConsumerを継承
class KanbanConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        """
        Consumerに独自の属性(consumer_id, user)を
        もたせるためにオーバライド
        """
        super().__init__(*args, **kwargs)
        # 自身に一意なIDを付与する
        self.consumer_id = id(self)
        self.user = None
        self.board_id = None
        self.namespace = 'board'
        # self.action_mapにどのメッセージが来たら
        # どのメソッドを呼び出すかの対応を定義
        self.action_map = {
            'update_card_order': self.update_card_order,
            'broadcast_board_data': self.broadcast_board_data,
            'add_pipe_line': self.add_pipe_line,
            'rename_pipe_line': self.rename_pipe_line,
            'delete_pipe_line': self.delete_pipe_line,
        }
        self.room_group_name = None

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
        # channel layerの初期化
        self.room_group_name = 'board_id_{}'.format(self.board_id)
        # ボード毎のグループに参加
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # 初期データをクライアントに返送
        self.send_board_data()

    def send_board_data(self, event=None, *args, **kwargs):
        """
        取得したボードの構成情報をクライアントに返す
        connect内で呼び出す
        """
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
        # 同じroom_group_nameに所属しているConsumerすべてにsend_board_dataを呼び出させる
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_board_data',
            }
        )

    def add_pipe_line(self, content):
        """
        パイプラインの追加
        """
        board_id = content['boardId']
        pipe_line_name = content['pipeLineName']
        kanban_sv.add_pipe_line(board_id, pipe_line_name)
        self.broadcast_board_data()

    def rename_pipe_line(self, content):
        """
        パイプライン名の変更
        """
        pipe_line_id = content['pipeLineId']
        pipe_line_name = content['pipeLineName']
        kanban_sv.update_pipe_line(pipe_line_id, pipe_line_name)
        self.broadcast_board_data()

    def delete_pipe_line(self, content):
        """
        パイプラインの削除
        :param content:
        :return:
        """
        board_id = content['boardId']
        pipe_line_id = content['pipeLineId']
        kanban_sv.delete_pipe_line(pipe_line_id)
        self.broadcast_board_data()

    def receive_json(self, content, **kwargs):
        """
        メッセージ内のtypeに該当するものを直接呼び出し
        未定義のtypeを受け取った場合は例外を送出
        :param dict content:
        :param kwargs:
        :return:
        """
        action = self.action_map.get(content['type'])
        if not action:
            raise Exception('{} is not a valid action_type'.format(content['type']))
        action(content)

    def broadcast_board_data(self, content=None):
        """
        このメソッドを呼び出してメッセージをサーバ側に送信することで
        同じボードを開いている全クライアントのデータが更新できる
        :param content:
        :return:
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_board_data',
            }
        )
