from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()


class IsUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.role == User.Roles.User


class IsModeratorRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.role == User.Roles.MODERATOR


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.role == User.Roles.ADMIN
