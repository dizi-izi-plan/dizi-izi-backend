"""Algorithm."""

import bisect
import random
from crossover_checks import *
from corner_markings import *
from layout_algorithm import create_picture, crossover_checks


class FurnitureArrangement:
    coordinates = []  # хранение координат по схеме "ключ объекта: (координаты, маркеры углов, маркеры точек)
    free_space = []  # хранение расстояний между мебелью через запятую (в виде координат)
    sorted_points = []  # хранения точек на прямой из сложенных сторон комнаты для правильной вставки получившихся координат в список
    wall_perimetr = 0  # хранения периметра комнаты для удобства обращения из функций

    room_coordinates = {}  # хранение координат комнаты для удобства обращения из функций
    room_coordinates_tuple = ()  # хранение координаты комнаты для удобства вычислений
    walls_length = ()  # хранение длин стен для удобства обращения

    def convert_coordinates_to_line(self, coordinates: dict) -> float | int:
        """Функция преобразует координаты в точку на прямой.

        Args:
        Returns:

        """
        if coordinates['x'] == 0:
            return coordinates['y']
        elif coordinates['y'] == self.walls_length[0]:
            return self.walls_length[0] + coordinates['x']
        elif coordinates['x'] == self.walls_length[1]:
            return sum(self.walls_length[:3]) - coordinates['y']
        return sum(self.walls_length) - coordinates['x']

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
            if second_object[counter]["north_west"] in self.room_coordinates_tuple:
                second_left_corner = "south_west"

            first_point = self.convert_coordinates_to_line(first_object[first_right_corner])
            second_point = self.convert_coordinates_to_line(second_object[counter][second_left_corner])
            distance = 0
            if second_point >= first_point:
                distance = second_point - first_point
            elif second_point < first_point:
                distance = second_point + (self.wall_perimetr - first_point)

            length[distance] = {"left_corner": first_object[first_right_corner],
                                "right_corner": second_object[counter][second_left_corner], }

            # расстояния могут быть одинаковые, но нам по сути неважно какой из вариантов брать, а значит мы
            # можем просто перезаписать ключ словаря

        for item in objects:
            if counter == len(objects):
                counter = 0
            core_and_output(item, objects)
            counter += 1
        return length[max(length)]

    def middle_and_shift(self, free_space: dict) -> dict:
        """
        Функция для нахождения средней точки в оставшемся пустом пространстве комнаты.
        Получает на вход координаты точек и длины стен.
        Возвращает координаты средней точки.

        Args:

        Returns:

        """

        def convert_line_to_coordinates(dot: float | int) -> dict:
            """Функция преобразует точку на прямой в координаты

        Args:

        Returns:

        """

            if 0 <= dot <= self.walls_length[0]:
                return {'x': 0, 'y': dot}
            elif self.walls_length[0] < dot <= sum(self.walls_length[:2]):
                return {'x': dot - self.walls_length[0],
                        'y': self.walls_length[0]}
            elif sum(self.walls_length[:2]) < dot <= sum(self.walls_length[:3]):
                return {'x': self.walls_length[1],
                        'y': sum(self.walls_length[:3]) - dot}
            elif sum(self.walls_length[:3]) < dot <= self.wall_perimetr:
                return {'x': self.wall_perimetr - dot, 'y': 0}
            raise Exception(
                'Ошибка данных, нет возможности разместить среднюю точку на одной из стен комнаты.'
            )

        if 'left_corner' in free_space:
            """

            Args:

            Returns:

            """

            point_1 = self.convert_coordinates_to_line(free_space['left_corner'])
            point_2 = self.convert_coordinates_to_line(free_space['right_corner'])
            middle_point = (
                (point_2 + point_1) / 2
                if point_1 < point_2
                else (point_2 + point_1 + self.wall_perimetr) / 2
            )
            if middle_point > self.wall_perimetr:
                middle_point = middle_point - self.wall_perimetr
            return convert_line_to_coordinates(middle_point)

        elif "x" in free_space:
            """

            Args:

            Returns:

            """

            point = self.convert_coordinates_to_line({"x": free_space["x"], "y": free_space["y"]})
            if free_space["shift_method"] == "plus":
                shifted_point = point + free_space["displacement_value"]
            elif free_space["shift_method"] == "minus":
                shifted_point = point - free_space["displacement_value"]
            else:
                raise Exception('Неправильно введенный метод')

            if shifted_point < 0:
                shifted_point = self.wall_perimetr - abs(shifted_point)
            elif shifted_point > self.wall_perimetr:
                shifted_point = abs(shifted_point) - self.wall_perimetr
            # else:
            #     raise Exception('Неправильно переменные')

            return convert_line_to_coordinates(shifted_point)

    def placing_in_coordinates(
        self,
        middle_point: dict,
        figure: dict,
        walls: dict,
        length_and_width: dict,
    ) -> bool:
        """Функция проверки возможности резервирования места для мебели в комнате.

        Args:
            middle_point (dict): {"middle_point": {"x": 0, "y": 0}}
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
            nonlocal figure, middle_point, objects_counter, cycle_counter, cycle_border, displacement_start
            # if cycle_counter % 2 != 0:
            #     middle_point["shift_method"] = "minus"
            # elif cycle_counter % 2 == 0:
            #     middle_point["shift_method"] = "plus"
            # displacement_start += middle_point["displacement_value"]
            #

            middle_point["x"], middle_point["y"] = self.middle_and_shift(middle_point).values()
            wall = self.wall_definition(middle_point)
            figure = corner_markings(length_and_width, middle_point, wall)
            objects_counter = 0
            cycle_counter += 1

        # Задаем переменные, чтобы определить случаи для выхода из цикла
        objects_counter = 0  # переменная необходимая для учета всех объектов, относительно которых делается проверка на пересечение
        cycle_counter = 0  # переменная для подсчета количества циклов, дабы они не были бесконечными
        cycle_border = 2000  # переменная, указывающая при каком значении будет критическая ошибка о невозможности размещения
        breaker = 2  # Переменная, выводящая из общего цикла при не пересечении объектов

        # Задаем данные для дальнейшей их отправки в функцию переноса объекта
        displacement_start = 0  # переменная необходима для обозначения стартовой точки, относительно которой будет смещение
        middle_point["displacement_value"] = 1  # значение на которое будет смещаться объект
        middle_point["shift_method"] = "plus"  # указываем сторону для начального смещения

        # сам цикл, в котором мы пытаемся разметить объект заданное количество циклов и проверяем пересечения со всеми объектами
        while cycle_counter < cycle_border:
            while objects_counter < len(self.coordinates):
                figure_2 = self.coordinates[objects_counter]

                if checks(figure, figure_2, walls):
                    # добавляем значение, что с этим объектом все проверки прошли успешно
                    breaker += 1
                    objects_counter += 1
                else:
                    displacement()

                # выходим из цикла, если достигнут лимит циклов
                if cycle_counter >= cycle_border:
                    return False

            # если пересечения со всеми объектами были проверены успешно, то выходим из цикла
            if breaker >= len(self.coordinates):
                break

            breaker = 1

            # меняем значения для отправки в функцию смещения
            if cycle_counter % 2 != 0:
                middle_point["shift_method"] = "minus"
            elif cycle_counter % 2 == 0:
                middle_point["shift_method"] = "plus"
            displacement_start += middle_point["displacement_value"]

            if cycle_counter >= cycle_border:
                return False

        # Если все проверки прошли, добавляем координаты мебели в словарь coordinates
        final_point = self.convert_coordinates_to_line(middle_point)
        bisect.insort(self.sorted_points, final_point)
        self.coordinates.insert(self.sorted_points.index(final_point), figure)
        return True


    def data_preprocessing(self, room_size, doors_and_windows):

        """

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
            middle_point = {"x": (item["north_east"]["x"] + item["north_west"]["x"]) / 2,
                            "y": (item["north_east"]["y"] + item["north_west"]["y"]) / 2}
            self.coordinates.append(item)
            self.sorted_points.append(self.convert_coordinates_to_line(middle_point))

        self.sorted_points.sort()

    def algorithm_activation(self, doors_and_windows: list, furniture: list, room_size: dict):
        """Основная функция алгоритма, проходящаяся по всему заданному списку мебели
        и расставляющая каждую единицу внутри помещения

        Args:
            doors_and_windows:
            furniture:
            room_size:
        Returns:

        """

        self.data_preprocessing(room_size, doors_and_windows)
        for item in furniture:
            result_free_space = self.free_space_algorithm(self.coordinates)
            result_middle_distance = self.middle_and_shift(result_free_space)
            result_wall_definition = self.wall_definition(result_middle_distance)
            result_corner_markings = corner_markings(item, result_middle_distance, result_wall_definition)
            self.placing_in_coordinates(result_middle_distance, result_corner_markings, room_size, item)

        # функции для возможности наглядного тестирования результата до отправки на фронт
        create_picture.create_rectangles(self.coordinates, self.room_coordinates)
        print(self.coordinates)


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
