from django.urls import path, include
from .views import GetUserToken, UserRegister, UserViewSet
from rest_framework.routers import DefaultRouter


v1_router = DefaultRouter()

v1_router.register(
    'users',
    UserViewSet,
    basename='Users'
)

urlpatterns = [
    path('v1/auth/token/', GetUserToken.as_view(), name='get_user_token'),
    path('v1/auth/email/', UserRegister.as_view(), name='register_user'),
]

urlpatterns += [
    path('v1/', include(v1_router.urls)),
]