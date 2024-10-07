from .offset_finder_convert import MiddlePointAndShift


class Room(MiddlePointAndShift):
    def __init__(self):
        self.walls_length = ()
        self.wall_perimetr = 0
        self.room_coordinates = {}
        self.room_coordinates_tuple = ()
        self.coordinates = []
        self.sorted_points = []

    def data_preprocessing(self, room_size, doors_and_windows):
        """Функция необходима для размещения данных в глобальных координатах
        и подготовки их к дальнейшей обработке в функциях

        Args:

        Returns:

        """
        self.walls_length = tuple(room_size.values())
        self.wall_perimetr = sum(self.walls_length)

        self.room_coordinates = {
            "south_west": {"x": 0, "y": 0},
            "north_west": {"x": 0, "y": room_size["first_wall"]},
            "north_east": {
                "x": room_size["second_wall"],
                "y": room_size["first_wall"],
            },
            "south_east": {"x": room_size["second_wall"], "y": 0},
        }

        self.room_coordinates_tuple = tuple(self.room_coordinates.values())

        # Функция определения стены по координатам для отправки ее в
        # дальнейшем в corner_markings
        for item in doors_and_windows:
            middle_point = {
                "x": (item["north_east"]["x"] + item["north_west"]["x"]) / 2,
                "y": (item["north_east"]["y"] + item["north_west"]["y"]) / 2,
            }
            self.coordinates.append(item)
            self.sorted_points.append(
                self.convert_coordinates_to_line(
                    middle_point,
                    self.walls_length,
                ),
            )
        self.sorted_points.sort()

    def wall_definition(self, dot: dict):
        """

        Args:

        Returns:

        """

        if dot["y"] == 0:
            return 4
        elif dot["x"] == 0:
            return 1
        elif dot["y"] == self.room_coordinates["north_east"]["y"]:
            return 2
        elif dot["x"] == self.room_coordinates["north_east"]["x"]:
            return 3
        self.room_coordinates = 0
