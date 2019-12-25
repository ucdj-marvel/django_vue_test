from .models import Board


# API側はget_board_list_by_ownerを呼び出す
def get_board_list_by_owner(owner):
    return Board.get_list_by_owner(owner=owner)
