from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from project.models import Project
from project.serializers import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
