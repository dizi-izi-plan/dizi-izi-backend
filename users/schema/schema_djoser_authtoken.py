from drf_spectacular.utils import extend_schema

from users.schema.base_extension import BaseExtension
from djoser.views import TokenCreateView, TokenDestroyView


class GenerateSwaggerDocForDjoserAuthtokenLogin(BaseExtension):
    """Этот класс предназначен для генерации документации Swagger для эндпоинтов Djoser Authtoken Login."""
    target_class = TokenCreateView
    endpoints_doc = {
        "post": extend_schema(
            summary="Аутентификация пользователя",
            description="Принимает учетные данные пользователя и возвращает токен аутентификации, если данные верны.",
        )
    }


class GenerateSwaggerDocForDjoserAuthtokenLogout(BaseExtension):
    """Этот класс предназначен для генерации документации Swagger для эндпоинтов Djoser Authtoken Logout."""
    target_class = TokenDestroyView
    endpoints_doc = {
        "post": extend_schema(
            summary="Выход пользователя",
            description="Удаляет токен аутентификации пользователя из системы, осуществляя выход.",
        )
    }
