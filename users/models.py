from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        _('first name'), max_length=30, blank=True, null=True
    )
    last_name = models.CharField(
        _('last name'), max_length=150, blank=True, null=True
    )
    email = models.EmailField(unique=True)

    USER = 1
    MODERATOR = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        default=1,
        verbose_name='Права доступа'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Информация о пользователе'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def get_role(self):
        roles_dict = dict(self.ROLE_CHOICES)
        role = roles_dict[self.role]
        return role

    def __str__(self):
        return self.email
