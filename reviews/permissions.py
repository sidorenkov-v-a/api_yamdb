from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import User


class IsAuthorOrModeratorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and request.user.role == User.Roles.MODERATOR:
            return True
        return (
            request.method in SAFE_METHODS or
            obj.author == request.user or
            request.user.role == User.Roles.Admin
        )
