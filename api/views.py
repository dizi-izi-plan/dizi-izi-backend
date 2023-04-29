from rest_framework import viewsets
from django.contrib.auth import get_user_model
from furniture.models import Furniture

from .serializers import FurnitureSerializer, RoomSerializer

User = get_user_model()


class FurnitureViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных о мебели."""
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение и изменение комнаты."""
    def get_queryset(self):
        """Получение данных о комнатах только пользователя запроса."""
        return self.request.user.rooms.all()

    serializer_class = RoomSerializer
