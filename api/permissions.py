from rest_framework import permissions


class CustumPer(permissions.BasePermission):
    """Разрешает доступ только с правами администратора или для чтения."""

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        # return (
        #     request.method in permissions.SAFE_METHODS or (
        #         request.user.is_authenticated and request.user.is_admin
        #     )
        # )

    def has_object_permission(self, request, view, obj):
        """Return `True` if permission is granted, `False` otherwise."""
        return False


class ReviewCommentPermission(permissions.BasePermission):
    """Разрешает доступ для чтения или для редактирования пользователям
    с правами администратора, модератора или автора.

    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.username == obj.author.username
        )
