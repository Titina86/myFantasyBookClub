from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Profile
from books.models import AdminBook


class Comment(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['date_time_of_publication']),
        ]
        ordering = ['-date_time_of_publication']

    text = models.TextField(
        max_length=300,
    )

    date_time_of_publication = models.DateTimeField(
        auto_now_add=True,
    )

    to_book = models.ForeignKey(
        to=AdminBook,
        on_delete=models.CASCADE,
    )

    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
    )