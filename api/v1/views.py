from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework import views, viewsets

from furniture.logging.logger import logger
from furniture.models import Furniture, Project, Room

from .serializers import (FurnitureSerializer, ProjectSerializer,
                          RoomSerializer,
                          # ProjectWriteSerializer
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

            return Room.objects.filter(projects__user=self.request.user)

    # def perform_create(self, serializer):
    #     """Назначение данных для обработки запроса."""
    #     print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     user = None
    #     if not self.request.user.is_anonymous:
    #         user = self.request.user
    #     serializer.save(user=user)


class ProjectListViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self) -> QuerySet[Project]:
        """Получает `queryset` в соответствии с параметрами запроса.

        Returns:
            `QuerySet`: Список запрошенных объектов.

        """
        queryset = self.queryset
        queryset = queryset.filter(user=self.request.user)
        if self.request.user.is_authenticated:
            return queryset

    def perform_create(self,
                       serializer:  ProjectSerializer
                       ):
        """Назначение данных для обработки запроса."""

        if self.request.user.is_authenticated:
            serializer.save(
                user=self.request.user,
                name=f'Проект{Project.objects.filter(user=self.request.user).count()}',
            )
