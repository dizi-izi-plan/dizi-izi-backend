from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status

from furniture import serializers, views
from furniture.schema.base_extension import BaseExtension


class GenerateSwaggerDocForFurnitureViewSet(BaseExtension):
    """Этот класс предназначен для генерации документации Swagger для эндпоинтов FurnitureViewSet."""
    serializer = serializers.FurnitureSerializer
    target_class = views.FurnitureViewSet

    endpoints_doc = {
        # GET /url/
        "list": extend_schema(
            summary="Получение данных о мебели",
            description="Возвращает данные мебели. Для администратора возвращает список всех пользователей",
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=serializer,
                    description="Данные мебели"
                ),
                status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Error: Unauthorized"),
            }
        ),
        # GET /url/{id}/
        "retrieve": extend_schema(
            summary="Получение данных о мебели по id",
            description="Возвращает данные мебели по её уникальному идентификатору. ",
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=serializer,
                    description="Данные мебели"
                ),
                status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Error: Unauthorized"),
            }
        ),
    }
