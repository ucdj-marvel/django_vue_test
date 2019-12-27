from django.db import models


# 縦のラインを管理（親カードを表す）
class PipeLine(models.Model):

    board = models.ForeignKey('kanban.Board', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} of {}'.format(self.pk, self.name, self.board)

    # パイプライン新規作成
    @classmethod
    def create(cls, **params):
        return cls.objects.create(**params)

    # Boardに紐づくものすべてのPipeLineを戻すメソッド
    @classmethod
    def get_list_by_board(cls, board):
        return list(cls.objects.filter(board=board).order_by('order'))

    # PipeLineをID指定で取得
    @classmethod
    def get_by_id(cls, pipe_line_id):
        try:
            return cls.objects.get(id=pipe_line_id)
        except cls.DoesNotExist:
            return None

    # 新規追加時点のパイプラインの数取得
    @classmethod
    def get_current_pipe_line_count_by_board(cls, board):
        return cls.objects.filter(board=board).count()
