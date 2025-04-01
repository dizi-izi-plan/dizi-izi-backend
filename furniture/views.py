from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsTariffAccepted
from furniture.filters import FurnitureFilter
from furniture.models import (DoorPlacement, Furniture, FurniturePlacement,
                              PowerSocketPlacement, Room, RoomLayout, RoomType,
                              WindowPlacement)
from furniture.serializers import (FurnitureSerializer, RoomLayoutSerializer,
                                   RoomSerializer, RoomTypeSerializer)
from furniture.utils import send_pdf_file


class FurnitureViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных о мебели."""

    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FurnitureFilter


class RoomTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Get types of rooms"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List of user rooms",
        tags=["Rooms"]
    )
)
class RoomListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Returns a read-only list of rooms owned by the currently authenticated user."""

    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    """Получение и изменение планировки."""

    serializer_class = RoomLayoutSerializer

    permission_classes = (IsAuthenticated, IsTariffAccepted)

    def get_queryset(self):
        """Получение данных о помещении только пользователя запроса."""
        if self.request.user.is_authenticated:
            return self.request.user.rooms.all()
        return RoomLayout.objects.none()

    def perform_create(self, serializer):
        """Назначение данных для обработки запроса."""
        user = self.request.user
        serializer.save(user=user)


class RoomCopyView(APIView):
    """Создаем копию объекта `Room`.

    Выполняется по произвольному пост запросу на url /api/v1/rooms/pk/.
    """

    @staticmethod
    def _copy_object(
        model: [DoorPlacement | WindowPlacement | PowerSocketPlacement],
        orig_room: RoomLayout,
        new_room: RoomLayout,
    ):
        models = model.objects.filter(room=orig_room)
        for model in models:
            model.pk = None
            model.room = new_room
            model.save()

    def get(self, request, pk):
        """Получаем планировку с заданным `pk`."""
        orig_room = get_object_or_404(RoomLayout, pk=pk)
        serializer = RoomLayoutSerializer(orig_room)
        return Response(serializer.data)

    def post(self, request, pk):
        """Создаем копию планировки с заданным `pk`."""
        orig_room = get_object_or_404(RoomLayout, pk=pk)
        new_room = orig_room.copy(request)
        new_room.save()
        serializer = RoomLayoutSerializer(new_room)
        furniture = Furniture.objects.filter(room=orig_room)

        for furn in furniture:
            placement = FurniturePlacement.objects.get(
                furniture=furn,
                room=orig_room,
            )
            FurniturePlacement.objects.create(
                room=new_room,
                furniture=furn,
                nw_coordinate=placement.nw_coordinate,
                ne_coordinate=placement.ne_coordinate,
                sw_coordinate=placement.sw_coordinate,
                se_coordinate=placement.se_coordinate,
            )
        [
            self._copy_object(obj, orig_room, new_room)
            for obj in [
                DoorPlacement,
                WindowPlacement,
                PowerSocketPlacement,
            ]
        ]

        return Response(serializer.data)

    def patch(self, request, pk):
        """Изменяем планировку с заданным `pk`."""
        instance = get_object_or_404(RoomLayout, pk=pk)
        instance.name = request.data.get("name")
        instance.save()
        serializer = RoomLayoutSerializer(instance)
        return Response(serializer.data)


class SendPDFView(APIView):
    """Отправка pdf файла на почту."""
    parser_classes = (MultiPartParser,)
    permission_classes = (
        IsAuthenticated,
        IsTariffAccepted,
    )

    def post(self, request, format="pdf"):
        """Загружаем планировку в формате PDF."""
        up_file = request.FILES["file"]
        subj = "План размещения мебели"
        text = "В приложении подготовленный план размещения мебели"
        email = request.user.email
        return send_pdf_file(subj, email, up_file, text)
