from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, CurrentUserDefault

from project.models import Project


class ProjectSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Project
        fields = "__all__"
