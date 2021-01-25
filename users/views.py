from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdminRole
from .serializers import GetTokenSerializer, RegisterSerializer, UserSerializer

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


@api_view(('POST',))
@permission_classes((AllowAny,))
def get_user_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    confirmation_code = serializer.validated_data.get('confirmation_code')

    user = get_object_or_404(User, email=email)

    if token_generator.check_token(user, confirmation_code):
        return Response({'token': str(AccessToken.for_user(user))})

    return Response(
        {'confirmation_code': 'value is invalid'}, status=HTTP_400_BAD_REQUEST
    )


@api_view(('POST',))
@permission_classes((AllowAny,))
def register_user(request):

    def set_username(instance, username):
        instance.username = username
        instance.save()

    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')

    user, created = User.objects.get_or_create(email=email)
    confirmation_code = token_generator.make_token(user)

    if username:
        try:
            set_username(user, username)
        except IntegrityError:
            set_username(user, email)
    else:
        if created:
            set_username(user, email)

    send_mail(
        subject='confirmation code',
        message=f'Your confirmation code: {confirmation_code}',
        from_email=None,
        recipient_list=(email,),
        fail_silently=False,
    )
    return Response({'email': email, 'username': user.username})


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

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)

        return Response(serializer.data)
