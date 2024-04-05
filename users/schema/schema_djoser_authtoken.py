from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status

from users.schema.base_extension import BaseExtension
from djoser.views import TokenCreateView, TokenDestroyView


class GenerateSwaggerDocForDjoserAuthtokenLogin(BaseExtension):
    """Этот класс предназначен для генерации документации Swagger для эндпоинтов Djoser Authtoken Login."""
    djoser_serializers = BaseExtension.djoser_serializers  # Переопределяем для сокращения кода.
    target_class = TokenCreateView
    endpoints_doc = {
        "post": extend_schema(
            summary="Аутентификация пользователя",
            description="Принимает учетные данные пользователя и возвращает токен аутентификации, если данные верны.",
            request=djoser_serializers.token_create,
            responses={
                status.HTTP_200_OK: djoser_serializers.token,
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Error: Bad Request")
                },
        )
    }


class GenerateSwaggerDocForDjoserAuthtokenLogout(BaseExtension):
    """Этот класс предназначен для генерации документации Swagger для эндпоинтов Djoser Authtoken Logout."""
    target_class = TokenDestroyView
    endpoints_doc = {
        "post": extend_schema(
            summary="Выход пользователя",
            description="Удаляет токен аутентификации пользователя из системы, осуществляя выход.",
            responses={
                status.HTTP_204_NO_CONTENT: OpenApiResponse(description="No response body"),
                status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Error: Unauthorized"),
            }
        )
    }
