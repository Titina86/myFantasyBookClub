from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from accounts.managers import AppUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    objects = AppUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )
    first_name = models.CharField(
        max_length=20,
    )
    last_name = models.CharField(
        max_length=20,
    )
    email = models.EmailField(
        unique=True,
    )
    profile_picture = models.URLField(
        blank=True,
        null=True,
    )

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

