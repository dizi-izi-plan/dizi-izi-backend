from djoser.serializers import UserCreateSerializer
from furniture.models import Door, Furniture, Placement, PowerSocket, Room, User, Window
from rest_framework import serializers


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

    user = UserCreateSerializer(read_only=True)
    furniture_placement = PlacementSerializer(many=True, source='placements')
    selected_furniture = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Furniture.objects.all(),
        write_only=True,
        allow_empty=True,
    )
    power_sockets = PowerSocketSerializer(
        many=True,
        # read_only=True,
        source='powersockets',
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
            'user',
        )
        model = Room
        read_only = ('id',)

    @staticmethod
    def _get_basic_parameters(
        validated_data_dictionary: dict, model: Room = Room
    ) -> dict[str, str]:
        return {
            'nw_coordinate': validated_data_dictionary['nw_coordinate'],
            'ne_coordinate': validated_data_dictionary['ne_coordinate'],
            'sw_coordinate': validated_data_dictionary['sw_coordinate'],
            'se_coordinate': validated_data_dictionary['se_coordinate'],
            'room': model,
        }

    def create(self, validated_data):
        """Создание помещения с расстановкой."""
        room_placement = validated_data.pop('placements')
        selected_furniture = validated_data.pop('selected_furniture')
        doors = validated_data.pop('doors')
        windows = validated_data.pop('windows')
        power_sockets = validated_data.pop('powersockets')
        room = Room.objects.create(**validated_data)

        furniture_placement = []
        for placement in room_placement:
            furniture = placement['furniture']
            furniture_placement.append(
                Placement(
                    furniture=furniture,
                    **self._get_basic_parameters(placement)
                ),
            )
        Placement.objects.bulk_create(furniture_placement)

        room_doors = []
        for door in doors:
            room_doors.append(
                Door(
                    width=door['width'],
                    open_inside=door['open_inside'],
                    **self._get_basic_parameters(door)
                ),
            )
        Door.objects.bulk_create(room_doors)

        room_windows = []
        for window in windows:
            room_windows.append(
                Window(
                    width=window['width'],
                    length=window['length'],
                    **self._get_basic_parameters(window)
                ),
            )
        Window.objects.bulk_create(room_windows)

        room_powersocket = []
        for powersocket in power_sockets:
            room_powersocket.append(
                PowerSocket(**self._get_basic_parameters(powersocket)),
            )
        PowerSocket.objects.bulk_create(room_powersocket)

        furniture_placement = []
        for furniture in selected_furniture:
            # здесь применение алгоритма по расстановке мебели
            pass

        return room

    def save(self, **kwargs):
        print(kwargs, self.validated_data)
        if not kwargs.get('user'):
            room = self.validated_data
            selected_furniture = room.pop('selected_furniture')
            # for furniture in selected_furniture:
            #     # здесь применение алгоритма по расстановке мебели
            #     one_furniture_placement = {}
            #     one_furniture_placement['furniture']=furniture
            #     one_furniture_placement['nw_coordinate']=12
            #     one_furniture_placement['ne_coordinate']=13
            #     one_furniture_placement['sw_coordinate']=14
            #     one_furniture_placement['se_coordinate']=15
            #     room['placements'].append(one_furniture_placement)
            self.instance = room
        else:
            self.instance = super().save(**kwargs)
        return self.instance


class RoomCopySerializer(serializers.ModelSerializer):
    furniture_placement = PlacementSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            'id',
            'user',
            'name',
            'created',
            'first_wall',
            'second_wall',
            'third_wall',
            'fourth_wall',
            'furniture_placement',
        ]
