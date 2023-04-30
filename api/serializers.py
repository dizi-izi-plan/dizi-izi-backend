from rest_framework import serializers
from django.db import transaction
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
        source='room_placement'
    )
    selected_furniture = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Furniture.objects.all(),
        write_only=True,
        allow_empty=True
    )

    class Meta:
        fields = (
            'name',
            'length',
            'width',
            'furniture_placement',
            'selected_furniture'
        )
        model = Room

    @transaction.atomic
    def create(self, validated_data):
        """Создание комнаты с расстановкой."""
        room_placement = validated_data.pop('room_placement')
        selected_furniture = validated_data.pop('selected_furniture')
        room = super().create(validated_data)
        furniture_placement = []
        for placement in room_placement:
            furniture = placement['furniture']
            furniture_placement.append(
                Placement(
                    furniture=furniture,
                    x_coordinate=placement['x_coordinate'],
                    y_coordinate=placement['y_coordinate'],
                    room=room
                )
            )
        Placement.objects.bulk_create(furniture_placement)
        for selected_furniture_one in selected_furniture:
            # здесь применение алгоритма по расстановке мебели
            pass

        return room
