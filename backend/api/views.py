from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import action
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status

from users.models import Subscription, User
from api.serializers import (
    UserSerializerCustom,
    TagSerializer,
    IngredientSerializer,
    SubscriptionSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer
)
from recipes.models import Tag, Ingredient, Recipe
from api.pagination import CustomPaginLimitOnPage


class UserViewSetCustom(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerCustom
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPaginLimitOnPage

    @action(detail=True, methods=("post", "delete",))
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == "POST":
            subscribe = Subscription.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(
                subscribe, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            subscription = get_object_or_404(
                Subscription,
                user=user,
                author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=("get",))
    def subscriptions(self, request):
        user = request.user
        queryset = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(
            queryset,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    pagination_class = CustomPaginLimitOnPage

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    pass
