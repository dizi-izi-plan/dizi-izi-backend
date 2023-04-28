"""Algorithm."""

import math
import create_picture


class FurnitureArrangement:
    coordinates = []  # хранение координат по схеме "ключ объекта: (координаты, маркеры углов, маркеры точек)
    free_space = []  # хранение расстояний между мебелью через запятую (в виде координат)

    def free_space_algorithm(self, objects: list) -> dict:
        # На вход подается список с координатами углов объектов. Координаты между друг другом минусим, находим
        # по ближайшим неприлегающим углам расстояние по модулю в виде гипотенузы (вычитание по иксу -- это
        # один катет, вычитание по игрику -- другой). И записыванием самое большое расстояние в переменную. Углы
        # разбиты по сторонам света: north_west, north-east, south-west, south-east. Отдельно так же идет
        # значение и длина стены "walls_length": {"first_wall": 1, "second_wall": 2, "third_wall": 1, "fourth_wall": 2}
        length = {}
        counter = 1

        def longest_distance_corner(first_left, first_right, second_left, second_right):
            first_distance = abs(first_left - second_left)
            second_distance = abs(first_left - second_right)
            third_distance = abs(first_right - second_left)
            fourth_distance = abs(first_right - second_right)

            minimal_distance = min([first_distance, second_distance, third_distance, fourth_distance])
            return minimal_distance

        def x_or_y_distance(first_object, second_object, x_or_y):
            result = longest_distance_corner(
                first_object["south_west"][f"{x_or_y}"],
                first_object["south_east"][f"{x_or_y}"],
                second_object[counter]["south_west"][f"{x_or_y}"],
                second_object[counter]["south_east"][f"{x_or_y}"])
            return result

        def core_and_output(first_object, second_object):
            x_distance = x_or_y_distance(first_object, second_object, "x")
            y_distance = x_or_y_distance(first_object, second_object, "y")
            hypotenuse = math.hypot(x_distance, y_distance)
            # Расстояние высчитываем через функцию поиска гипотенузы "hypot" по двум катетам.
            length[hypotenuse] = {"left_corner": first_object["north_east"],
                                  "right_corner": second_object[counter]["north_west"]}

            # расстояния могут быть одинаковые, но нам по сути неважно какой из вариантов брать, а значит мы
            # можем просто перезаписать ключ словаря

        for item in objects:
            if counter == len(objects):
                counter = 0
            core_and_output(item, objects)
            counter += 1
        return length[max(length)]

    # Доделать по алгоритму. Вариант с единственным объектом в комнате. Вариант с примыкающими со стороны
    # к объекту стенами. Модернизировать алгоритм на высчитывание расстояния по стене, а не по диагоналям

    def alternative_free_space_algorithm(self):
        return None

    def middle_of_the_distance_on_the_wall(self, free_space: dict, walls: dict) -> dict:
        """
        Функция для нахождения средней точки в оставшемся пустом пространстве комнаты.
        Получает на вход координаты точек и длины стен.
        Возвращает координаты средней точки.
        """
        walls_length = tuple(walls.values())
        room_perimeter = sum(walls_length)

        def convert_coordinates_to_line(coordinates: dict, length_of_walls: tuple) -> float | int:
            """Функция преобразует координаты в точку на прямой."""
            nonlocal room_perimeter
            if coordinates['x'] == 0:
                return coordinates['y']
            elif coordinates['y'] == length_of_walls[0]:
                return length_of_walls[0] + coordinates['x']
            elif coordinates['x'] == length_of_walls[1]:
                return sum(length_of_walls[:3]) - coordinates['y']
            return sum(length_of_walls) - coordinates['x']

        def convert_line_to_coordinates(dot: float | int, length_of_walls: tuple) -> dict:
            """Функция преобразует точку на прямой в координаты"""
            nonlocal room_perimeter
            if 0 <= dot <= walls_length[0]:
                return {'x': 0, 'y': dot}
            elif walls_length[0] < dot <= sum(length_of_walls[:2]):
                return {'x': dot - length_of_walls[0], 'y': length_of_walls[0]}
            elif sum(length_of_walls[:2]) < dot <= sum(length_of_walls[:3]):
                return {'x': length_of_walls[1], 'y': sum(length_of_walls[:3]) - dot}
            elif sum(length_of_walls[:3]) < dot <= room_perimeter:
                return {'x': room_perimeter - dot, 'y': 0}
            raise Exception('Ошибка данных, нет возможности разместить среднюю точку на одной из стен комнаты.')

        if 'left_corner' in free_space:
            point_1 = convert_coordinates_to_line(free_space['left_corner'], walls_length)
            point_2 = convert_coordinates_to_line(free_space['right_corner'], walls_length)
            middle_point = (point_2 + point_1) / 2 if point_1 < point_2 else (point_2 + point_1 + room_perimeter) / 2
            if middle_point > room_perimeter:
                middle_point = middle_point - room_perimeter
            return convert_line_to_coordinates(middle_point, walls_length)

        elif "x" in free_space:
            point = convert_coordinates_to_line({"x": free_space["x"], "y": free_space["y"]}, walls_length)
            if free_space["shift_method"] == "plus":
                shifted_point = point + free_space["displacement_value"]
            elif free_space["shift_method"] == "minus":
                shifted_point = point - free_space["displacement_value"]
            else:
                raise Exception('Неправильно введенный метод')

            if shifted_point < 0:
                shifted_point = room_perimeter - abs(shifted_point)
            elif shifted_point > room_perimeter:
                shifted_point = abs(shifted_point) - room_perimeter
            # else:
            #     raise Exception('Неправильно переменные')

            return convert_line_to_coordinates(shifted_point, walls_length)

    def placing_in_coordinates(self, middle_point: dict, figure: dict, walls: dict) -> bool:
        """Функция проверки возможности резервирования места для мебели в комнате.

        Args:
            middle_point (dict): {"middle_point": {"x": 0, "y": 0}}
            figure (dict): координаты для мебели. {"north_west": {"x": 0, "y": 0},
                   "north_east": {"x": 0, "y": 0}, "south_west": {"x": 0, "y": 0}, "south_east": {"x": 0, "y": 0}}
            walls (dict): стены комнаты начиная от левой {"first_wall": 0, "second_wall": 0, "third_wall": 0, "fourth_wall":0}

        Returns:
            bool: True, если место зарезервировано, иначе False
        """


        # Определяем ширину и высоту объекта, чтобы передать ее в дальнейшем в corner_markings
        length_and_width = {"length": abs(figure["north_west"]["y"] - figure["south_west"]["y"])
                                    + abs(figure["north_west"]["y"] - figure["north_east"]["y"]),
                             "width": abs(figure["north_west"]["x"] - figure["south_west"]["x"])
                                    + abs(figure["north_west"]["x"] - figure["north_east"]["x"])}

        # Определения координат комнаты для работы определения принадлежности координат к конкретной стене
        room_coordinates = {"south_west": {"x": 0, "y": 0},
                            "north_west": {"x": 0, "y": walls["first_wall"]},
                            "north_east": {"x": walls["second_wall"], "y": walls["first_wall"]},
                            "south_east": {"x": walls["second_wall"], "y": 0}}

        # Функция определения стены по координатам для отправки ее в дальнейшем в corner_markings
        def wall_definition(dot: dict):
            if dot["y"] == 0:
                return 4
            elif dot["x"] == 0:
                return 1
            elif dot["y"] == room_coordinates["north_east"]["y"]:
                return 2
            elif dot["x"] == room_coordinates["north_east"]["x"]:
                return 3

        def displacement():
            nonlocal figure, middle_point, objects_counter, cycle_counter, cycle_border
            middle_point["x"], middle_point["y"] = self.middle_of_the_distance_on_the_wall(middle_point, walls).values()
            wall = wall_definition(middle_point)
            figure = self.corner_markings(length_and_width, middle_point, wall)
            objects_counter = 0
            cycle_counter += 1

        def rib_crossover_check(object, object_2):
            # Проверка на пересечение ребер в левом нижнем углу
            if object["south_east"]["y"] > object_2["south_east"]["y"] > object_2["south_west"]["y"] > object["north_east"]["y"] and \
               object_2["south_east"]["x"] > object["south_west"]["x"] > object["south_east"]["x"] > object_2["north_east"]["x"]:
                displacement()
            # Проверка на пересечение ребер в левом верхнем углу
            elif object_2["north_east"]["y"] > object["south_east"]["y"] > object["south_west"]["y"] > object_2["south_east"]["y"] and \
                 object["south_east"]["x"] > object_2["south_east"]["x"] > object_2["south_west"]["x"] > object["north_east"]["x"]:
                displacement()
            # Проверка на пересечение ребер в правом верхнем углу
            elif object["north_east"]["y"] > object_2["north_west"]["y"] > object_2["north_east"]["y"] > object["south_east"]["y"] and \
                 object_2["north_east"]["x"] > object["south_east"]["x"] > object["south_west"]["x"] > object_2["south_east"]["x"]:
                displacement()
            # Проверка на пересечение ребер в правом нижнем углу
            elif object_2["south_east"]["y"] > object["south_west"]["y"] > object["south_east"]["y"] > object_2["north_east"]["y"] and \
                 object["north_east"]["x"] > object_2["south_west"]["x"] > object_2["south_east"]["x"] > object["south_east"]["x"]:
                displacement()

        def corner_crossover_check(object, object_2):
            # Проверка на вхождение углов объектов в левом нижнем углу комнаты
            if object_2["south_west"]["x"] > object["south_east"]["x"] > object_2["north_west"]["x"] and \
               object_2["south_east"]["y"] > object["south_east"]["y"] > object_2["north_west"]["y"]:
                displacement()
            # Проверка на вхождение углов объектов в левом верхнем углу комнаты
            elif object_2["south_east"]["x"] > object["south_east"]["x"] > object_2["south_west"]["x"] and \
                 object_2["north_west"]["y"] > object["south_east"]["y"] > object_2["south_west"]["y"]:
                displacement()
            # Проверка на вхождение углов объектов в правом верхнем углу комнаты
            elif object_2["north_east"]["x"] > object["south_east"]["x"] > object_2["south_east"]["x"] and \
                 object_2["south_west"]["y"] > object["south_east"]["y"] > object_2["south_east"]["y"]:
                displacement()
            # Проверка на вхождение углов объектов в правом нижнем углу комнаты
            elif object_2["south_west"]["x"] > object["south_east"]["x"] > object_2["south_east"]["x"] and \
                 object_2["south_west"]["y"] > object["south_east"]["y"] > object_2["north_east"]["y"]:
                displacement()


        def layering_of_objects_check(object, object_2):
            for item in object.values():
                # Проверяем пересечение с другими объектами в комнате
                if object_2["north_west"]["x"] <= item["x"] <= object_2["north_east"]["x"] and \
                   object_2["south_east"]["y"] <= item["y"] <= object_2["north_east"]["y"]:
                    displacement()

                elif object_2["north_west"]["x"] >= item["x"] >= object_2["north_east"]["x"] and \
                     object_2["south_east"]["y"] >= item["y"] >= object_2["north_east"]["y"]:
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
            if figure["north_east"]["x"] > walls["second_wall"] \
            or figure["south_east"]["x"] > walls["second_wall"]:
                displacement()

            elif figure["north_east"]["y"] > walls["first_wall"] \
              or figure["south_east"]["y"] > walls["first_wall"]:
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
        self.coordinates.append(figure)
        return True

    def corner_markings(self, length_and_width: dict, center: dict, wall_number: int) -> dict:
        corners_coordinates = {"north_west": {"x": 0, "y": 0}, "north_east": {"x": 0, "y": 0},
                               "south_west": {"x": 0, "y": 0}, "south_east": {"x": 0, "y": 0}}

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

    # class DataVerificationAndImplementation(FurnitureArrangement):
    #
    #     def area_calculation(self, figure: Figure) -> float:
    #         "Метод вычисления площади фигуры."
    #         if figure.side_a == figure.side_c and figure.side_b == figure.side_d:
    #             area = figure.side_a * figure.side_b
    #             return area
    #
    #         else:
    #             raise IncorrectFigure("Неверно заданы размеры помещения!")
    #
    #     def area_monitoring(self, area: dict) -> bool:
    #         "Метод контроля допустимой общей площади мебели в помещении."
    #         if (area["area_furniture"] / area["area_room"]) > 0.75:
    #             raise LackSpace("Общая площадь мебели превышает площадь помещения!")
    #         return True
    #
    # def algorithm_activation(self, furniture: tuple, room_size: dict, random_switcher: bool):
    #     furniture_check = self.area_monitoring(db_operations(furniture))
    #     # надо дописать функции с возвратом данных из бд и переделать входящие данные для area_monitoring
    #
    #     if furniture_check is False:
    #         raise_area_error(False)
    #
    #     # прописать функцию ошибки с выводом во фронт
    #
    #     def activation_core(algorithm_type):
    #         counter = 1
    #         while counter != len(furniture):
    #             result_free_space = algorithm_type(db_operations(furniture))
    #             self.middle_of_the_distance_on_the_wall(result_free_space)
    #             draw_objects(self.coordinates)
    #             counter += 1
    #
    #     if random_switcher is True:
    #         # условные переменные вызова (пока что)
    #         activation_core(self.random_free_space_algorithm(db_operations(furniture)))
    #
    #     elif random_switcher is False:
    #         activation_core(self.free_space_algorithm(db_operations(furniture)))
    #

    def algorithm_activation(self, doors_and_windows: list, furniture: list, room_size: dict):
        # Определения координат комнаты для работы определения принадлежности координат к конкретной стене
        room_coordinates = {"south_west": {"x": 0, "y": 0},
                            "north_west": {"x": 0, "y": room_size["first_wall"]},
                            "north_east": {"x": room_size["second_wall"], "y": room_size["first_wall"]},
                            "south_east": {"x": room_size["second_wall"], "y": 0}}

        # Функция определения стены по координатам для отправки ее в дальнейшем в corner_markings
        def wall_definition(dot: dict):
            if dot["y"] == 0:
                return 4
            elif dot["x"] == 0:
                return 1
            elif dot["y"] == room_coordinates["north_east"]["y"]:
                return 2
            elif dot["x"] == room_coordinates["north_east"]["x"]:
                return 3
        for item in doors_and_windows:
            self.coordinates.append(item)

        for item in furniture:
            result_free_space = self.free_space_algorithm(self.coordinates)
            result_middle_distance = self.middle_of_the_distance_on_the_wall(result_free_space, room_size)
            result_wall_definition = wall_definition(result_middle_distance)
            result_corner_markings = self.corner_markings(item, result_middle_distance, result_wall_definition)
            self.placing_in_coordinates(result_middle_distance, result_corner_markings, room_size)

        create_picture.create_rectangles(self.coordinates)
        print(self.coordinates)