from djoser.views import UserViewSet
from rest_framework import viewsets

from users.models import Subscription, User
from api.serializers import UserSerializerCustom, TagSerializer
from recipes.models import Tag


class UserViewSetCustom(UserViewSet):
    queryset = User.objects.all()
    pass


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()