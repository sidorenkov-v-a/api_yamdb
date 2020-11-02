from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user and
            request.user.is_authenticated and
            request.user == obj.author
        )


class IsModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user and
            request.user.is_authenticated and
            request.user.is_moderator()
        )


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user and
            request.user.is_authenticated and
            request.user.is_admin()
        )
