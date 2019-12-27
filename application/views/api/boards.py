import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

from modules.kanban import service as kanban_sv


# APIでCSRFを考慮するのは複雑なので、解除
# Djangoではgetやpostに処理を引き渡す
# dispatchというメソッドがデフォルトで定義
# そこにcsrf_exemptを付与する
# TODO: APIにCSRFを適用
@method_decorator(csrf_exempt, name='dispatch')
class BoardListApi(View):

    def get(self, request):
        """
        ボードの一覧を戻す
        """
        board_list = []
        for board in kanban_sv.get_board_list_by_owner(request.user):
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
        board = kanban_sv.add_board(
            owner=request.user,
            board_name=board_name
        )
        return JsonResponse({
            'board_data': {
                'id': board.id,
                'name': board.name,
            }
        })


# add_cardを呼び出すAPI
@method_decorator(csrf_exempt, name='dispatch')
class CardApi(View):

    def post(self, request):
        """
        新しいcardを追加する
        """
        data = json.loads(request.body)
        card_title = data.get('cardTitle')
        pipe_line_id = data.get('pipeLineId')

        card = kanban_sv.add_card(
            pipe_line_id=pipe_line_id,
            card_title=card_title
        )
        return JsonResponse({
            'card_data': {
                'id': card.id,
                'name': card.title,
            }
        })


# モーダルで表示するカードを取得
@method_decorator(csrf_exempt, name='dispatch')
class CardGetApi(View):

    def get(self, _, board_id, card_id):
        """
        カードを取得する
        """
        card = kanban_sv.get_card_by_card_id(card_id)

        return JsonResponse({
            'card_data': {
                'title': card.title,
                'content': card.content,
                'updated_at': card.updated_at,
            }
        })
