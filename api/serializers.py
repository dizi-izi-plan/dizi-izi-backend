from rest_framework import serializers

from furniture.models import Furniture, Room, Placement


class FurnitureSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""

    class Meta:
        fields = (
            'name',
            'name_english',
            'length',
            'width',
        )
        model = Furniture


class PlacementSerializer(serializers.ModelSerializer):
    """Сериализатор для размещения мебели в комнате."""
    furniture = serializers.StringRelatedField(
        source='furniture.name'
    )

    class Meta:
        fields = (
            'furniture',
            'x_coordinate',
            'y_coordinate',
        )
        model = Placement


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""
    furniture_placement = PlacementSerializer(
        many=True,
        read_only=True,
        source='room_placement'
    )

    class Meta:
        fields = (
            'name',
            'length',
            'width',
            'furniture_placement'
        )
        model = Room
