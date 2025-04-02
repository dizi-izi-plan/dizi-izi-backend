from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


UnauthorizedErrorResponse = OpenApiResponse(
    description="Unauthorized",
    response=ErrorSerializer,
    examples=[
        OpenApiExample(
            name="Unauthorized Error",
            value={
                "detail": "Учетные данные не были предоставлены."
            }
        )
    ]
)

ForbiddenErrorResponse = OpenApiResponse(
    description="Forbidden",
    response=ErrorSerializer,
    examples=[
        OpenApiExample(
            name='Forbidden Error',
            value={
                "detail": "У вас недостаточно прав для выполнения данного действия."
            }
        )
    ]
)
