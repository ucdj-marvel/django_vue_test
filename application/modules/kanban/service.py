from .models import Board, Card, PipeLine


# API側はget_board_list_by_ownerを呼び出す
def get_board_list_by_owner(owner):
    return Board.get_list_by_owner(owner=owner)


# ボードを追加するメソッド
def add_board(owner, board_name):
    """
    :param User owner:
    :param str board_name:
    :return:
    """
    board = Board.objects.create(
        owner=owner,
        name=board_name
    )
    return board


# Djangoではmanage.py shellで実装したメソッドなどが試せる
# $ docker-compose exec service ./manage.py shell
# でコンテナに入り
# get_board_data_by_board_idを実行
def get_board_data_by_board_id(board_id):
    """
    borad and pipeline and card.
    :param int board_id:
    :return:
    :rtype: dict
    """
    # ボード取得
    board = Board.get_by_id(board_id)
    board_data = {
        'board_id': board.id,
        'name': board.name,
        'pipe_line_list': []
    }
    # ボードに紐づく各パイプライン取得
    for pipe_line in PipeLine.get_list_by_board(board):
        pipe_line_data = {
            'pipe_line_id': pipe_line.id,
            'name': pipe_line.name,
            'card_list': []
        }
        # パイプラインに紐づくカードを取得
        for card in Card.get_list_by_pipe_line(pipe_line):
            pipe_line_data['card_list'].append({
                'card_id': card.id,
                'title': card.title,
                'content': card.content,
            })
        board_data['pipe_line_list'].append(pipe_line_data)

    return board_data


# PipeLineのIDと新しい並び順としてのCardIdのListを受け取り
# その順にcard.orderを更新するサービス
def update_card_order(pipe_line_id, card_id_list):
    """
    :param int pipe_line_id:
    :param list card_id_list:
    :return:
    """
    pipe_line = PipeLine.get_by_id(pipe_line_id)
    for i, card_id in enumerate(card_id_list):
        card = Card.get_by_id(card_id)
        card.order = i
        card.pipe_line = pipe_line
        card.save()


# カードを追加
def add_card(pipe_line_id, card_title):
    pipe_line = PipeLine.get_by_id(pipe_line_id)
    current_count = Card.get_current_card_count_by_pipe_line(pipe_line)
    card = Card(
        title=card_title,
        content=None,
        pipe_line=pipe_line,
        order=current_count + 1,  # 現在のカード数1で末尾になる
    )
    card.save()
    return card


# カードを取得
def get_card_by_card_id(card_id):
    """
    :param int card_id:
    :return:
    """
    return Card.get_by_id(card_id)


# カードの更新
def update_card(card_id, title=None, content=None):
    """
    :param int card_id:
    :param str title:
    :param str content:
    :return:
    :rtype Card:
    """
    card = Card.get_by_id(card_id)
    if title:
        card.title = title
    if content:
        card.content = content
    card.save()
    return card


# カードの削除
def delete_card(card_id):
    card = Card.get_by_id(card_id)
    card.delete()

# パイプライン追加
def add_pipe_line(board_id, pipe_line_name):
    board = Board.get_by_id(board_id)
    current_count = PipeLine.get_current_pipe_line_count_by_board(board)
    return PipeLine.create(
        board=board,
        name=pipe_line_name,
        order=current_count + 1,
    )

# パイプライン更新
def update_pipe_line(pipe_line_id, name=None):
    """
    :param int pipe_line_id:
    :param str name:
    :return:
    """
    pipe_line = PipeLine.get_by_id(pipe_line_id)
    if name:
        pipe_line.name = name
    pipe_line.save()
    return pipe_line

# パイプライン削除
def delete_pipe_line(pipe_line_id):
    pipe_line = PipeLine.get_by_id(pipe_line_id)
    pipe_line.delete()
