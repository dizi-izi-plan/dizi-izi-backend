from rest_framework import viewsets
from django.contrib.auth import get_user_model
from furniture.models import Furniture, Room
from rest_framework import status
from rest_framework.response import Response
from .serializers import FurnitureSerializer, RoomSerializer
from .permissions import CustumPer

User = get_user_model()


class FurnitureViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных о мебели."""
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """Получение и изменение помещения."""
    serializer_class = RoomSerializer

    def get_queryset(self):
        """Получение данных о помещении только пользователя запроса."""
        if not self.request.user.is_anonymous:
            return self.request.user.rooms.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
