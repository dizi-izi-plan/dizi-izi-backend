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
    """Получение и изменение комнаты."""
    serializer_class = RoomSerializer
    # permission_classes = [CustumPer, ]
    def get_queryset(self):
        """Получение данных о комнатах только пользователя запроса."""
        return self.request.user.rooms.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
