from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import User, Subscription
from recipes.models import Tag, Ingredient, Recipe, ShoppingCart


class UserCreateSerializerCustom(UserCreateSerializer):

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'password': {'required': True}
        }


class UserSerializerCustom(UserSerializer):

    class Meta:
        fields = "__all__"

    model = User
    lookup_field = 'username'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = "__all__"


class BriefInfoSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.IntegerField(
        source="author.recipes.count",
        read_only=True
    )
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context["request"].user,
            author=obj.author
        ).exists()

    def get_recipes(self, obj):
        recipes_limit = (
            self.context["request"].query_params.get("recipes_limit")
        )
        queryset = (
            obj.author.recipes.all()[:int(recipes_limit)] if recipes_limit
            else obj.author.recipes.all()
        )
        return BriefInfoSerializer(queryset, many=True).data


class RecipeCreateSerializer(serializers.ModelSerializer):
    pass


class RecipeReadSerializer():
    author = UserSerializerCustom(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = "__all__"

    def to_representation(self, instance):
        return BriefInfoSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data    
