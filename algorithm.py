"""Algorithm."""

import bisect
import random

import create_picture


class FurnitureArrangement:
    coordinates = []  # хранение координат по схеме "ключ объекта: (координаты, маркеры углов, маркеры точек)
    free_space = []  # хранение расстояний между мебелью через запятую (в виде координат)
    sorted_points = []  # хранения точек на прямой из сложенных сторон комнаты для правильной вставки получившихся координат в список
    wall_perimetr = 0  # хранения периметра комнаты для удобства обращения из функций

    room_coordinates = {}  # хранение координат комнаты для удобства обращения из функций
    room_coordinates_tuple = ()  # хранение координаты комнаты для удобства вычислений
    walls_length = ()  # хранение длин стен для удобства обращения

    def convert_coordinates_to_line(self, coordinates: dict) -> float | int:
        """Функция преобразует координаты в точку на прямой."""
        if coordinates['x'] == 0:
            return coordinates['y']
        elif coordinates['y'] == self.walls_length[0]:
            return self.walls_length[0] + coordinates['x']
        elif coordinates['x'] == self.walls_length[1]:
            return sum(self.walls_length[:3]) - coordinates['y']
        return sum(self.walls_length) - coordinates['x']

    def wall_definition(self, dot: dict):
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
        length = {}
        counter = 1

        def core_and_output(first_object, second_object):
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

    def middle_of_the_distance_on_the_wall(self, free_space: dict) -> dict:
        """
        Функция для нахождения средней точки в оставшемся пустом пространстве комнаты.
        Получает на вход координаты точек и длины стен.
        Возвращает координаты средней точки.
        """

        def convert_line_to_coordinates(dot: float | int) -> dict:
            """Функция преобразует точку на прямой в координаты"""

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
            nonlocal figure, middle_point, objects_counter, cycle_counter, cycle_border
            middle_point["x"], middle_point["y"] = self.middle_of_the_distance_on_the_wall(middle_point).values()
            wall = self.wall_definition(middle_point)
            figure = self.corner_markings(length_and_width, middle_point, wall)
            objects_counter = 0
            cycle_counter += 1

        def rib_crossover_check(object, object_2):
            # Проверка на пересечение ребер в левом нижнем углу
            if (object["south_east"]["y"] > object_2["south_east"]["y"]
            > object_2["south_west"]["y"] > object["north_east"]["y"]
          and object_2["south_east"]["x"] > object["south_west"]["x"]
              > object["south_east"]["x"] > object_2["north_east"]["x"]):

                displacement()
            # Проверка на пересечение ребер в левом верхнем углу
            elif (
                object_2["north_east"]["y"]
                > object["south_east"]["y"]
                > object["south_west"]["y"]
                > object_2["south_east"]["y"]
                and object["south_east"]["x"]
                > object_2["south_east"]["x"]
                > object_2["south_west"]["x"]
                > object["north_east"]["x"]
            ):
                displacement()
            # Проверка на пересечение ребер в правом верхнем углу
            elif (
                object["north_east"]["y"]
                > object_2["north_west"]["y"]
                > object_2["north_east"]["y"]
                > object["south_east"]["y"]
                and object_2["north_east"]["x"]
                > object["south_east"]["x"]
                > object["south_west"]["x"]
                > object_2["south_east"]["x"]
            ):
                displacement()
            # Проверка на пересечение ребер в правом нижнем углу
            elif (
                object_2["south_east"]["y"]
                > object["south_west"]["y"]
                > object["south_east"]["y"]
                > object_2["north_east"]["y"]
                and object["north_east"]["x"]
                > object_2["south_west"]["x"]
                > object_2["south_east"]["x"]
                > object["south_east"]["x"]
            ):
                displacement()

        def corner_crossover_check(object, object_2):
            # Проверка на вхождение углов объектов в левом нижнем углу комнаты
            if (
                object_2["south_west"]["x"]
                > object["south_east"]["x"]
                > object_2["north_west"]["x"]
                and object_2["south_east"]["y"]
                > object["south_east"]["y"]
                > object_2["north_west"]["y"]
            ):
                displacement()
            # Проверка на вхождение углов объектов в левом верхнем углу комнаты
            elif (
                object_2["south_east"]["x"]
                > object["south_east"]["x"]
                > object_2["south_west"]["x"]
                and object_2["north_west"]["y"]
                > object["south_east"]["y"]
                > object_2["south_west"]["y"]
            ):
                displacement()
            # Проверка на вхождение углов объектов в правом верхнем углу комнаты
            elif (
                object_2["north_east"]["x"]
                > object["south_east"]["x"]
                > object_2["south_east"]["x"]
                and object_2["south_west"]["y"]
                > object["south_east"]["y"]
                > object_2["south_east"]["y"]
            ):
                displacement()
            # Проверка на вхождение углов объектов в правом нижнем углу комнаты
            elif (
                object_2["south_west"]["x"]
                > object["south_east"]["x"]
                > object_2["south_east"]["x"]
                and object_2["south_west"]["y"]
                > object["south_east"]["y"]
                > object_2["north_east"]["y"]
            ):
                displacement()

        def layering_of_objects_check(object, object_2):
            for item in object.values():
                # Проверяем пересечение с другими объектами в комнате
                if (object_2["north_west"]["x"] <= item["x"] <= object_2["north_east"]["x"]
                and object_2["south_east"]["y"] <= item["y"] <= object_2["north_east"]["y"]):
                    displacement()

                elif (object_2["north_west"]["x"] >= item["x"] >= object_2["north_east"]["x"]
                  and object_2["south_east"]["y"] >= item["y"] >= object_2["north_east"]["y"]):
                    displacement()

                elif (object_2["north_west"]["x"] <= item["x"] <= object_2["north_east"]["x"]
                  and object_2["south_east"]["y"] <= item["y"] <= object_2["south_west"]["y"]):
                    displacement()

                elif (object_2["north_west"]["x"] >= item["x"] >= object_2["north_east"]["x"]
                  and object_2["south_east"]["y"] >= item["y"] >= object_2["south_west"]["y"]):
                    displacement()

        # Задаем переменные, чтобы определить случаи для выхода из цикла
        objects_counter = 0
        cycle_counter = 0
        cycle_border = 2000
        breaker = 1  # Переменная, выводящая из общего цикла при не пересечении объектов

        # Задаем данные для дальнейшей их отправки в функцию переноса объекта
        displacement_start = 0
        middle_point["displacement_value"] = 1
        middle_point["shift_method"] = "plus"

        while cycle_counter < cycle_border:
            while objects_counter < len(self.coordinates):
                figure_2 = self.coordinates[objects_counter]

                # Проверяем пересечение противоположных объектов
                layering_of_objects_check(figure, figure_2)
                # Проверяем объекты на поглощение друг друга
                layering_of_objects_check(figure_2, figure)
                # Проверка пересечения ребер, если объекты находятся с одной и с другой стороны друг от друга
                rib_crossover_check(figure, figure_2)
                rib_crossover_check(figure_2, figure)
                # Проверяем на вхождение углов объектов внутрь друг друга
                corner_crossover_check(figure, figure_2)
                corner_crossover_check(figure_2, figure)

                breaker += 1

                if cycle_counter >= cycle_border:
                    return False
                objects_counter += 1

            # Проверяем, что мебель не выходит за пределы комнаты
            if (figure["north_east"]["x"] > walls["second_wall"]
                or figure["south_east"]["x"] > walls["second_wall"]):
                displacement()

            elif (figure["north_east"]["y"] > walls["first_wall"]
                or figure["south_east"]["y"] > walls["first_wall"]):
                displacement()

            elif figure["south_west"]["x"] < 0 or figure["south_west"]["y"] < 0:
                displacement()

            else:
                breaker += 1

            if breaker >= len(self.coordinates) + 1:
                break

            breaker = 1

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

    def corner_markings(self, length_and_width: dict, center: dict, wall_number: int) -> dict:
        corners_coordinates = {
            "north_west": {"x": 0, "y": 0},
            "north_east": {"x": 0, "y": 0},
            "south_west": {"x": 0, "y": 0},
            "south_east": {"x": 0, "y": 0},
        }

        north_east = corners_coordinates["north_east"]
        north_west = corners_coordinates["north_west"]
        south_east = corners_coordinates["south_east"]
        south_west = corners_coordinates["south_west"]

        length = length_and_width["length"]
        width = length_and_width["width"]

        if wall_number == 1:
            north_east["x"] = center["x"]
            north_east["y"] = center["y"] + (width / 2)
            north_west["x"] = center["x"]
            north_west["y"] = center["y"] - (width / 2)
            south_east["x"] = center["x"] + length
            south_east["y"] = center["y"] + (width / 2)
            south_west["x"] = center["x"] + length
            south_west["y"] = center["y"] - (width / 2)

        elif wall_number == 2:
            north_east["x"] = center["x"] + (width / 2)
            north_east["y"] = center["y"]
            north_west["x"] = center["x"] - (width / 2)
            north_west["y"] = center["y"]
            south_east["x"] = center["x"] + (width / 2)
            south_east["y"] = center["y"] - length
            south_west["x"] = center["x"] - (width / 2)
            south_west["y"] = center["y"] - length

        elif wall_number == 3:
            north_east["x"] = center["x"]
            north_east["y"] = center["y"] - (width / 2)
            north_west["x"] = center["x"]
            north_west["y"] = center["y"] + (width / 2)
            south_east["x"] = center["x"] - length
            south_east["y"] = center["y"] - (width / 2)
            south_west["x"] = center["x"] - length
            south_west["y"] = center["y"] + (width / 2)

        elif wall_number == 4:
            north_east["x"] = center["x"] - (width / 2)
            north_east["y"] = center["y"]
            north_west["x"] = center["x"] + (width / 2)
            north_west["y"] = center["y"]
            south_east["x"] = center["x"] - (width / 2)
            south_east["y"] = center["y"] + length
            south_west["x"] = center["x"] + (width / 2)
            south_west["y"] = center["y"] + length

        return corners_coordinates


    def algorithm_activation(self, doors_and_windows: list, furniture: list, room_size: dict):
        # Определения координат комнаты для работы определения принадлежности координат к конкретной стене
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

        def middle_point(coordinates):
            return abs

        # Функция определения стены по координатам для отправки ее в дальнейшем в corner_markings
        for item in doors_and_windows:
            middle_point = {"x": (item["north_east"]["x"] + item["north_west"]["x"]) / 2,
                            "y": (item["north_east"]["y"] + item["north_west"]["y"]) / 2}
            self.coordinates.append(item)
            self.sorted_points.append(self.convert_coordinates_to_line(middle_point))

        self.sorted_points.sort()

        for item in furniture:
            result_free_space = self.free_space_algorithm(self.coordinates)
            result_middle_distance = self.middle_of_the_distance_on_the_wall(result_free_space)
            result_wall_definition = self.wall_definition(result_middle_distance)
            result_corner_markings = self.corner_markings(item, result_middle_distance, result_wall_definition)
            self.placing_in_coordinates(result_middle_distance, result_corner_markings, room_size, item)

        create_picture.create_rectangles(self.coordinates)
        print(self.coordinates)

    def shuffle_furniture(furniture: list, mode: str) -> list:
        '''Shuffle list of furniture with three mods.
        mode keys: light, medium, hard.'''

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
