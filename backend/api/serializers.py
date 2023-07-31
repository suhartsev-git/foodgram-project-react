from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from api.validators import (
    validate_cooking_time,
    validate_ingredients,
    validate_subscribed,
    validate_tags
)
from users.models import User, Subscription
from recipes.models import (
    IngredientRecipe,
    ShoppingCart,
    Ingredient,
    Favorite,
    Recipe,
    Tag
)


class UserCreateSerializerCustom(UserCreateSerializer):
    """
    Кастомный сериализатор для создания пользователя.
    """

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        UserCreateSerializerCustom.
        Здесь мы указываем модель, с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )

        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }


class UserSerializerCustom(UserSerializer):
    """
    Пользовательский сериализатор для пользователя.
    Добавляет поле is_subscribed, которое показывает,
    подписан ли текущий пользователь на пользователя из контекста запроса.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        UserSerializerCustom.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )

    lookup_field = 'username'

    def get_is_subscribed(self, obj):
        """
        Определяет,
        подписан ли текущий пользователь на пользователя из контекста запроса.
        """
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user, author=obj.id
            ).exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.
    """

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        TagSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ingredient.
    """

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        IngredientSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = Ingredient
        fields = "__all__"


class BriefInfoSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор для модели Recipe,
    содержащий только базовую информацию.
    """
    image = Base64ImageField()

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        BriefInfoSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class IngredientAddSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления ингредиентов.
    """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели IngredientRecipe,
    включая данные из связанной модели Ingredient.
    """
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.IntegerField(
        source='ingredient.id',
        read_only=True
    )

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        IngredientInRecipeSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = IngredientRecipe
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Subscription.
    Включает информацию о подписке пользователя на автора рецептов.
    """
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    username = serializers.ReadOnlyField(source='author.username')
    recipes = serializers.SerializerMethodField()
    id = serializers.ReadOnlyField(source='author.id')

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        SubscriptionSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = Subscription
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            'recipes_count',
        )

    def validate(self, data):
        """
        Проверяет валидность данных перед созданием или обновлением подписки.
        """
        request_user = self.context["request"].user
        data = validate_subscribed(data, request_user)
        return data

    def get_is_subscribed(self, obj):
        """
        Определяет, подписан ли текущий пользователь на автора рецептов.
        """
        return Subscription.objects.filter(
            user=self.context["request"].user,
            author=obj.author
        ).exists()

    def get_recipes(self, obj):
        """
        Получает список рецептов автора, связанных с объектом Subscription.
        """
        recipes_limit = (
            self.context["request"].query_params.get("recipes_limit")
        )
        queryset = (
            obj.author.recipes.all()[:int(recipes_limit)] if recipes_limit
            else obj.author.recipes.all()
        )
        return BriefInfoSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """
        Получает количество рецептов автора.
        """
        return Recipe.objects.filter(author=obj.author).count()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления модели Recipe.
    """
    author = UserSerializerCustom(read_only=True)
    cooking_time = serializers.IntegerField(
        validators=[validate_cooking_time]
    )
    ingredients = IngredientAddSerializer(
        many=True,
        validators=[validate_ingredients]
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        validators=[validate_tags]
    )
    image = Base64ImageField()

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        RecipeCreateSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def validate(self, data):
        ingredients = data['ingredient_number']
        if len(ingredients) != len(
                set(obj['ingredient'] for obj in ingredients)):
            raise serializers.ValidationError(
                'Выбран повторно один и тот же ингредиент')
        return super().validate(data)

    # def validate_ingredients(self, value):
    #     ingredients_list = []
    #     for item in value:
    #         ingredient = get_object_or_404(
    #             Ingredient, id=item["id"]
    #         )
    #         if ingredient in ingredients_list:
    #             raise serializers.ValidationError({
    #                 "ingredients": "Ингридиенты не должны повторяться."
    #             })
    #         ingredients_list.append(ingredient)
    #     return value

    def create_ingredients(self, ingredients, recipe):
        """
        Создает связанные объекты IngredientRecipe для рецепта.
        """
        ingredient_list = [
            IngredientRecipe(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient, id=ingredient.get("id")
                ),
                amount=ingredient.get("amount")
            )
            for ingredient in ingredients
        ]
        IngredientRecipe.objects.bulk_create(ingredient_list)

    @transaction.atomic
    def create(self, validated_data):
        """
        Создает новый рецепт.
        """
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(
            author=self.context["request"].user,
            **validated_data
        )
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Обновляет существующий рецепт.
        """
        instance.tags.clear()
        tags = validated_data.pop("tags")
        instance.tags.set(tags)
        instance.ingredients.clear()
        ingredients = validated_data.pop("ingredients")
        self.create_ingredients(ingredients, instance)
        return super().update(
            instance,
            validated_data
        )

    def to_representation(self, instance):
        """
        Преобразует объект модели Recipe в представление для чтения.
        """
        return RecipeReadSerializer(
            instance, context=self.context
        ).data


class RecipeReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения модели Recipe.
    Включает дополнительные поля, такие как информация о пользователе,
    тегах, ингредиентах, а также флаги is_favorited и is_in_shopping_cart,
    которые показывают, добавлен ли рецепт в избранное или корзину покупок.
    """
    author = UserSerializerCustom(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = IngredientInRecipeSerializer(
        source="ingredientrecipe",
        many=True,
    )

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        RecipeReadSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        """
        Получает список ингредиентов, связанных с текущим объектом Recipe.
        """
        ingredients_list = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients_list, many=True).data

    def get_is_in_shopping_cart(self, obj):
        """
        Определяет,
        добавлен ли текущий рецепт в корзину покупок текущего пользователя.
        """
        request = self.context.get("request")
        if request.user.is_authenticated:
            return obj.carts.filter(user=request.user).exists()
        return False

    def get_is_favorited(self, obj):
        """
        Определяет,
        добавлен ли текущий рецепт в избранное текущего пользователя.
        """
        request = self.context.get("request")
        if request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ShoppingCart.
    """

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        ShoppingCartSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = ShoppingCart
        fields = "__all__"

    def to_representation(self, instance):
        """
        Преобразует объект модели ShoppingCart в представление.
        Возвращает краткую информацию о рецепте,
        связанном с объектом ShoppingCart.
        """
        return BriefInfoSerializer(
            instance.recipe,
            context={"request": self.context.get("request")}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Favorite.
    """

    class Meta:
        """
        Класс Meta определяет метаданные для сериализатора
        FavoriteSerializer.
        Здесь мы указываем модель с которой работает сериализатор
        и поля которые будут сериализованы.
        """
        model = Favorite
        fields = "__all__"

    def to_representation(self, instance):
        """
        Преобразует объект модели Favorite в представление.
        Возвращает краткую информацию о рецепте,
        связанном с объектом Favorite.
        """
        return BriefInfoSerializer(
            instance.recipe,
            context={"request": self.context.get("request")}
        ).data
