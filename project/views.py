from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAuthor
from project.models import Project
from project.serializers import ProjectSerializer, ProjectUpdateSerializer


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.action == "partial_update":
            return ProjectUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if set(request.data.keys()) - {"name"}:
            return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)
