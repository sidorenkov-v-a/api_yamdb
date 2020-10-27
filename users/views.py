from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import ValidationError as EmailError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .confirmation_code import (confirmation_code_decrypt,
                                confirmation_code_encrypt)
from .permissions import IsAdminRole
from .serializers import UserSerializer

# from django.core.validators import ValidationError as EmailError

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
        if 'email' not in request.data:
            raise ValidationError(['email field is required.'])

        if 'confirmation_code' not in request.data:
            raise ValidationError(['confirmation_code field is required.'])

        user_email = request.data['email']
        try:
            validate_email(user_email)
        except EmailError as e:
            raise ValidationError(e.message)

        confirmation_code = request.data['confirmation_code']
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
        if 'email' not in request.data:
            raise ValidationError(['email field is required.'])
        email = request.data['email']
        try:
            validate_email(email)
        except EmailError as e:
            raise ValidationError(e.message)

        confirmation_code = confirmation_code_encrypt(email.encode()).decode()
        User.objects.get_or_create(email=email)
        send_mail(
            'confirmation code',
            f'Your confirmation code: {confirmation_code}',
            'yamdb@fake.com',
            [email],
            fail_silently=False,
        )
        return Response({'confirmation code': confirmation_code})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'username'

    @action(
        detail=False, methods=['GET', 'PATCH'], name='personal_user_page',
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
