from django.db.models import QuerySet, Exists, OuterRef
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsSuperUserOrReadOnly
from tariff.models import Tariff, UsersTariffs
from tariff.serializers import TariffSerializer, ChangeTariffSerializer


class APITariff(ListAPIView, CreateAPIView):
    """Список тарифов.

    Просмотр доступен для всех. Редактирование только для суперпользователя.
    """

    serializer_class = TariffSerializer
    permission_classes = (IsSuperUserOrReadOnly,)

    def get_queryset(self) -> QuerySet:
        """Получение `queryset`а тарифов.

        Текущий пользователь видит, какой тариф у него активен. Другие тарифы
        маркируются, как неактивные. Для незарегистрированного пользователя
        возвращаются все тарифы.

        Returns:
            Queryset: queryset с тарифами.
        """
        if self.request.user.is_authenticated:
            return Tariff.objects.annotate(
                is_active=Exists(
                    UsersTariffs.objects.filter(
                        user=self.request.user, tariff=OuterRef("pk"),
                    ),
                ),
            )
        return Tariff.objects.all()


class APIChangeTariff(APIView):
    """Изменяем тариф."""

    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request: HttpRequest, name_english: str) -> Response:
        """Добавляем тариф пользователю."""
        new_tariff = get_object_or_404(Tariff, name_english=name_english)
        user_tariff = get_object_or_404(UsersTariffs, user=request.user)
        serializer = ChangeTariffSerializer(
            user_tariff,
            data={"user": request.user.id, "tariff": new_tariff.id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, tariff=new_tariff)
        return Response(
            status=status.HTTP_205_RESET_CONTENT,
            data={"message": "Тариф изменен"},
        )
