from django.urls import include, path
from rest_framework import routers

from .views import UserViewSetCustom


app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'users',
    UserViewSetCustom,
    basename='user'
)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
]
