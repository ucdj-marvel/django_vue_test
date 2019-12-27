from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Childのルーティングルールに分割
from .ws.routing import urlpatterns

# channelsのエントリーポイント(最初にアクセスされるファイル)
# デフォルトではHTTP用のルールが自動設定
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            urlpatterns
        )
    ),
})
