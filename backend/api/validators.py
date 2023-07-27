from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from users.models import Subscription


def validate_ingredients(value):
    """
    Валидатор для поля "ingredients" в рецепте.
    """
    if not value or value < settings.MIN_VALUE_IS_ONE:
        raise ValidationError(
            f"Количество ингредиентов не может быть пустым, "
            f"или быть меньше чем {settings.MIN_VALUE_IS_ONE}"
        )
    return value


def validate_tags(value):
    """
    Валидатор для поля "tags" в рецепте.
    """
    if not value:
        raise ValidationError(
            "Необходимо выбрать тег или теги"
        )
    return value


def validate_cooking_time(value):
    """
    Валидатор для поля "cooking_time" в рецепте.
    """
    if not value or value <= settings.MIN_VALUE_IS_ONE:
        raise ValidationError(
            f"Время приготовления не может быть пустым, или быть "
            f"меньше {settings.MIN_VALUE_IS_ONE}-й минуты."
        )
    return value


def validate_amount(value):
    """
    Валидатор для поля "amount" в рецепте.
    """
    if not value or value < settings.MIN_VALUE_IS_ONE:
        raise ValidationError(
            f"Количество ингредиентов не может быть пустым, "
            f"или быть меньше чем {settings.MIN_VALUE_IS_ONE}"
        )
    return value


def validate_subscribed(data, request_user):
    """
    Проверяет валидность данных при создании подписки.
    При создании подписки проверяет,
    что текущий пользователь не пытается
    подписаться на самого себя
    и что подписка на данного автора уже не существует.
    """
    author = data["author"]
    if request_user == author:
        raise serializers.ValidationError(
            "Вы не можете подписаться на самого себя."
        )
    if Subscription.objects.filter(
        user=request_user, author=author
    ).exists():
        raise serializers.ValidationError(
            "Вы уже подписаны на этого автора."
        )
    return data
