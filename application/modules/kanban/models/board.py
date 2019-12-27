from django.conf import settings
from django.db import models


class Board(models.Model):
    """
    1枚のカンバンを表現する
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 所有者
    name = models.CharField(max_length=255)  # ボード名

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} of {}'.format(self.pk, self.name, self.owner)

    # ORMはモデルクラスに書いてしまうほうが整理しやすい
    @classmethod
    def get_list_by_owner(cls, owner):
        """
        ユーザが保持するボードの一覧を戻すORM
        """
        return list(cls.objects.filter(owner=owner).order_by('updated_at'))

    # Boardを取得⇨紐づくPipeLineの一覧を取得⇨紐づくCard一覧取得
    @classmethod
    def get_by_id(cls, board_id):
        try:
            return cls.objects.get(pk=board_id)
        except cls.DoesNotExist:
            return None
