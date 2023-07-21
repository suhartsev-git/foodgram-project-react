from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import User, Subscription
from recipes.models import Tag, Ingredient


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