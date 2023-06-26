from django.forms import model_to_dict
from django.http import HttpRequest

from furniture.models import Door, Furniture, Placement, PowerSocket, Room, Window
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
from ..utils import get_name


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
                name=get_name(self.request.user)
                )


class RoomCopyView(APIView):
    """
    Создаем копию объекта `Room` по произвольному пост запросу на url
    /api/v1/rooms/pk/.
    """

    @staticmethod
    def _copy_object(
        model: [Door | Window | PowerSocket],
        orig_room: Room,
        new_room: Room,
    ):
        models = model.objects.filter(room=orig_room)
        for model in models:
            model.pk = None
            model.room = new_room
            model.save()

    def get(self, request, pk):
        orig_room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(orig_room)
        return Response(serializer.data)

    def post(self, request, pk):
        orig_room = get_object_or_404(Room, pk=pk)
        new_room = orig_room.copy(request)
        new_room.save()
        serializer = RoomSerializer(new_room)
        furniture = Furniture.objects.filter(room=orig_room)

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

        [
            self._copy_object(obj, orig_room, new_room)
            for obj in [
                Door,
                Window,
                PowerSocket,
            ]
        ]

        return Response(serializer.data)
