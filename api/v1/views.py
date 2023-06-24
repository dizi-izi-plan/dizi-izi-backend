from django.forms import model_to_dict

from furniture.models import Door, Furniture, Placement, Room, Window
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (  # ProjectWriteSerializer
    FurnitureSerializer,
    RoomCopySerializer,
    RoomSerializer,
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
        if self.request.user.is_authenticated:
            return self.request.user.rooms.all()

    def perform_create(self, serializer):
        """Назначение данных для обработки запроса."""

        if self.request.user.is_authenticated:
            serializer.save(
                user=self.request.user,
                name=(
                    f'Проект'
                    f'{Room.objects.filter(user=self.request.user).count()}'
                ),
            )


class RoomCopyView(APIView):
    """
    Создаем копию объекта `Room` по пустому пост запросу на url
    /api/v1/rooms/pk.
    """

    def get(self, request, pk):
        orig_room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(orig_room)
        return Response(serializer.data)

    def post(self, request, pk):
        orig_room = get_object_or_404(Room, pk=pk)
        new_room = orig_room.copy(request)
        new_room.save()
        serializer = RoomSerializer(new_room)
        furniture = Furniture.objects.filter(
            room=orig_room
        )

        for furn in furniture:
            Placement.objects.create(
                room=new_room,
                furniture=furn,
                nw_coordinate=Placement.objects.get(
                    furniture=furn, room=orig_room
                ).nw_coordinate,
                ne_coordinate=Placement.objects.get(
                    furniture=furn, room=orig_room
                ).ne_coordinate,
                sw_coordinate=Placement.objects.get(
                    furniture=furn, room=orig_room
                ).sw_coordinate,
                se_coordinate=Placement.objects.get(
                    furniture=furn, room=orig_room
                ).se_coordinate,
            )

        for door in Door.objects.filter(room=orig_room):
            door.room = new_room
            door.save()

        for window in Window.objects.filter(room=orig_room):
            window.room = new_room
            window.save()

        return Response(serializer.data)
