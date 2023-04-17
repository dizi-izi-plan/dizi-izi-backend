from rest_framework import serializers
from .models import Furniture


class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = ['name', 'width', 'lenght', 'x_coordinate', 'y_coordinate']
