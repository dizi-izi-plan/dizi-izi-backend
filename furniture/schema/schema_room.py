from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status

from furniture import serializers, views
from furniture.schema.base_extension import BaseExtension


class GenerateSwaggerDocForRoomViewSet(BaseExtension):
    """Этот класс предназначен для генерации документации Swagger для эндпоинтов RoomViewSet."""
    serializer = serializers.RoomLayoutSerializer
    target_class = views.RoomViewSet
    endpoints_doc = {
        # GET /url/
        "list": extend_schema(
            summary="Получение cписка комнат",
            description="Получение списка комнат. Доступно всем пользователям.",
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=serializer,
                    description="Данные комнаты"
                ),
            }
        ),
        # POST /url/
        "create": extend_schema(
            summary="Создание комнаты",
            description="Создание новой комнаты. Доступно авторизованным пользователям.",
            responses={
                status.HTTP_201_CREATED: OpenApiResponse(
                    response=serializer,
                    description="Данные комнаты",
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Error: Bad Request"),
                status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Error: Unauthorized"),
            }
        ),
        # GET /url/{id}/
        "retrieve": extend_schema(
            summary="Получение комнаты по id",
            description="Получение информации о комнате по идентификатору.",
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=serializer,
                    description="Данные комнаты"
                ),
            }
        ),
        # PUT /url/{id}/
        "update": extend_schema(
            summary="Обновление комнаты",
            description="Обновление информации о комнате. Доступно владельцу комнаты.",
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=serializer,
                    description="Данные комнаты"
                ),
            }
        ),
        # PATCH /url/{id}/
        "partial_update": extend_schema(
            summary="Частичное обновление комнаты",
            description="Частичное обновление комнаты.",
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=serializer,
                    description="Данные комнаты"
                ),
            }
        ),
        # DELETE /users/{id}/
        "destroy": extend_schema(
            summary="Удаление комнаты",
            description="Удаление существующей комнаты. Доступно владельцу комнаты.",
            responses={
                status.HTTP_204_NO_CONTENT: OpenApiResponse(description="No response body"),
                status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Error: Unauthorized"),
                status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Error: Forbidden"),
            }
        ),
    }
