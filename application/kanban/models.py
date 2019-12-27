from django.conf import settings
from django.db import models


class Board(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} of {}'.format(self.pk, self.name, self.owner)

    @classmethod
    def create(cls, **params):
        return cls.objects.create(**params)

    @classmethod
    def is_exist(cls, board_id):
        return Board.objects.filter(id=board_id).exists()

    @classmethod
    def get_by_id(cls, board_id):
        try:
            return cls.objects.get(pk=board_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_list_by_owner(cls, owner):
        return list(cls.objects.filter(owner=owner).order_by('updated_at'))


class PipeLine(models.Model):

    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name='pipe_lines')
    name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} of {}'.format(self.pk, self.name, self.board)

    @classmethod
    def create(cls, **params):
        return cls.objects.create(**params)

    @classmethod
    def get_by_id(cls, pipe_line_id):
        try:
            return cls.objects.get(id=pipe_line_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_list_by_board(cls, board):
        return list(cls.objects.filter(board=board).order_by('order'))

    @classmethod
    def get_current_pipe_line_count_by_board(cls, board):
        return cls.objects.filter(board=board).count()


class Card(models.Model):

    pipe_line = models.ForeignKey(to=PipeLine, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} of {}'.format(self.pk, self.title, self.pipe_line)

    @classmethod
    def create(cls, **params):
        return cls.objects.create(**params)

    @classmethod
    def get_by_id(cls, card_id):
        try:
            return cls.objects.get(id=card_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_by_pipe_line(cls, pipe_line):
        cls.objects.filter(pipe_line=pipe_line).delete()

    @classmethod
    def get_list_by_pipe_line(cls, pipe_line):
        return list(cls.objects.filter(pipe_line=pipe_line).order_by('order'))

    @classmethod
    def get_current_card_count_by_pipe_line(cls, pipe_line):
        return cls.objects.filter(pipe_line=pipe_line).count()

