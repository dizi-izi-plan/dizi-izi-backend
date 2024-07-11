from django.contrib.auth import user_logged_out
from djoser.conf import settings

from users.models import CustomUser


def logout_user(user: CustomUser):
    """
    Кастомный logout для user

    Функция удаляет связанный с пользователем токен.
    Отправляет сигнал user_logged_out, для уведомления других частей приложения.
    Завершает все сессии пользователя.
    """
    if settings.TOKEN_MODEL:
        settings.TOKEN_MODEL.objects.filter(user=user).delete()
        user_logged_out.send(sender=user.__class__, user=user)

    if settings.CREATE_SESSION_ON_LOGIN:
        user.session_set.all().delete()
