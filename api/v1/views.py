from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from furniture.models import Furniture
from info.models import Tariff, UsersTariffs
from .filters import FurnitureFilter
from .serializers import (
    FurnitureSerializer,
    RoomSerializer,
    RoomAnonymousSerializers, TariffSerializer, ChangeTariffSerializer
)


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
        return self.request.user.rooms.all()

    def perform_create(self, serializer):
        if not self.request.user.is_anonymous:
            serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    def get_serializer_class(self):
        if not self.request.user.is_anonymous:
            return RoomSerializer
        return RoomAnonymousSerializers


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
