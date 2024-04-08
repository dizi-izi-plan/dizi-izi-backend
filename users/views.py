from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class UserViewSet(DjoserUserViewSet):
    """
    Расширяет Djoser UserViewSet для настройки троттлинга и аутентификации.

    Этот класс предназначен для тонкой настройки механизмов контроля частоты запросов (троттлинга) и аутентификации
    для пользовательских запросов в API. В основе его работы лежит расширение стандартного класса UserViewSet от Djoser.

    Примечание: В настоящий момент изменения не активированы для использования в проекте.
    """

    throttle_scope = 'low_request'
    authentication_classes = (TokenAuthentication,)

    def get_throttles(self):
        """
        Устанавливает классы троттлинга для действия создания пользователя "create".
        """
        if self.action == "create":
            self.throttle_classes = [AnonRateThrottle, UserRateThrottle]
        return super().get_throttles()
