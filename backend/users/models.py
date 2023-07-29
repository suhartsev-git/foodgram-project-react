from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Абстрактная модель пользователя.
    """
    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name"
    )
    USERNAME_FIELD = ("email")
    email = models.EmailField(
        max_length=settings.MAX_COUNT_CHARS_TWO_HUNDRED_FIFTY_FOUR,
        unique=True,
        verbose_name="email"
    )
    username = models.CharField(
        max_length=settings.MAX_COUNT_CHARS_ONE_HUNDRED_FIFTY,
        unique=True,
        verbose_name="username",
        validators=(UnicodeUsernameValidator(),)
    )
    first_name = models.CharField(
        max_length=settings.MAX_COUNT_CHARS_ONE_HUNDRED_FIFTY,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=settings.MAX_COUNT_CHARS_ONE_HUNDRED_FIFTY,
        verbose_name="Фамилия"
    )

    class Meta:
        """
        Метакласс для модели User.
        Определяет метаданные модели User,
        такие как сортировка по имени пользователя,
        а также названия модели в единственном и множественном числе.
        """
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Возвращает строковое представление пользователя.
        """
        return self.username


class Subscription(models.Model):
    """
    Модель для подписки пользователя на автора рецептов.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="subscriptions",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="subscribers"
    )

    class Meta:
        """
        Метакласс для модели Subscription.
        Определяет метаданные модели Subscription,
        такие как сортировка по id в обратном порядке
        (сначало новые), а также ограничение на уникальность
        комбинации полей 'user' и 'author',
        чтобы пользователь мог подписаться только
        один раз на одного автора.
        """
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_subscription'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        """
        Возвращает строковое представление подписки.
        """
        return f"{self.user} подписан на {self.author}"
