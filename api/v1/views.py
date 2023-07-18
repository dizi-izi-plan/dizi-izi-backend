from __future__ import annotations

from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from furniture.models import (Door, Furniture, Placement, PowerSocket, Room,
                              Window)
from info.models import Tariff, UsersTariffs
from .filters import FurnitureFilter
from .serializers import (
    FurnitureSerializer,
    RoomSerializer,
    TariffSerializer, ChangeTariffSerializer
)
from ..utils import send_pdf_file


class FurnitureViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных о мебели."""

    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FurnitureFilter


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
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        serializer.save(user=user)


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
            placement = Placement.objects.get(
                furniture=furn,
                room=orig_room,
            )
            Placement.objects.create(
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
                Door,
                Window,
                PowerSocket,
            ]
        ]

        return Response(serializer.data)

    def patch(self, request, pk):
        instance = get_object_or_404(Room, pk=pk)
        instance.name = request.data.get('name')
        instance.save()
        serializer = RoomSerializer(instance)
        return Response(serializer.data)


class SendPDFView(APIView):
    """Отправка pdf файла на почту"""

    parser_classes = (MultiPartParser,)

    def post(self, request, format='pdf'):
        print(request.FILES)
        up_file = request.FILES['file']
        subj = 'План размещения мебели'
        text = 'В приложении подготовленный план размещения мебели'
        email = request.user.email
        return send_pdf_file(subj, email, up_file, text)


class APITariff(ListAPIView):
    serializer_class = TariffSerializer

    def get_queryset(self):
        return Tariff.objects.annotate(
            is_active=Exists(
                UsersTariffs.objects.filter(
                    user=self.request.user,
                    tariff=OuterRef('pk')
                )
            )
        )


class APIChangeTariff(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        new_tariff = get_object_or_404(Tariff, pk=pk)
        user_tariff = get_object_or_404(UsersTariffs, user=request.user)
        serializer = ChangeTariffSerializer(
            user_tariff,
            data={'user': request.user.id, 'tariff': new_tariff.id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, tariff=new_tariff)
        return Response(status=status.HTTP_205_RESET_CONTENT)
