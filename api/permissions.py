import datetime

from django.contrib.auth import get_user_model
from rest_framework import permissions
from users.models import CustomUser


User = get_user_model()


class CustumPer(permissions.BasePermission):
    """Разрешает доступ только с правами администратора или для чтения."""

    def has_permission(
        self,
        request,
        view,
    ):
        if request.user.is_anonymous:
            return False
        return request.user.is_admin

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        """Return `True` if permission is granted, `False` otherwise."""
        return False


class ReviewCommentPermission(permissions.BasePermission):
    """Права доступа.

    Разрешает доступ для чтения или для редактирования пользователям
    с правами администратора, модератора или автора.
    """

    def has_permission(
        self,
        request,
        view,
    ):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.username == obj.author.username
        )


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """Разрешает доступ для изменения тарифа только администратору.

    Смотреть может любой пользователь.
    """

    def has_permission(
        self,
        request,
        view,
    ):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_admin
        )


class IsTariffAccepted(permissions.BasePermission):
    """Разрешает доступ клиенту, если его тариф это позволяет."""

    message = "Ваш тариф не позволяет больше создавать комнаты."

    @staticmethod
    def is_outdated(
        user: CustomUser,
    ):
        """Проверка на `просроченность` тарифа по времени."""
        return user.user_tariff.tariff.period < (
            datetime.datetime.now(datetime.timezone.utc)
            - user.user_tariff.start_date
        )

    @staticmethod
    def is_rooms_limit_exceeded(
        user: User,
    ):
        """Проверка на превышение лимита комнат."""
        return user.rooms.count() > user.user_tariff.tariff.rooms_limit

    def has_permission(
        self,
        request,
        view,
    ):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_authenticated:
            if self.is_outdated(user) or self.is_rooms_limit_exceeded(user):
                return False
            return True
