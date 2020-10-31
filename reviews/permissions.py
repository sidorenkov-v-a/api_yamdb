from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrModeratorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and request.user.role in \
                ['moderator', 'admin']:
            return True
        if request.method == 'PATCH' and request.user.role in \
                ['admin']:
            return True
        return request.method in SAFE_METHODS or obj.author == request.user


# class IsAuthorOrModeratorOrAdmin(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method == 'DELETE' and request.user.is_moderator()
#             return True
#         return (
#             request.method in SAFE_METHODS or 
#             obj.author == request.user or
#             request.user.is_admin()
#         )
