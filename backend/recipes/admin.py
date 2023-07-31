from django.contrib import admin

from recipes.models import (
    IngredientRecipe,
    ShoppingCart,
    Ingredient,
    Favorite,
    Recipe,
    Tag
)


class IngredientInline(admin.TabularInline):
    """
    Встроенная административная форма для модели IngredientRecipe.
    Используется для отображения ингредиентов рецепта
    в административной панели.
    """
    model = IngredientRecipe


class RecipeAdmin(admin.ModelAdmin):
    """
    Класс административной формы для модели Recipe.
    Используется для настройки отображения и фильтрации рецептов
    в административной панели.
    """
    list_display = (
        "name",
        "author",
    )
    search_fields = (
        "name",
        "author__username",
        "tags__name",
    )
    list_filter = ("name", "author__username", "tags__name")
    inlines = (IngredientInline,)
    empty_value_display = "-пусто-"

    def get_favorites(self, obj):
        """
        Возвращает количество добавлений рецепта в избранное.
        """
        return obj.favorites.count()
    get_favorites.short_description = "Избранное"

    def get_ingredients(self, obj):
        """
        Возвращает строку с перечислением ингредиентов рецепта.
        """
        return ', '.join([
            ingredients.name for ingredients
            in obj.ingredients.all()])
    get_ingredients.short_description = "Ингридиенты"


class TagAdmin(admin.ModelAdmin):
    """
    Класс административной формы для модели Tag.
    Используется для настройки отображения и фильтрации тегов
    в административной панели.
    """
    list_display = (
        "name",
        "color",
        "slug",
    )

    search_fields = ("name", "slug",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    """
    Класс административной формы для модели Ingredient.
    Используется для настройки отображения и фильтрации ингредиентов
    в административной панели.
    """
    list_display = ("name", "measurement_unit",)
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class FavoriteAdmin(admin.ModelAdmin):
    """
    Класс административной формы для модели Favorite.
    Используется для настройки отображения и фильтрации избранных рецептов
    в административной панели.
    """
    list_display = ("user", "recipe",)
    # list_filter = ("user", "recipe",)
    search_fields = ("user__username", "recipe__name")
    empty_value_display = "-пусто-"


class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Класс административной формы для модели ShoppingCart.
    Используется для настройки отображения и фильтрации списка покупок
    в административной панели.
    """
    list_display = ("recipe", "user",)
    # list_filter = ("recipe", "user",)
    search_fields = ("user__username", "recipe__name")
    empty_value_display = "-пусто-"


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
