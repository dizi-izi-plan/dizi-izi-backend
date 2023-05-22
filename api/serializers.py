from rest_framework import serializers
from django.db import transaction
from furniture.models import (
    Furniture,
    Room,
    Placement,
    PowerSocket,
    Door,
    Window
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
            'nw_coordinate',
            'ne_coordinate',
            'sw_coordinate',
            'se_coordinate'
        )
        model = Placement


class PowerSocketSerializer(serializers.ModelSerializer):
    """Сериализатор для размещения розеток в помещении."""

    class Meta:
        fields = (
            'nw_coordinate',
            'ne_coordinate',
            'sw_coordinate',
            'se_coordinate'
        )
        model = PowerSocket


class DoorSerializer(serializers.ModelSerializer):
    """Сериализатор для размещения розеток в помещении."""

    class Meta:
        fields = (
            'width',
            'open_inside',
            'nw_coordinate',
            'ne_coordinate',
            'sw_coordinate',
            'se_coordinate'
        )
        model = Door


class WindowSerializer(serializers.ModelSerializer):
    """Сериализатор для размещения окон в помещении."""

    class Meta:
        fields = (
            'length',
            'width',
            'nw_coordinate',
            'ne_coordinate',
            'sw_coordinate',
            'se_coordinate'
        )
        model = Window


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""
    furniture_placement = PlacementSerializer(
        many=True,
        source='placements'
    )
    selected_furniture = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Furniture.objects.all(),
        write_only=True,
        allow_empty=True
    )
    power_sockets = PowerSocketSerializer(
        many=True,
        read_only=True,
        source='powersockets'
    )
    doors = DoorSerializer(
        many=True,
    )
    windows = WindowSerializer(
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'first_wall',
            'second_wall',
            'third_wall',
            'fourth_wall',
            'furniture_placement',
            'selected_furniture',
            'doors',
            'power_sockets',
            'windows'
        )
        model = Room
        read_only = ('id', )

    @transaction.atomic
    def create(self, validated_data):
        """Создание помещения с расстановкой."""
        room_placement = validated_data.pop('placements')
        selected_furniture = validated_data.pop('selected_furniture')
        doors = validated_data.pop('doors')
        windows = validated_data.pop('windows')
        room = super().create(validated_data)
        furniture_placement = []
        for placement in room_placement:
            furniture = placement['furniture']
            furniture_placement.append(
                Placement(
                    furniture=furniture,
                    nw_coordinate=placement['nw_coordinate'],
                    ne_coordinate=placement['ne_coordinate'],
                    sw_coordinate=placement['sw_coordinate'],
                    se_coordinate=placement['se_coordinate'],
                    room=room
                )
            )
        Placement.objects.bulk_create(furniture_placement)
        room_doors = []
        for door in doors:
            room_doors.append(
                Door(
                    width=door['width'],
                    open_inside=door['open_inside'],
                    nw_coordinate=door['nw_coordinate'],
                    ne_coordinate=door['ne_coordinate'],
                    sw_coordinate=door['sw_coordinate'],
                    se_coordinate=door['se_coordinate'],
                    room=room
                )
            )
        Door.objects.bulk_create(room_doors)
        room_windows = []
        for window in windows:
            room_windows.append(
                Window(
                    width=window['width'],
                    length=window['length'],
                    nw_coordinate=window['nw_coordinate'],
                    ne_coordinate=window['ne_coordinate'],
                    sw_coordinate=window['sw_coordinate'],
                    se_coordinate=window['se_coordinate'],
                    room=room
                )
            )
        Window.objects.bulk_create(room_windows)
        for selected_furniture_one in selected_furniture:
            # здесь применение алгоритма по расстановке мебели
            pass

        return room

    def save(self, **kwargs):
        # if 'user' not in kwargs:
        #     return self.create_anonymous(**kwargs)
        return super().save(**kwargs)


class RoomAnonymousSerializers(serializers.Serializer):
    """Сериализатор для анонимного пользователя."""
    min_value_len_width = 1
    name = serializers.CharField(
        max_length=128,
        label='Название помещения',
    )
    first_wall = serializers.IntegerField(
        label='Длина 1 стены',
        help_text='Длина стены в мм',
        min_value=min_value_len_width
    )
    second_wall = serializers.IntegerField(
        label='Длина 2 стены',
        help_text='Длина стены в мм',
        min_value=min_value_len_width
    )
    third_wall = serializers.IntegerField(
        label='Длина 3 стены',
        help_text='Длина стены в мм',
        min_value=min_value_len_width
    )
    fourth_wall = serializers.IntegerField(
        label='Длина 4 стены',
        help_text='Длина стены в мм',
        min_value=min_value_len_width
    )
    furniture_placement = PlacementSerializer(
        many=True,
        # source='placements'
        # queryset=Placement.objects.all(),
    )
    selected_furniture = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Furniture.objects.all(),
        write_only=True,
        allow_empty=True
    )
    power_sockets = PowerSocketSerializer(
        many=True,
        read_only=True,
    )
    doors = DoorSerializer(
        many=True,
    )
    windows = WindowSerializer(
        many=True,
    )
    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        # room_placement = validated_data.pop('furniture_placement')
        # selected_furniture = validated_data.pop('selected_furniture')
        # doors = validated_data.pop('doors')
        # windows = validated_data.pop('windows')
        room = Room(**self.validated_data)
        return room
        # furniture_placement = []
        # for placement in room_placement:
        #     furniture = placement['furniture']
        #     furniture_placement.append(
        #         Placement(
        #             furniture=furniture,
        #             nw_coordinate=placement['nw_coordinate'],
        #             ne_coordinate=placement['ne_coordinate'],
        #             sw_coordinate=placement['sw_coordinate'],
        #             se_coordinate=placement['se_coordinate'],
        #             room=room
        #         )
        #     )
        # Placement.objects.bulk_create(furniture_placement)
        # room_doors = []
        # for door in doors:
        #     room_doors.append(
        #         Door(
        #             width=door['width'],
        #             open_inside=door['open_inside'],
        #             nw_coordinate=door['nw_coordinate'],
        #             ne_coordinate=door['ne_coordinate'],
        #             sw_coordinate=door['sw_coordinate'],
        #             se_coordinate=door['se_coordinate'],
        #             room=room
        #         )
        #     )
        # Door.objects.bulk_create(room_doors)
        # room_windows = []
        # for window in windows:
        #     room_windows.append(
        #         Window(
        #             width=window['width'],
        #             length=window['length'],
        #             nw_coordinate=window['nw_coordinate'],
        #             ne_coordinate=window['ne_coordinate'],
        #             sw_coordinate=window['sw_coordinate'],
        #             se_coordinate=window['se_coordinate'],
        #             room=room
        #         )
        #     )
        # Window.objects.bulk_create(room_windows)
        # for selected_furniture_one in selected_furniture:
        #     # здесь применение алгоритма по расстановке мебели
        #     pass

        # return room
