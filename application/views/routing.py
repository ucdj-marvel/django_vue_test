from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from .ws.kanban_consumer import KanbanConsumer

# channelsのエントリーポイント(最初にアクセスされるファイル)
# デフォルトではHTTP用のルールが自動設定
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/boards/<int:board_id>', KanbanConsumer),
        ])
    ),
})
