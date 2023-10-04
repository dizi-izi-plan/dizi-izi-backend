"""Algorithm."""

import bisect
import random
from .crossover_checks import checks
from .corner_markings import corner_markings
from .offset_finder_convert import MiddlePointAndShift


class FurnitureArrangement(MiddlePointAndShift):

    def __init__(self):

        coordinates, free_space, sorted_points = [], [], []
        wall_perimetr = 0
        room_coordinates = {}
        room_coordinates_tuple, walls_length = (), ()

        self.coordinates = coordinates  # хранение координат по схеме "ключ объекта: (координаты, маркеры углов, маркеры точек)
        self.free_space = free_space  # хранение расстояний между мебелью через запятую (в виде координат)
        self.sorted_points = sorted_points  # хранения точек на прямой из сложенных сторон комнаты для правильной вставки получившихся координат в список
        self.wall_perimetr = wall_perimetr  # хранения периметра комнаты для удобства обращения из функций

        self.room_coordinates = room_coordinates  # хранение координат комнаты для удобства обращения из функций
        self.room_coordinates_tuple = room_coordinates_tuple  # хранение координаты комнаты для удобства вычислений
        self.walls_length = walls_length  # хранение длин стен для удобства обращения

    def free_space_algorithm(self, objects: list) -> dict:
        # На вход подается список с координатами углов объектов. Координаты между друг другом минусим, находим
        # по ближайшим неприлегающим углам расстояние по модулю в виде гипотенузы (вычитание по иксу -- это
        # один катет, вычитание по игрику -- другой). И записыванием самое большое расстояние в переменную. Углы
        # разбиты по сторонам света: north_west, north-east, south-west, south-east. Отдельно так же идет
        # значение и длина стены "walls_length": {"first_wall": 1, "second_wall": 2, "third_wall": 1, "fourth_wall": 2}

        """

        Args:

        Returns:

        """

        length = {}
        counter = 1

        def core_and_output(first_object, second_object):
            """

            Args:

            Returns:

            """

            first_right_corner = "north_east"
            second_left_corner = "north_west"

            if first_object["north_east"] in self.room_coordinates_tuple:
                first_right_corner = "south_east"
            if second_object[counter][
                "north_west"] in self.room_coordinates_tuple:
                second_left_corner = "south_west"

            first_point = self.convert_coordinates_to_line(
                first_object[first_right_corner], self.walls_length)
            second_point = self.convert_coordinates_to_line(
                second_object[counter][second_left_corner], self.walls_length)
            distance = 0
            if second_point >= first_point:
                distance = second_point - first_point
            elif second_point < first_point:
                distance = second_point + (self.wall_perimetr - first_point)

            length[distance] = {
                "left_corner": first_object[first_right_corner],
                "right_corner": second_object[counter][second_left_corner]}

            # расстояния могут быть одинаковые, но нам по сути неважно какой из вариантов брать, а значит мы
            # можем просто перезаписать ключ словаря

        for item in objects:
            if counter == len(objects):
                counter = 0
            core_and_output(item, objects)
            counter += 1

        return length[max(length)]

    def placing_in_coordinates(
            self,
            data: dict,
            figure: dict,
            walls: dict,
            object_attributes: dict,
    ) -> bool:
        """Функция проверки возможности резервирования места для мебели в комнате.

        Args:
            data (dict):
            figure (dict): координаты для мебели. {"north_west": {"x": 0, "y": 0},
                   "north_east": {"x": 0, "y": 0}, "south_west": {"x": 0, "y": 0}, "south_east": {"x": 0, "y": 0}}
            walls (dict): стены комнаты начиная от левой {"first_wall": 0, "second_wall": 0, "third_wall": 0, "fourth_wall":0}
            length_and_width(dict): ширина и длина располагаемого объекта

        Returns:
            bool: True, если место зарезервировано, иначе False
        """

        def displacement():
            """
            """
            nonlocal figure, data, objects_counter, cycle_counter, cycle_border, displacement_start
            displacement_start += data["displacement_value"]

            data["x"], data["y"] = self.offset(data, self.wall_perimetr,
                                               self.walls_length).values()
            wall = self.wall_definition(data)
            figure = corner_markings(object_attributes, data, wall)
            objects_counter = 0
            cycle_counter += 1

        # Задаем переменные, чтобы определить случаи для выхода из цикла
        objects_counter = 0  # переменная необходимая для учета всех объектов, относительно которых делается проверка на пересечение
        cycle_counter = 0  # переменная для подсчета количества циклов, дабы они не были бесконечным
        cycle_border = self.wall_perimetr  # переменная, указывающая при каком значении будет критическая ошибка о невозможности размещения
        breaker = 0  # Переменная, выводящая из общего цикла при не пересечении объектов

        # Задаем данные для дальнейшей их отправки в функцию переноса объекта
        displacement_start = 0  # переменная необходима для обозначения стартовой точки, относительно которой будет смещение
        data[
            "shift_method"] = "plus"  # указываем сторону для начального смещения

        # указываем значение на которое будет смещаться объект в зависимости от разрядности периметра
        if self.wall_perimetr < 100:
            data["displacement_value"] = 1
        elif self.wall_perimetr < 1000:
            data["displacement_value"] = 10
        elif self.wall_perimetr < 10000:
            data["displacement_value"] = 100
        elif self.wall_perimetr < 100000:
            data["displacement_value"] = 1000

        # сам цикл, в котором мы пытаемся разметить объект заданное количество циклов и проверяем пересечения со всеми объектами
        while cycle_counter < cycle_border and objects_counter < len(
                self.coordinates):

            figure_2 = self.coordinates[objects_counter]
            if checks(figure, figure_2, walls):
                # добавляем единицу брейкеру за каждый прошедший проверки пересечения объект,
                # чтобы организовать выход из цикла
                breaker += 1
                objects_counter += 1
            else:
                displacement()
            # если пересечения со всеми объектами были проверены успешно, то выходим из цикла
            if breaker >= len(self.coordinates):
                break
            if cycle_counter >= cycle_border:
                raise Exception("Превышено число попыток на размещение")

            breaker = 1

        # Если все проверки прошли, добавляем координаты мебели в словарь coordinates
        final_point = self.convert_coordinates_to_line(data, self.walls_length)

        return self.convert_coordinates_to_line(data,
                                                self.walls_length), figure

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

        # Функция определения стены по координатам для отправки ее в дальнейшем в corner_markings
        for item in doors_and_windows:
            middle_point = {
                "x": (item["north_east"]["x"] + item["north_west"]["x"]) / 2,
                "y": (item["north_east"]["y"] + item["north_west"]["y"]) / 2}
            self.coordinates.append(item)
            self.sorted_points.append(
                self.convert_coordinates_to_line(middle_point,
                                                 self.walls_length))

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

    def shuffle_furniture(self, furniture: list, mode: str) -> list:
        """Функция меняет позиции внутри списка мебели местами для предоставления пользователю других
        результатов при повторной генерации

        Args:
            furniture: список мебели, необходимой для перестановки
            mode: степень серьезности перестановки
        Returns:
            list: список мебели с перемещенными позициями

        """

        def light_or_medium_shuffle(mode: str) -> list:
            '''Light mode shuffle have swap position with one step.
            Medium mode shuffle have swap position with two step.'''
            if mode == 'light':
                step = 1
            if mode == 'medium':
                step = 2
            for i in range(0, len(furniture) - step, step + 1):
                furniture[i], furniture[i + step] = (
                    furniture[i + step],
                    furniture[i],
                )
            return furniture

        def hard_shuffle():
            """Hard mode shuffle have random swap position."""
            random.shuffle(furniture)

        # Key for selection mode
        if mode == 'hard':
            hard_shuffle()
            return furniture
        if mode == 'light' or 'medium':
            return light_or_medium_shuffle(mode)
