from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=150,
        verbose_name="Единицы измерения"
    )

    class Meta():
        verbose_name = "Ингридиенты"
        verbose_name_plural = "Ингридиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique_name_measurement_unit"
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name="Название тега"
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="HEX-код"
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name="Slug"
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор рецепта",
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название рецепта",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингридиенты",
    )
    text = models.TextField(verbose_name="Описание")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время готовки"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):