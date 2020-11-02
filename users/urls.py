from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_user_token, register_user

v1_router = DefaultRouter()

v1_router.register(
    'users',
    UserViewSet,
    basename='Users'
)

auth_urls = [
    path('token/', get_user_token, name='get_user_token'),
    path('email/', register_user, name='register_user'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(v1_router.urls)),
]
