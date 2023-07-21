rom djoser.views import UserViewSet

from users.models import Subscription, User
from api.serializers import UserSerializerCustom

class UserViewSetCustom(UserViewSet):
    queryset = User.objects.all()
