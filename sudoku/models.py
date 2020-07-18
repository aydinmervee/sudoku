from django.conf import settings
from django.db import models


class Sudoku(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    size = models.IntegerField()
    game = models.CharField(max_length=512)
    solution = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Sudoku - ' + str(self.id)
