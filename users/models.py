from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )

    first_name = models.CharField(
        max_length=30, blank=True, null=True
    )
    last_name = models.CharField(
        max_length=150, blank=True, null=True
    )
    email = models.EmailField(unique=True)

    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    role = models.CharField(
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name='Права доступа',
        max_length=150
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Информация о пользователе'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
