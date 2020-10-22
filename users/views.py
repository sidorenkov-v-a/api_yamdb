from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .confirmation_code import (
    confirmation_code_encrypt, confirmation_code_decrypt
)

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework.viewsets import ModelViewSet
from.serializers import UserSerializer

User = get_user_model()


class GetUserToken(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    def post(self, request):
        confirmation_code = request.data.get('confirmation_code')
        if not confirmation_code:
            return Response({'error': 'confirmation_code is required'})

        user_email = request.data.get('email')
        if not user_email:
            return Response({'error': 'email is required'})

        user = User.objects.filter(email=user_email).first()

        if not user:
            return Response({'error': 'email or confirmation_code is invalid'})

        # noinspection PyBroadException
        try:
            decrypted_email = \
                confirmation_code_decrypt(confirmation_code).decode()
        except:
            return Response({'error': 'email or confirmation_code is invalid'})

        if user_email == decrypted_email:
            return Response(self.get_tokens_for_user(user))


class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'email is required'})

        try:
            validate_email(email)
        except ValidationError:
            return Response({'email is invalid': 'input a valid email'})

        User.objects.get_or_create(email=email)

        confirmation_code = confirmation_code_encrypt(email.encode())
        return Response({'confirmation code': confirmation_code})


class UserViewSet(ModelViewSet):
    queryset = User.objects

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
