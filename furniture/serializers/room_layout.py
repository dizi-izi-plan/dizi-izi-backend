from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from furniture.models import Furniture, RoomLayout
from furniture.serializers import (DoorPlacementSerializer,
                                   FurniturePlacementSerializer,
                                   PowerSocketPlacementSerializer,
                                   WindowPlacementSerializer)
from furniture.services import create_room_layout

User = get_user_model()


class RoomLayoutSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""

    user = UserCreateSerializer(read_only=True)
    furniture_placement = FurniturePlacementSerializer(many=True, source="placements")
    selected_furniture = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Furniture.objects.all(),
        write_only=True,
        allow_empty=True,
    )
    power_sockets = PowerSocketPlacementSerializer(
        many=True,
        # read_only=True,
        source="powersockets",
    )
    doors = DoorPlacementSerializer(
        many=True,
    )
    windows = WindowPlacementSerializer(many=True)

    class Meta:
        fields = (
            "id",
            "name",
            "first_wall",
            "second_wall",
            "third_wall",
            "fourth_wall",
            "furniture_placement",
            "selected_furniture",
            "doors",
            "power_sockets",
            "windows",
            "user",
        )
        model = RoomLayout
        read_only = ("id",)

    @transaction.atomic
    def create(self, validated_data):
        """Создание помещения с расстановкой."""

        return create_room_layout(validated_data)


class RoomLayoutListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка планировок с ограниченным набором полей."""
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RoomLayout
        fields = (
            'id',
            'name', 
            'user',
            'first_wall',
            'second_wall',
            'third_wall',
            'fourth_wall',
        )


class RoomLayoutCopySerializer(serializers.ModelSerializer):
    furniture_placement = FurniturePlacementSerializer(many=True, read_only=True)

    class Meta:
        model = RoomLayout
        fields = [
            "id",
            "user",
            "name",
            "created",
            "first_wall",
            "second_wall",
            "third_wall",
            "fourth_wall",
            "furniture_placement",
        ]
