from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .service import service


class ConsumerException(Exception):
    """
    consumer内での例外
    """


class BaseJsonConsumer(AsyncJsonWebsocketConsumer):
    namespace = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer_id = id(self)
        self.user = None
        self.room_group_name = None
        self.action_map = {}

    async def send_data(self, content, mutation=None, action=None, namespace=None):
        """
        VueNativeWebSocket用にnamespace等を追加して送信する

        mutation かactionは何れか一方を指定する
        :param dict or list content:
        :param str mutation:
        :param str action:
        :param str namespace:
        :return:
        """
        namespace = self.namespace if namespace is None else namespace
        send_data = {
            'namespace': namespace
        }
        if mutation and action:
            raise ConsumerException('mutation and action is only one.')

        if (not mutation) and (not action):
            raise ConsumerException('mutation or action must be set.')

        if mutation:
            send_data['mutation'] = mutation
        if action:
            send_data['action'] = action
        if not isinstance(content, dict):
            content = {
                'data': content,
            }
        content.update(send_data)
        await self.send_json(content)

    async def receive_json(self, content, **kwargs):
        """
        Typeに応じた処理を呼び出して実行する
        :param dict content:
        :param kwargs:
        :return:
        """
        action = self.action_map.get(content['type'])
        if not action:
            raise ConsumerException('{} is not a valid action_type'.format(content['type']))
        await action(content)

    async def group_add(self, group_name, channel_name):
        """
        channel_layerと毎回書くのが面倒なので。。。
        """
        await self.channel_layer.group_add(
            group_name,
            channel_name
        )

    async def group_send(self, group_name, body):
        """
        channel_layerと毎回書くのが面倒なので。。。
        """
        await self.channel_layer.group_send(
            group_name,
            body
        )


class KanbanConsumer(BaseJsonConsumer):

    # VueNativeWebSocket経由でStoreにマップするための情報
    namespace = 'board'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board_id = None
        self.action_map = {
            'update_card_order': self.update_card_order,
            'update_pipe_line_order': self.update_pipe_line_order,
            'add_pipe_line': self.add_pipe_line,
            'add_card': self.add_card,
            'rename_pipe_line': self.rename_pipe_line,
            'delete_pipe_line': self.delete_pipe_line,
            'delete_board': self.delete_board,
            'rename_board': self.rename_board,
            'broadcast_board_data': self.broadcast_board_data,
            'broadcast_board_data_without_requester': self.broadcast_board_data_without_requester,
        }

    async def connect(self):
        """
        接続時の処理
        :return:
        """
        # 認証チェック
        if not self.scope['user'].is_authenticated:
            await self.close()
            return
        self.user = self.scope['user']
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        self.room_group_name = self.user.username
        # ボード毎のグループに参加
        await self.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        # ボードがあれば初期データを返送
        if await database_sync_to_async(service.is_board_exist)(self.board_id):
            await self.send_board_data({})
        else:
            # 存在しないボードだった場合は、クライアントにリダイレクトを指示
            await self.send_back_to_home()

    async def send_board_data(self, event):
        """
        ボードのデータを送る
        :return:
        """
        # requester_idが指定されている場合には、自身と一致した場合は返送しない
        if event.get('requester_id') == self.consumer_id:
            return
        board_data = await database_sync_to_async(service.get_board_data_board_id)(self.board_id)
        await self.send_data({
            'boardData': board_data,
        }, mutation='setBoardData')

    async def update_card_order(self, content):
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
        await database_sync_to_async(service.update_card_order)(pipe_line_id, card_id_list)
        await self.broadcast_board_data_without_requester()

    async def update_pipe_line_order(self, content):
        """
        パイプラインの並びを変更する
        {
            'type': 'update_pipe_line_order',
            'boardId': 1,
            'pipeLineIdList': [2, 1]
        }
        """
        board_id = content['boardId']
        pipe_line_id_list = content['pipeLineIdList']
        await database_sync_to_async(service.update_pipe_line_order)(board_id, pipe_line_id_list)
        await self.broadcast_board_data_without_requester()

    async def add_pipe_line(self, content):
        """
        パイプラインの追加
        """
        board_id = content['boardId']
        pipe_line_name = content['pipeLineName']
        await database_sync_to_async(service.add_pipe_line)(board_id, pipe_line_name)
        await self.broadcast_board_data()

    async def add_card(self, content):
        """
        カードの追加
        """
        pipe_line_id = content['pipeLineId']
        card_title = content['cardTitle']
        await database_sync_to_async(service.add_card)(pipe_line_id, card_title)
        await self.broadcast_board_data()

    async def rename_board(self, content):
        """
        ボード名の変更
        :param content:
        :return:
        """
        board_id = content['boardId']
        board_name = content['boardName']
        await database_sync_to_async(service.update_board)(board_id, board_name)
        await self.broadcast_board_data()

    async def rename_pipe_line(self, content):
        """
        パイプライン名の変更
        """
        pipe_line_id = content['pipeLineId']
        pipe_line_name = content['pipeLineName']
        await database_sync_to_async(service.update_pipe_line)(pipe_line_id, pipe_line_name)
        await self.broadcast_board_data()

    async def delete_pipe_line(self, content):
        """
        パイプラインの削除
        :param content:
        :return:
        """
        board_id = content['boardId']
        pipe_line_id = content['pipeLineId']
        await database_sync_to_async(service.delete_pipe_line)(pipe_line_id)
        await self.broadcast_board_data()

    async def delete_board(self, content):
        """
        ボードの削除
        :param content:
        :return:
        """
        board_id = content['boardId']
        await database_sync_to_async(service.delete_board)(board_id)
        await self.broadcast_delete_board()

    async def send_back_to_home(self, *args):
        await self.send_data({}, action='backToHome')

    async def broadcast_delete_board(self, *args):
        """
        各ConsumerにクライアントをHomeへリダイレクトするよう指示させる
        :param args:
        :return:
        """
        await self.group_send(
            self.room_group_name,
            {
                'type': 'send_back_to_home',
            }
        )

    async def broadcast_board_data(self, *args):
        """
        各Consumerにボードの最新データを返送するよう指示する
        :param args:
        :return:
        """
        await self.group_send(
            self.room_group_name,
            {
                'type': 'send_board_data',
            }
        )

    async def broadcast_board_data_without_requester(self, *args):
        """
        このメソッドを呼び出したConsumer以外にボードデータを返送するよう指示する
        """
        await self.group_send(
            self.room_group_name,
            {
                'type': 'send_board_data',
                'requester_id': self.consumer_id,
            }
        )
