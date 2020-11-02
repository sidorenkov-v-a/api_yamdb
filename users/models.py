from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

username_validator = UnicodeUsernameValidator()


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    email = models.EmailField(unique=True)

    role = models.CharField(
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name='Права доступа',
        max_length=20
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Информация о пользователе'
    )

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR or self.is_staff

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN or self.is_superuser

    def __str__(self):
        return self.email
