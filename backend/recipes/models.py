from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

from users.models import User
from api.validators import (
    validate_cooking_time,
    validate_ingredients,
    validate_amount,
    validate_tags
)


class Ingredient(models.Model):
    """
    Модель для ингредиента.
    """
    name = models.CharField(
        max_length=settings.MAX_COUNT_CHARS_TWO_HUNDRED,
        db_index=True,
        verbose_name="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=settings.MAX_COUNT_CHARS_TWO_HUNDRED,
        verbose_name="Единицы измерения"
    )

    class Meta():
        """
        Метакласс для модели Ingredient.
        Определяет метаданные модели Ingredient, такие как
        ограничения на уникальность
        комбинации названия и единиц измерения
        и названия модели в единственном и множественном числе.
        """
        verbose_name = "Ингридиенты"
        verbose_name_plural = "Ингридиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique_name_measurement_unit"
            )
        ]

    def __str__(self):
        """
        Возвращает строковое представление ингредиента.
        """
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Модель для тега.
    """
    name = models.CharField(
        max_length=settings.MAX_COUNT_CHARS_TWO_HUNDRED,
        unique=True,
        db_index=True,
        verbose_name="Название тега"
    )
    color = models.CharField(
        max_length=settings.MAX_COUNT_CHARS_SEVEN,
        unique=True,
        verbose_name="HEX-код",
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                message='Проверьте вводимый формат'
            )
        ]
    )
    slug = models.SlugField(
        max_length=settings.MAX_COUNT_CHARS_TWO_HUNDRED,
        unique=True,
        verbose_name="Slug"
    )

    class Meta:
        """
        Метакласс для модели Tag.
        Определяет метаданные модели Tag, такие как
        сортировку по имени и
        названия модели в единственном и множественном числе.
        """
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """
        Возвращает строковое представление тега.
        """
        return self.name


class Recipe(models.Model):
    """
    Модель для рецепта.
    """
    author = models.ForeignKey(
        User,
        verbose_name="Автор рецепта",
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    name = models.CharField(
        max_length=settings.MAX_COUNT_CHARS_TWO_HUNDRED,
        verbose_name="Название рецепта",
    )
    tags = models.ManyToManyField(
        Tag,
        validators=[validate_tags],
        verbose_name="Теги"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        validators=[validate_ingredients],
        verbose_name="Ингридиенты",
    )
    text = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="recipes/image/",
        verbose_name="Изображение"
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[validate_cooking_time],
        verbose_name="Время готовки"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )

    class Meta:
        """
        Метакласс для модели Recipe.
        Определяет метаданные модели Recipe, такие как
        сортировку по дате публикации (сначало новые)
        и названия модели в единственном и множественном числе.
        """
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        """
        Возвращает строковое представление рецепта.
        """
        return self.name


class IngredientRecipe(models.Model):
    """
    Модель для ингредиента рецепта
    (промежуточная таблица многие-ко-многим).
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name="Ингредиент"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[validate_amount],
        verbose_name='Количество ингредиента'
    )

    class Meta:
        """
        Метакласс для модели IngredientRecipe.
        Определяет метаданные модели IngredientRecipe,
        такие как сортировка по убыванию id
        и названия модели в единственном и множественном числе.
        """
        ordering = ("-id",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты рецепта"

    def __str__(self):
        """
        Возвращает строковое представление связи между рецептом и ингредиентом.
        """
        return f"{self.recipe.name} - {self.ingredient.name}"


class Favorite(models.Model):
    """
    Модель для избранного.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт"
    )

    class Meta:
        """
        Метакласс для модели Favorite.
        Определяет метаданные модели Favorite,
        такие как ограничение уникальности,
        а также названия модели в единственном и множественном числе.
        """
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe_favorite"
            )
        ]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        """
        Возвращает строковое представление избранного рецепта.
        """
        return f"{self.user} добавил {self.recipe.name} в избраннное"


class ShoppingCart(models.Model):
    """
    Модель для списка покупок пользователей.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Рецепт"
    )

    class Meta:
        """
        Метакласс для модели ShoppingCart.
        Определяет метаданные модели ShoppingCart,
        такие как сортировка по убыванию id,
        ограничение уникальности поля "user" и "recipe",
        а также названия модели в единственном и множественном числе.
        """
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_shopping_cart"
            )
        ]
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок'"

    def __str__(self):
        """
        Возвращает строковое представление списка покупок.
        """
        return f"{self.user} добавил {self.recipe.name} в список покупок"
