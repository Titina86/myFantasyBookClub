from django.db import models
from django.conf import settings

from accounts.models import Profile
from books.models import MyBook


class ReadingJournal(models.Model):

    user = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='reading_journal'
    )

    book = models.OneToOneField(
        to=MyBook,
        on_delete=models.CASCADE,
        max_length=255,
        related_name="my_book",
        verbose_name='Book'
    )

    characters = models.TextField(
        blank=True,
        null=True,
        verbose_name="Characters"
    )

    favorite_character = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Favorite Character"
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Start Date"
    )

    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="End Date"
    )

    pages = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Pages"
    )

    favorite_moment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Favorite Moment"
    )
    about = models.TextField(
        blank=True,
        null=True,
        verbose_name="About")

    recommended_by = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Recommended By"
    )
    quotes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Quotes")
    will_recommend_to_friend = models.BooleanField(
        default=False,
        verbose_name="Will Recommend to a Friend")

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At")
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At")

    class Meta:
        verbose_name = "Reading Journal"
        verbose_name_plural = "Reading Journals"
        ordering = ['-created_at']

