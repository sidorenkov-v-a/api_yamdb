from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetUserToken, UserRegister, UserViewSet

v1_router = DefaultRouter()

v1_router.register(
    'users',
    UserViewSet,
    basename='Users'
)

auth_urls = [
    path('token/', GetUserToken, name='get_user_token'),
    path('email/', UserRegister.as_view(), name='register_user'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
]

urlpatterns += [
    path('v1/', include(v1_router.urls)),
]
