from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework import views, viewsets

from furniture.models import Furniture, Project, Room

from .serializers import (FurnitureSerializer, ProjectListSerializer,
                          RoomSerializer)


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
            print(Room.objects.filter(project__user=self.request.user), '222222222')
            return Room.objects.filter(project__user=self.request.user)

    # def perform_create(self, serializer):
    #     """Назначение данных для обработки запроса."""
    #     print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     user = None
    #     if not self.request.user.is_anonymous:
    #         user = self.request.user
    #     serializer.save(user=user)


class ProjectListViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('user')
    serializer_class = ProjectListSerializer

    def get_queryset(self) -> QuerySet[Project]:
        """Получает `queryset` в соответствии с параметрами запроса.

        Returns:
            `QuerySet`: Список запрошенных объектов.

        """
        queryset = self.queryset

        # author = self.queryset.values_list('user')
        # print(author)
        # if author:
        queryset = queryset.filter(user=self.request.user)
        print(queryset)
        if self.request.user.is_anonymous:
            return queryset

    #
    # @staticmethod
    # def quantity_of_projects(request: HttpRequest) -> int:
    #     return Project.objects.filter(user=request.user).count()

    def perform_create(self, serializer):
        """Назначение данных для обработки запроса."""
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print(serializer)
        if self.request.user.is_authenticated:
            serializer.save(
                user=self.request.user,
                name=f'Проект{Project.objects.filter(user=self.request.user).count()}',
            )
        print('end')
