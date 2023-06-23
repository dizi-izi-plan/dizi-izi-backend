from furniture.models import Furniture
from rest_framework import viewsets

from .serializers import FurnitureSerializer  # ProjectWriteSerializer
from .serializers import RoomSerializer


class FurnitureViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных о мебели."""

    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """Получение и изменение помещения."""

    serializer_class = RoomSerializer

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        """Получение данных о помещении только пользователя запроса."""
        if self.request.user.is_authenticated:
            return self.request.user.rooms.all()

    def perform_create(self, serializer):
        """Назначение данных для обработки запроса."""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
