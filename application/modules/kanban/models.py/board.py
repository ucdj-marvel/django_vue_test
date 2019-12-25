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
