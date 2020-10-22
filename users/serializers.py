from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(method_name='get_role')

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User

    def get_role(self, obj):
        return obj.get_role()
