from django.db import models

from accounts.models import Profile
from books.models import MyBook


class BooksList(models.Model):
    class ReadStatus(models.TextChoices):
        WISH_LIST = 'wish_list', 'Wish List'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        MyBook,
        on_delete=models.CASCADE
    )

    read_status = models.CharField(
        max_length=15,
        choices=ReadStatus.choices,
        default=ReadStatus.WISH_LIST,
    )

    class Meta:
        unique_together = ('profile', 'book')  # За да няма дублирани записи за една и съща книга за един профил