from rest_framework import serializers

from furniture.models import Furniture


class FurnitureSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""

    class Meta:
        fields = '__all__'
        model = Furniture
