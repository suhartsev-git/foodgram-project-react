from django.urls import include, path
from rest_framework import routers

from .views import UserViewSetCustom, TagViewSet, IngredientViewSet


app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'users',
    UserViewSetCustom,
    basename='user'
)
router_v1.register(
    r'tags',
    TagViewSet,
    basename='tag'
)
router_v1.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredient'
)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
]
