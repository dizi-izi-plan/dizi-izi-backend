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
            {"north_wall": {"x_1": 0, "y_1": figure.side_a, "x_2": figure.side_b, "y_2": figure.side_c}},
            {"east_wall": {"x_1": figure.side_b, "y_1": figure.side_c, "x_2": figure.side_d, "y_2": 0}},
            {"south_wall": {"x_1": figure.side_d, "y_1": 0, "x_2": 0, "y_2": 0}})
        return room_coordinates

    def determining_the_furthest_point(self):
        return None

    # Функция определения самой отдаленной точки в комнате по заданным точкам.
    # Мы складываем длины всех стен (которые получаем на входе), вычисляем
    # расстояние между центрами окна и двери с одной стороны и с другой стороны,
    # делим большее расстояние на двое и получаем новую точку для мебели.
    # Если координаты стены или других предметов пересекаются с координатами
    # расположенной мебели, мы сдвигаем примыкающий к стене центр грани этой
    # мебели на 5 сантиметров в одну из сторон в координатах. Если это не
    # помогает, то смещаем в другую сторону. Важно помнить, что сдвигаем мы
    # мебель по сторонам прямоугольника.
    # Функцию повторяем до тех пор, пока не кончится мебель. Если мебель
    # невозможно расположить без пересечения координат, то мы возвращаем ошибку.


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
        "Метод котнроля допустимой общей площади мебели в помещении."
        if (area_furniture / area_room) > 0.75:
            raise LackSpace("Общая площадь мебели превышает площадь помещения!")
        return True

    def algorithm_activation(self):
        return None

    # Функция определения общей площади всей мебели. Если общая площадь больше,
    # чем 75% (посмотрим на тестах сколько именно нужно будет, но пока так)
    # площади комнаты, то возвращается ошибка о невозможности планировки. Эта
    # функция нужна на случай, если такое количество мебели невозможно разместить
    # в данной комнате по причине нехватки места.
