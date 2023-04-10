"""Algorithm."""

import math
from typing import NamedTuple

from exception import LackSpace, IncorrectFigure


class Figure(NamedTuple):
    """Figure module."""
    side_a: float
    side_b: float
    side_c: float
    side_d: float


class FurnitureArrangement():

    def room_coordinates(self, figure: Figure) -> tuple:
        "Метод создания координат комнаты."
        room_coordinates = (
            {"west_wall": {"x_1": 0, "y_1": 0, "x_2": 0, "y_2": figure.side_a}},
            {"north_wall": {"x_1": 0, "y_1": figure.side_a, "x_2": figure.side_b, "y_2": figure.side_a}},
            {"east_wall": {"x_1": figure.side_b, "y_1": figure.side_c, "x_2": figure.side_b, "y_2": 0}},
            {"south_wall": {"x_1": figure.side_d, "y_1": 0, "x_2": 0, "y_2": 0}})
        return room_coordinates

    coordinates = {}  # хранение координат по схеме "ключ объекта: (координаты, маркеры углов, маркеры точек)
    free_space = [] # хранение расстояний между мебелью через запятую (в виде координат)

    def placing_in_coordinates(self):
        return None

    def corner_markings(self, length_and_width: dict, center: dict, wall_number: int) -> dict:
        corners_coordinates = {"north_west": {"x": 0, "y": 0}, "north_east": {"x": 0, "y": 0},
                               "south_west": {"x": 0, "y": 0}, "south_east": {"x": 0, "y": 0}}

        if wall_number == 1:
            corners_coordinates["north_east"]["x"] = center["x"]
            corners_coordinates["north_east"]["y"] = center["y"] + (length_and_width["width"] // 2)
            corners_coordinates["north_west"]["x"] = center["x"]
            corners_coordinates["north_west"]["y"] = center["y"] - (length_and_width["width"] // 2)
            corners_coordinates["south_east"]["x"] = center["x"] + length_and_width["length"]
            corners_coordinates["south_east"]["y"] = center["y"] + (length_and_width["width"] // 2)
            corners_coordinates["south_west"]["x"] = center["x"] + length_and_width["length"]
            corners_coordinates["south_west"]["y"] = center["y"] - (length_and_width["width"] // 2)

        elif wall_number == 2:
            corners_coordinates["north_east"]["x"] = center["x"] + (length_and_width["width"] // 2)
            corners_coordinates["north_east"]["y"] = center["y"]
            corners_coordinates["north_west"]["x"] = center["x"] - (length_and_width["width"] // 2)
            corners_coordinates["north_west"]["y"] = center["y"]
            corners_coordinates["south_east"]["x"] = center["x"] + (length_and_width["width"] // 2)
            corners_coordinates["south_east"]["y"] = center["y"] - length_and_width["length"]
            corners_coordinates["south_west"]["x"] = center["x"] - (length_and_width["width"] // 2)
            corners_coordinates["south_west"]["y"] = center["y"] - length_and_width["length"]

        elif wall_number == 3:
            corners_coordinates["north_east"]["x"] = center["x"]
            corners_coordinates["north_east"]["y"] = center["y"] - (length_and_width["width"] // 2)
            corners_coordinates["north_west"]["x"] = center["x"]
            corners_coordinates["north_west"]["y"] = center["y"] + (length_and_width["width"] // 2)
            corners_coordinates["south_east"]["x"] = center["x"] - length_and_width["length"]
            corners_coordinates["south_east"]["y"] = center["y"] - (length_and_width["width"] // 2)
            corners_coordinates["south_west"]["x"] = center["x"] - length_and_width["length"]
            corners_coordinates["south_west"]["y"] = center["y"] + (length_and_width["width"] // 2)

        elif wall_number == 4:
            corners_coordinates["north_east"]["x"] = center["x"] - (length_and_width["width"] // 2)
            corners_coordinates["north_east"]["y"] = center["y"]
            corners_coordinates["north_west"]["x"] = center["x"] + (length_and_width["width"] // 2)
            corners_coordinates["north_west"]["y"] = center["y"]
            corners_coordinates["south_east"]["x"] = center["x"] - (length_and_width["width"] // 2)
            corners_coordinates["south_east"]["y"] = center["y"] + length_and_width["length"]
            corners_coordinates["south_west"]["x"] = center["x"] + (length_and_width["width"] // 2)
            corners_coordinates["south_west"]["y"] = center["y"] + length_and_width["length"]

        return corners_coordinates
    
    def middle_of_the_distance_on_the_wall(self):
        return None

    def free_space_algorithm(self, objects: list) -> tuple:
        # На вход подается список с координатами углов объектов. Координаты между друг другом минусим, находим
        # по ближайшим неприлегающим углам расстояние по модулю в виде гипотенузы (вычитание по иксу -- это
        # один катет, вычитание по игрику -- другой). И записыванием самое большое расстояние в переменную. Углы
        # разбиты по сторонам света: north_west, north-east, south-west, south-east.
        length = {}
        counter = 1
        for item in objects:
            if counter == len(objects):
                counter = 0
                distance_x = (item["south_west"]["x"] - objects[counter]["south_east"]["x"])
                distance_y = (item["south_west"]["y"] - objects[counter]["south_east"]["y"])
                round_hypotenuse = round(math.hypot(distance_x, distance_y))
                length[round_hypotenuse] = {"North_east": item["north_east"]},\
                                           {"North_west": objects[counter]["north_west"]}
            # Расстояние высчитываем через функцию поиска гипотенузы "hypot" по двум катетам.
            else:
                distance_x = (item["south_east"]["x"] - objects[counter]["south_west"]["x"])
                distance_y = (item["south_east"]["y"] - objects[counter]["south_west"]["y"])
                round_hypotenuse = round(math.hypot(distance_x, distance_y))
                length[round_hypotenuse] = {"North_west": item["north_west"]},\
                                           {"North_east": objects[counter]["north_east"]}
            # расстояния могут быть одинаковые, но нам по сути неважно какой из вариантов брать, а значит мы
            # можем просто перезаписать ключ словаря
            counter += 1

        return length[max(length)]

    def alternative_free_space_algorithm(self):
        return None

    def longest_distance(self):
        return None



class DataVerificationAndImplementation(FurnitureArrangement):

    def area_calculation(self, figure: Figure) -> float:
        "Метод вычисления площади фигуры."
        if figure.side_a == figure.side_c and figure.side_b == figure.side_d:
            area = figure.side_a * figure.side_b
            return area
        # elif figure.side_b != figure.side_d and figure.side_a == figure.side_c: # Eсли условие выполняется, то фигура является равнобедренной трапецией
        #    trapezoid_height = math.sqrt(pow(figure.side_a, 2) \
        #     - (pow((pow((figure.side_d - figure.side_b), 2) \
        #     + pow(figure.side_a, 2) - pow(figure.side_c, 2)) / (2 \
        #     * (figure.side_d - figure.side_b)), 2)))
        #     area = ((figure.side_d + figure.side_b) / 2) * trapezoid_height
        #     return area
        else: 
            raise IncorrectFigure("Неверно заданы размеры помещения!")

    def area_monitoring(self, area_room: int, area_furniture: int) -> bool:
        "Метод контроля допустимой общей площади мебели в помещении."
        if (area_furniture / area_room) > 0.75:
            raise LackSpace("Общая площадь мебели превышает площадь помещения!")
        return True

    def algorithm_activation(self):
        return None

    def activation(self):
        return None