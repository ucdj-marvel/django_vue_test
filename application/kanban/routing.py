from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from .consumer import KanbanConsumer

urlpatterns = [
    path('ws/boards/<int:board_id>', KanbanConsumer)
]

# channelsのエントリーポイント(最初にアクセスされるファイル)
# デフォルトではHTTP用のルールが自動設定
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            urlpatterns
        )
    ),
})
