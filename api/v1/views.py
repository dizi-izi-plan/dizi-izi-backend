from furniture.models import Door, Furniture, Placement, PowerSocket, Room, Window
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils import get_name, send_pdf_file
from .serializers import FurnitureSerializer, RoomSerializer


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
        user = None
        if self.request.user.is_authenticated:
            user=self.request.user
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
    """Отправка pdf файла на почту."""

    parser_classes = (MultiPartParser, )

    def post(self, request, format='pdf'):
        print(request.FILES)
        up_file = request.FILES['file']
        subj = 'План размещения мебели'
        text = 'В приложении подготовленный план размещения мебели'
        email = request.user.email
        return send_pdf_file(subj, email, up_file, text)

