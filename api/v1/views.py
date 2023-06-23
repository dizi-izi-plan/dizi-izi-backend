from furniture.models import Furniture, Room
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

    # def get_queryset(self):
    #     """Получение данных о помещении только пользователя запроса."""
    #     if self.request.user.is_authenticated:
    #         return Room.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     """Назначение данных для обработки запроса."""
    #     if self.request.user.is_authenticated:
    #         serializer.save(user=self.request.user)

    def get_queryset(self):
        """Получение данных о помещении только пользователя запроса."""
        if not self.request.user.is_anonymous:
            return self.request.user.rooms.all()

    def perform_create(self, serializer):
        """Назначение данных для обработки запроса."""
        user = None
        if not self.request.user.is_anonymous:
            user = self.request.user
            print(user)
        serializer.save(user=user)
