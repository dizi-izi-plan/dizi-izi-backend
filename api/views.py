from rest_framework import viewsets
from furniture.models import Furniture
from .serializers import (
    FurnitureSerializer,
    RoomSerializer,
    RoomAnonymousSerializers
)


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
        return self.request.user.rooms.all()

    def perform_create(self, serializer):
        if not self.request.user.is_anonymous:
            serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if not self.request.user.is_anonymous:
            return RoomSerializer
        return RoomAnonymousSerializers
