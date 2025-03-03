from furniture.models import (DoorPlacement, FurniturePlacement,
                              PowerSocketPlacement, RoomLayout,
                              WindowPlacement)
from layout_algorithm import core


def create_room_layout(validated_data):
    room_placement = validated_data.pop("placements")
    selected_furniture = validated_data.pop("selected_furniture")
    doors = validated_data.pop("doors")
    windows = validated_data.pop("windows")
    power_sockets = validated_data.pop("powersockets")
    room = RoomLayout.objects.create(**validated_data)

    furniture_placement = []
    for placement in room_placement:
        furniture = placement["furniture"]
        coordinates = create_by_coordinate(placement)
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
        coordinates = create_by_coordinate(door)
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
        coordinates = create_by_coordinate(window)
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
        coordinates = create_by_coordinate(powersocket)
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

    return room


def create_by_coordinate(placement):
    """Создать и вернуть координаты для элемента (мебель, окно, ...)"""
    return
