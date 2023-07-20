from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name"
    )
    USERNAME_FIELD = ("email")
    email = models.EmailField(
        max_length=150,
        verbose_name="email",
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="username"
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия"
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
