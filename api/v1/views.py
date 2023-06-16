from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework import views, viewsets

from furniture.logging.logger import logger
from furniture.models import Furniture, Project, Room

from .serializers import (FurnitureSerializer, ProjectReadSerializer,
                          RoomSerializer, ProjectWriteSerializer)


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

            return Room.objects.filter(project__user=self.request.user)

    # def perform_create(self, serializer):
    #     """Назначение данных для обработки запроса."""
    #     print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     user = None
    #     if not self.request.user.is_anonymous:
    #         user = self.request.user
    #     serializer.save(user=user)


class ProjectListViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    def get_queryset(self) -> QuerySet[Project]:
        """Получает `queryset` в соответствии с параметрами запроса.

        Returns:
            `QuerySet`: Список запрошенных объектов.

        """
        queryset = self.queryset
        print(queryset, '!!!!!!!!!!!!!!!!!!!!!!!!!!')
        queryset = queryset.filter(user=self.request.user)
        print(queryset,'!!!!!!!!!!!!!!!!!!!!!!!!!!')
        if self.request.user.is_authenticated:
            logger.debug(queryset)
            return queryset

    def get_serializer_class(
        self,
    ) -> [ProjectReadSerializer | ProjectWriteSerializer]:
        """Выбор сериализатора в зависимости от вида запроса.

        Returns:
            Выбранный сериализатор.

        """
        if self.action in (
            'list',
            'retrieve',
        ):
            return ProjectReadSerializer
        print('PProjectWriteSerializer')
        return ProjectWriteSerializer
    #
    # @staticmethod
    # def quantity_of_projects(request: HttpRequest) -> int:
    #     return Project.objects.filter(user=request.user).count()

    def perform_create(self, serializer: ProjectWriteSerializer):
        """Назначение данных для обработки запроса."""

        if self.request.user.is_authenticated:
            print(serializer)

            # serializer.save(
            #     user=self.request.user,
            #     name=f'Проект{Project.objects.filter(user=self.request.user).count()}',
            #
            # )
            serializer.save()
        print('endsdfasdfasdfasdhfhasdfjkashdfajlsdfsdfasdfasdfasdhfhasdfjkashdfajlsdf')
