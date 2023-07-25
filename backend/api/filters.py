from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe, Tag


class SearchIngredientFilter(SearchFilter):
    search_param = "name"

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(filters.FilterSet):
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
        model = Recipe
        fields = (
            "is_in_shopping_cart",
            "is_favorited",
            "author",
            "tags",
        )

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and self.request.user.is_authenticated:
            return queryset.filter(carts__user=user)
        return queryset

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset
