class Furniture:
    def __init__(self, length, width, center: dict, wall_number: int):
        self.length = length
        self.width = width
        self.center = center
        self.wall_number = wall_number
        self.corners_coordinates: dict | None = None
        self.corner_markings()

    def corner_markings(self):
        """Вычисляем координаты углов объекта.

        Имея центр объекта и его размеры, относительно конкретной стены
        обозначить его углы координатами.

        Args:
            self.center: центр стороны объекта, примыкающей к стене {"x": 0, "y": 0},
            self.wall_number: сторона комнаты с учетом, что левая сторона первая, а
            дальнейшие нумеруются по часовой стрелке

        Returns:
            dict: словарь с координатами углов
                    {
                    "north_west": {"x": 0, "y": 0},
                    "north_east": {"x": 0, "y": 0},
                    "south_west": {"x": 0, "y": 0},
                    "south_east": {"x": 0, "y": 0},
                    }
        """
        self.corners_coordinates = {
            "north_west": {"x": 0, "y": 0},
            "north_east": {"x": 0, "y": 0},
            "south_west": {"x": 0, "y": 0},
            "south_east": {"x": 0, "y": 0},
        }

        # последующие шесть строчек нужны для визуального сокращения кода
        north_east = self.corners_coordinates["north_east"]
        north_west = self.corners_coordinates["north_west"]
        south_east = self.corners_coordinates["south_east"]
        south_west = self.corners_coordinates["south_west"]

        # так как примыкающая сторона объекта смещает внутренние стороны света
        # углов, то относительно каждой стороны координаты вычисляются по-разному
        if self.wall_number == 1:
            north_east["x"] = self.center["x"]
            north_east["y"] = self.center["y"] + (self.width / 2)
            north_west["x"] = self.center["x"]
            north_west["y"] = self.center["y"] - (self.width / 2)
            south_east["x"] = self.center["x"] + self.length
            south_east["y"] = self.center["y"] + (self.width / 2)
            south_west["x"] = self.center["x"] + self.length
            south_west["y"] = self.center["y"] - (self.width / 2)

        elif self.wall_number == 2:
            north_east["x"] = self.center["x"] + (self.width / 2)
            north_east["y"] = self.center["y"]
            north_west["x"] = self.center["x"] - (self.width / 2)
            north_west["y"] = self.center["y"]
            south_east["x"] = self.center["x"] + (self.width / 2)
            south_east["y"] = self.center["y"] - self.length
            south_west["x"] = self.center["x"] - (self.width / 2)
            south_west["y"] = self.center["y"] - self.length

        elif self.wall_number == 3:
            north_east["x"] = self.center["x"]
            north_east["y"] = self.center["y"] - (self.width / 2)
            north_west["x"] = self.center["x"]
            north_west["y"] = self.center["y"] + (self.width / 2)
            south_east["x"] = self.center["x"] - self.length
            south_east["y"] = self.center["y"] - (self.width / 2)
            south_west["x"] = self.center["x"] - self.length
            south_west["y"] = self.center["y"] + (self.width / 2)

        elif self.wall_number == 4:
            north_east["x"] = self.center["x"] - (self.width / 2)
            north_east["y"] = self.center["y"]
            north_west["x"] = self.center["x"] + (self.width / 2)
            north_west["y"] = self.center["y"]
            south_east["x"] = self.center["x"] - (self.width / 2)
            south_east["y"] = self.center["y"] + self.length
            south_west["x"] = self.center["x"] + (self.width / 2)
            south_west["y"] = self.center["y"] + self.length
