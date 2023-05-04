from rest_framework import serializers
from django.db import transaction
from furniture.models import (
    Furniture,
    Room,
    Placement,
    PowerSocket,
    Door
)


class FurnitureSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""

    class Meta:
        fields = (
            'id',
            'name',
            'name_english',
            'length',
            'width',
            'length_access',
            'width_access',
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


class PowerSocketSerializer(serializers.ModelSerializer):
    """Сериализатор для размещения розеток в комнате."""

    class Meta:
        fields = (
            'x_coordinate',
            'y_coordinate',
        )
        model = PowerSocket


class DoorSerializer(serializers.ModelSerializer):
    """Сериализатор для размещения розеток в комнате."""

    class Meta:
        fields = (
            'width',
            'open_inside',
            'x_coordinate',
            'y_coordinate',
        )
        model = Door


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
    power_sockets = PowerSocketSerializer(
        many=True,
        read_only=True
    )
    doors = DoorSerializer(
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'length',
            'width',
            'furniture_placement',
            'selected_furniture',
            'doors',
            'power_sockets'
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
