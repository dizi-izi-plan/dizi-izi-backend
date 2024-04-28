from rest_framework import serializers

from furniture.models import Coordinate


class CoordinateSerializer(serializers.ModelSerializer):
    """Сериализатор для координат x, y."""

    class Meta:
        fields = (
            "x",
            "y",
        )
        model = Coordinate


class AbstractCoordinates(serializers.Serializer):
    """Абстрактная модель для координат в сериализаторах."""

    north_west = CoordinateSerializer()
    north_east = CoordinateSerializer()
    south_west = CoordinateSerializer()
    south_east = CoordinateSerializer()

    class Meta:
        abstract = True
