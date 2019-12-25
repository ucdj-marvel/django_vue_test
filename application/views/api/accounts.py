from django.http import JsonResponse
from django.views.generic import View


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
