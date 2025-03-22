from rest_framework import serializers

from furniture.models import (DoorPlacement, FurniturePlacement,
                              PowerSocketPlacement, WindowPlacement)
from furniture.serializers import AbstractCoordinates

FIELDS_COORDINATE = ()


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
            "open_direction",
        ) + FIELDS_COORDINATE
        model = DoorPlacement


class WindowPlacementSerializer(serializers.ModelSerializer, AbstractCoordinates):
    """Сериализатор для размещения окон в помещении."""

    class Meta:
        fields = (
            "height",
            "width",
        ) + FIELDS_COORDINATE
        model = WindowPlacement
