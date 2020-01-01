import json

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView
from django.contrib.auth.forms import UserCreationForm

from .service import *


# CreateView...モデル(データ)の作成を簡単にしてくれる関数
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class AccountsApi(View):

    def get(self, request):
        """
        認証済であればログイン情報を戻す
        """
        account = request.user
        # ログイン済みかのチェック
        if account.is_authenticated:
            return JsonResponse({
                'account_info': {
                    'account_id': account.id,
                    'name': account.username,
                }
            })

        return JsonResponse({
            'account_info': None,
        })


class BaseApiView(View):
    """
    API系Viewの基底クラス
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_member = None

    def dispatch(self, request, *args, **kwargs):
        self.login_member = request.user
        return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class BoardListApi(BaseApiView):

    def get(self, _):
        """
        ボードの一覧を戻す
        """
        board_list = []
        for board in get_board_list_by_owner(self.login_member):
            board_list.append({
                'id': board.id,
                'name': board.name,
            })
        return JsonResponse({
            'board_list': board_list,
        })

    def post(self, request):
        """
        新しいボードを追加する
        """
        data = json.loads(request.body)
        board_name = data.get('boardName')
        board = add_board(
            owner=self.login_member,
            board_name=board_name
        )
        return JsonResponse({
            'board_data': {
                'id': board.id,
                'name': board.name,
            }
        })


@method_decorator(csrf_exempt, name='dispatch')
class CardApi(BaseApiView):

    def get(self, _, board_id, card_id):
        """
        カードを追加する
        """
        card = get_card_by_card_id(card_id)

        return JsonResponse({
            'card_data': {
                'title': card.title,
                'content': card.content,
                'updated_at': card.updated_at,
            }
        })

    def patch(self, request, board_id, card_id):
        """
        カードの内容を更新する
        """
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        card = update_card(card_id=card_id, title=title, content=content)

        return JsonResponse({
            'card_data': {
                'title': card.title,
                'content': card.content,
                'updated_at': card.updated_at,
            }
        })

    def delete(self, _, board_id, card_id):
        """
        カードを削除する
        """
        delete_card(card_id=card_id)
        return JsonResponse({
            'success': True
        })
