from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import action
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status

from users.models import Subscription, User
from api.serializers import (
    UserSerializerCustom, TagSerializer, IngredientSerializer,
    SubscriptionSerializer
)
from recipes.models import Tag, Ingredient


class UserViewSetCustom(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerCustom
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def subscribe_error_response(
        errors, status_code=status.HTTP_400_BAD_REQUEST
    ):
        return Response({"errors": errors}, status=status_code)

    def is_subscribed(self, user, author):
        return Subscription.objects.filter(user=user, author=author).exists()

    @action(detail=True, methods=("post", "delete",))
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == "POST":
            if user == author:
                return self.subscribe_error_response(
                    "Вы не можете подписываться на самого себя"
                )
            if self.is_subscribed(user, author):
                return self.subscribe_error_response(
                    "Вы уже подписаны на данного пользователя"
                )
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
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
