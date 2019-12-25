from django.http import JsonResponse
from django.views.generic import View

from modules.kanban import service as kanban_sv


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
