from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import Profile

UserModel = get_user_model()


class Book(models.Model):

    title = models.CharField(
        max_length=255,
        unique=True,
    )
    author = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    cover = models.URLField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class AdminBook(Book):
    created_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='admin_books'
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_monthly_book = models.BooleanField(
        default=False
    )
    monthly_book_date = models.DateField(
        null=True,
        blank=True
    )

    @classmethod
    def get_monthly_books(cls):
        return cls.objects.filter(
            is_monthly_book=True,
            monthly_book_date__month=date.today().month,
            monthly_book_date__year=date.today().year
        )


class MyBook(Book):

    profile = models.ManyToManyField(
        Profile,
        related_name='my_books'
    )



