from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from .accounts import signup as signup_view
from .api.accounts import AccountsApi
from .api.boards import BoardListApi, CardApi, CardGetApi


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', signup_view.SignUpView.as_view(), name='signup'),
    path('api/accounts/', AccountsApi.as_view()),
    path('api/boards/', login_required(BoardListApi.as_view())),
    path('api/boards/<int:board_id>/cards/<int:card_id>/', login_required(CardGetApi.as_view())),
    path('api/cards/', login_required(CardApi.as_view())),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# app routing to vue-router
urlpatterns += [
    re_path('.*', login_required(TemplateView.as_view(template_name='index.html')))  # 特定URLへのアクセスをログイン必須にする
]
