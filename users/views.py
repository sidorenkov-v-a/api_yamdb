from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .confirmation_code import (
    confirmation_code_encrypt, confirmation_code_decrypt
)

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer

from .permissions import IsUserRole, IsModeratorRole, IsAdminRole

from rest_framework.decorators import action


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
            return Response(
                {'error': 'email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError as e:
            return Response(
                {'detail': e.message}, status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.get_or_create(email=email)

        confirmation_code = confirmation_code_encrypt(email.encode())
        return Response({'confirmation code': confirmation_code})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'username'

    @action(
        detail=False, methods=['GET', 'PATCH'], name='Get Highlight',
        permission_classes=[IsAuthenticated], url_path='me'
    )
    def personal_user_page(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
