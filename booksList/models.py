from django.db import models

from accounts.models import Profile
from books.models import MyBook


class BooksList(models.Model):
    class ReadStatus(models.TextChoices):
        WISH_LIST = 'Wish List', 'Wish List'
        IN_PROGRESS = 'In Progress', 'In Progress'
        COMPLETED = 'Completed', 'Completed'

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        MyBook,
        on_delete=models.CASCADE,
        related_name='my_list_book',
    )

    read_status = models.CharField(
        max_length=15,
        choices=ReadStatus.choices,
        default=ReadStatus.WISH_LIST,
    )

    have_journal = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.book.title

    class Meta:
        unique_together = ('profile', 'book')