from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter

from recipes.models import (
    Ingredient,
    Recipe,
    Tag
)


class SearchIngredientFilter(SearchFilter):
    """
    Фильтр поиска для модели Ingredient.
    Класс 'SearchIngredientFilter' даёт возможность выполнять поиск по
    полю 'name' модели Ingredient.
    """
    search_param = "name"

    class Meta:
        """Метакласс 'SearchIngredientFilter'
        определяет свойства для фильтрации поиска.
        """
        model = Ingredient
        fields = ("name",)


class RecipeFilter(FilterSet):
    """
    Фильтры для модели Recipe.
    Класс 'RecipeFilter' определяет несколько кастомных фильтров,
    которые можно использовать для фильтрации списка рецептов.
    """
    tags = filters.ModelMultipleChoiceFilter(
        to_field_name="slug",
        field_name="tags__slug",
        queryset=Tag.objects.all(),
    )
    is_in_shopping_cart = filters.NumberFilter(
        method="is_in_shopping_cart_filter"
    )
    is_favorited = filters.NumberFilter(
        method="is_favorited_filter"
    )

    class Meta:
        """Метакласс 'RecipeFilter'
        определяет свойства фильтрации для модели Recipe
        """
        model = Recipe
        fields = (
            "is_in_shopping_cart",
            "is_favorited",
            "author",
            "tags",
        )

    def is_in_shopping_cart_filter(self, queryset, name, value):
        """
        Фильтр по наличию рецепта в корзине покупок текущего пользователя.
        """
        user = self.request.user
        if value and self.request.user.is_authenticated:
            return queryset.filter(carts__user=user)
        return queryset

    def is_favorited_filter(self, queryset, name, value):
        """
        Фильтр по наличию рецепта в списке избранного текущего пользователя.
        """
        user = self.request.user
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset
