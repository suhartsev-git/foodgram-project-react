from djoser.views import UserViewSet
from rest_framework import viewsets

from users.models import Subscription, User
from api.serializers import UserSerializerCustom, TagSerializer, IngredientSerializer
from recipes.models import Tag, Ingredient


class UserViewSetCustom(UserViewSet):
    queryset = User.objects.all()
    pass


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
