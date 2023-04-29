from rest_framework import viewsets

from furniture.models import Furniture

from .serializers import FurnitureSerializer


class FurnitureViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение и изменение постов."""
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
