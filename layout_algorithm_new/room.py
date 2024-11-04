from .utils import convert_coordinates_to_line


class Room:
    def __init__(self, room_size, doors_and_windows):
        self.room_size = room_size
        self.doors_and_windows = doors_and_windows
        self.walls_length = tuple(room_size.values())
        self.wall_perimetr = sum(self.walls_length)
        self.room_coordinates = self._calculate_room_coordinates()
        self.room_coordinates_tuple = tuple(self.room_coordinates.values())
        self.room_objects_coordinates = []
        self.sorted_points = []

        self._add_doors_and_windows_coordinates()
        self._calculate_doors_and_windows_middle_point()

    def _calculate_room_coordinates(self):
        return {
            "south_west": {"x": 0, "y": 0},
            "north_west": {"x": 0, "y": self.room_size["first_wall"]},
            "north_east": {
                "x": self.room_size["second_wall"],
                "y": self.room_size["first_wall"],
            },
            "south_east": {"x": self.room_size["second_wall"], "y": 0},
        }

    def _add_doors_and_windows_coordinates(self):
        for door_or_window in self.doors_and_windows:
            self.room_objects_coordinates.append(door_or_window)

    def _calculate_doors_and_windows_middle_point(self):
        for door_or_window in self.doors_and_windows:
            middle_point = {
                "x": (door_or_window["north_east"]["x"] + door_or_window["north_west"]["x"]) / 2,
                "y": (door_or_window["north_east"]["y"] + door_or_window["north_west"]["y"]) / 2,
            }
            self.sorted_points.append(
                convert_coordinates_to_line(
                    middle_point,
                    self.walls_length,
                ),
            )
        self.sorted_points.sort()

    def wall_definition(self, point: dict) -> int:
        """
        Returns the number of the wall to which the point belongs

        Args: Point - the insertion point of the object into the room

        Returns: Wall number

        """

        if point["y"] == 0:
            return 4
        elif point["x"] == 0:
            return 1
        elif point["y"] == self.room_coordinates["north_east"]["y"]:
            return 2
        elif point["x"] == self.room_coordinates["north_east"]["x"]:
            return 3
        self.room_coordinates = 0
