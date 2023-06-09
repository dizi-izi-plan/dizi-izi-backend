from rest_framework import viewsets, views
from furniture.models import Furniture
from .serializers import (
    FurnitureSerializer,
    RoomSerializer
)


class FurnitureViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных о мебели."""
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

class RoomViewSet(viewsets.ModelViewSet):
    """Получение и изменение помещения."""
    serializer_class = RoomSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        """Получение данных о помещении только пользователя запроса."""
        if not self.request.user.is_anonymous:
            return self.request.user.rooms.all()

    def perform_create(self, serializer):
        """Назначение данных для обработки запроса."""
        user=None
        if not self.request.user.is_anonymous:
            user=self.request.user
        serializer.save(user=user)
