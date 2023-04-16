from rest_framework import generics
from .models import Furniture
from .serializers import FurnitureSerializer


class FurnitureViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
