from rest_framework import serializers

from furniture.models import Furniture, RoomType


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
            "name_eng",
            "depth",
            "width",
            "depth_with_access_zone",
            "width_with_access_zone",
            "type_of_rooms",
            "image"
        )
        model = Furniture
