from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

from furniture.models import (
    Furniture,
    RoomLayout,
    FurniturePlacement,
    PowerSocketPlacement,
    DoorPlacement,
    WindowPlacement,
    RoomType,
    Coordinate,
)
from layout_algorithm import core

FIELDS_COORDINATE = (
    "north_west",
    "north_east",
    "south_west",
    "south_east",
)

User = get_user_model()


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ("name", "slug")


class FurnitureSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""

    type_of_rooms = RoomTypeSerializer()

    class Meta:
        fields = (
            "id",
            "name",
            "name_english",
            "length",
            "width",
            "length_access",
            "width_access",
            "type_of_rooms",
        )
        model = Furniture


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


class FurniturePlacementSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения мебели в комнате."""

    class Meta:
        fields = ("furniture",) + FIELDS_COORDINATE
        model = FurniturePlacement


class PowerSocketPlacementSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения розеток в помещении."""

    class Meta:
        fields = FIELDS_COORDINATE
        model = PowerSocketPlacement


class DoorPlacementSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения розеток в помещении."""

    class Meta:
        fields = (
            "width",
            "open_inside",
        ) + FIELDS_COORDINATE
        model = DoorPlacement


class WindowPlacementSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения окон в помещении."""

    class Meta:
        fields = (
            "length",
            "width",
        ) + FIELDS_COORDINATE
        model = WindowPlacement


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

        def _create_by_coordinate(placement):
            """Создать и вернуть координаты для элемента (мебель, окно, ...)"""
            return {
                "north_west": Coordinate.objects.create(
                    x=placement["north_west"]["x"],
                    y=placement["north_west"]["y"],
                ),
                "north_east": Coordinate.objects.create(
                    x=placement["north_east"]["x"],
                    y=placement["north_east"]["y"],
                ),
                "south_west": Coordinate.objects.create(
                    x=placement["south_west"]["x"],
                    y=placement["south_west"]["y"],
                ),
                "south_east": Coordinate.objects.create(
                    x=placement["south_east"]["x"],
                    y=placement["south_east"]["y"],
                ),
            }

        room_placement = validated_data.pop("placements")
        selected_furniture = validated_data.pop("selected_furniture")
        doors = validated_data.pop("doors")
        windows = validated_data.pop("windows")
        power_sockets = validated_data.pop("powersockets")
        room = RoomLayout.objects.create(**validated_data)

        furniture_placement = []
        for placement in room_placement:
            furniture = placement["furniture"]
            coordinates = _create_by_coordinate(placement)
            furniture_placement.append(
                FurniturePlacement(
                    furniture=furniture,
                    room=room,
                    **coordinates,
                ),
            )
        FurniturePlacement.objects.bulk_create(furniture_placement)

        room_doors = []
        for door in doors:
            coordinates = _create_by_coordinate(door)
            room_doors.append(
                DoorPlacement(
                    width=door["width"],
                    open_inside=door["open_inside"],
                    room=room,
                    **coordinates,
                ),
            )
        DoorPlacement.objects.bulk_create(room_doors)

        room_windows = []
        for window in windows:
            coordinates = _create_by_coordinate(window)
            room_windows.append(
                WindowPlacement(
                    width=window["width"],
                    length=window["length"],
                    room=room,
                    **coordinates,
                ),
            )
        WindowPlacement.objects.bulk_create(room_windows)

        room_powersocket = []
        for powersocket in power_sockets:
            coordinates = _create_by_coordinate(powersocket)
            room_powersocket.append(
                PowerSocketPlacement(
                    room=room,
                    **coordinates,
                ),
            )
        PowerSocketPlacement.objects.bulk_create(room_powersocket)

        furniture_placement = []
        if selected_furniture:
            doors_and_windows = []
            doors_and_windows.extend(doors)
            doors_and_windows.extend(windows)
            doors_and_windows.extend(room_placement)
            furniture = []
            for one_furniture in selected_furniture:
                furniture.append(
                    {
                        "name": one_furniture.name,
                        "length": one_furniture.length_access,
                        "width": one_furniture.width_access,
                        "power_socket_type": one_furniture.power_socket_type,
                        "first_power_socket_height": one_furniture.first_power_socket_height,
                        "first_power_socket_width": one_furniture.first_power_socket_width,
                        "second_power_socket_height": one_furniture.second_power_socket_height,
                        "second_power_socket_width": one_furniture.second_power_socket_width,
                    },
                )
            room_size = {
                "first_wall": room.first_wall,
                "second_wall": room.second_wall,
                "third_wall": room.third_wall,
                "fourth_wall": room.fourth_wall,
            }
            furniture_arrangement = core.Core()
            furniture_arrangement.algorithm_activation(
                doors_and_windows,
                furniture,
                room_size,
            )
        for furniture in selected_furniture:
            # здесь применение алгоритма по расстановке мебели
            pass
        return room


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
