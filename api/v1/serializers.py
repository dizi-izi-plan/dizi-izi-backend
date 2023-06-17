from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


from furniture.logging.logger import logger
from furniture.models import (Door, Furniture, Placement, PowerSocket, Project,
                              Room, Window, User)


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password')


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
            'se_coordinate',
        )
        model = Placement


class PowerSocketSerializer(serializers.ModelSerializer):
    """Сериализатор для размещения розеток в помещении."""

    class Meta:
        fields = (
            'nw_coordinate',
            'ne_coordinate',
            'sw_coordinate',
            'se_coordinate',
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
            'se_coordinate',
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
            'se_coordinate',
        )
        model = Window


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""

    furniture_placement = PlacementSerializer(many=True, source='placements')
    selected_furniture = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Furniture.objects.all(),
        write_only=True,
        allow_empty=True,
    )
    power_sockets = PowerSocketSerializer(
        many=True, read_only=True, source='powersockets'
    )
    doors = DoorSerializer(
        many=True,
    )
    windows = WindowSerializer(many=True)

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
            'windows',
        )
        model = Room
        read_only = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        """Создание помещения с расстановкой."""
        room_placement = validated_data.pop('placements')
        selected_furniture = validated_data.pop('selected_furniture')
        doors = validated_data.pop('doors')
        windows = validated_data.pop('windows')
        room = Room.objects.create(**validated_data)
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
                    room=room,
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
                    room=room,
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
                    room=room,
                )
            )
        Window.objects.bulk_create(room_windows)
        furniture_placement = []
        for furniture in selected_furniture:
            # здесь применение алгоритма по расстановке мебели
            pass

        return room

    # def save(self, **kwargs):
    #     print(kwargs, self.validated_data)
    #     if not kwargs['user']:
    #         room = self.validated_data
    #         selected_furniture = room.pop('selected_furniture')
    #         # for furniture in selected_furniture:
    #         #     # здесь применение алгоритма по расстановке мебели
    #         #     one_furniture_placement = {}
    #         #     one_furniture_placement['furniture']=furniture
    #         #     one_furniture_placement['nw_coordinate']=12
    #         #     one_furniture_placement['ne_coordinate']=13
    #         #     one_furniture_placement['sw_coordinate']=14
    #         #     one_furniture_placement['se_coordinate']=15
    #         #     room['placements'].append(one_furniture_placement)
    #         self.instance = room
    #     else:
    #         self.instance = super().save(**kwargs)
    #     return self.instance


class ProjectReadSerializer(WritableNestedModelSerializer):
    room = RoomSerializer(
        many=True,
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'room',
            'created',
        )


# class ProjectWriteSerializer(WritableNestedModelSerializer):
#     room = RoomSerializer(
#         many=True,
#         # allow_empty=True,
#     )
#
#     class Meta:
#         model = Project
#         fields = (
#             'name',
#             'room',
#         )

    # @transaction.atomic
    # def create(self, validated_data):
    #     logger.debug(validated_data)
    #     # name = validated_data.pop('name')
    #     rooms = validated_data.pop('room')
    #     project = Project.objects.create(**validated_data)
    #     # project.name.set(name)
    #     print( '//////////////////////')
    #
    #     for room in rooms:
    #         room_list.append
    #     return project
    #
    # def to_representation(self, instance):
    #     request = self.context.get('request')
    #     context = {'request': request}
    #     return ProjectReadSerializer(instance, context=context).data
