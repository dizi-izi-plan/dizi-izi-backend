import random
from .crossover_checks import checks
from .offset_finder_convert import MiddlePointAndShift

from .furniture import Furniture


class FurnitureArrangement(MiddlePointAndShift):
    def __init__(self, room):
        free_space = []
        # хранение расстояний между мебелью через запятую (в виде координат)
        self.free_space = free_space
        self.room = room

    def free_space_algorithm(self, objects: list) -> dict:
        """На вход подается список с координатами углов объектов.

        Координаты между друг другом минусим, находим по ближайшим
        неприлегающим углам расстояние по модулю в виде гипотенузы
        (вычитание по иксу -- это один катет, вычитание по игрику -- другой).
        И записыванием самое большое расстояние в переменную. Углы разбиты по
        сторонам света: north_west, north-east, south-west, south-east.
        Отдельно так же идет значение и длина стены
        "walls_length": {"first_wall": 1, "second_wall": 2, "third_wall": 1,
        "fourth_wall": 2}
        """
        length = {}
        counter = 1

        def core_and_output(first_object, second_object):

            first_right_corner = "north_east"
            second_left_corner = "north_west"

            if first_object["north_east"] in self.room.room_coordinates_tuple:
                first_right_corner = "south_east"
            if (
                second_object[counter]["north_west"]
                in self.room.room_coordinates_tuple
            ):
                second_left_corner = "south_west"

            first_point = self.convert_coordinates_to_line(
                first_object[first_right_corner], self.room.walls_length,
            )
            second_point = self.convert_coordinates_to_line(
                second_object[counter][second_left_corner], self.room.walls_length,
            )
            distance = 0
            if second_point >= first_point:
                distance = second_point - first_point
            elif second_point < first_point:
                distance = second_point + (self.room.wall_perimetr - first_point)

            length[distance] = {
                "left_corner": first_object[first_right_corner],
                "right_corner": second_object[counter][second_left_corner],
            }
            # расстояния могут быть одинаковые, но нам по сути неважно какой
            # из вариантов брать, а значит мы можем просто перезаписать ключ
            # словаря

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
        """Проверка возможности резервирования места для мебели в комнате.

        Args:
            object_attributes:
            data:
            figure: координаты для мебели.
            {"north_west": {"x": 0, "y": 0},
            "north_east": {"x": 0, "y": 0},
            "south_west": {"x": 0, "y": 0},
            "south_east": {"x": 0, "y": 0}}
            walls: стены комнаты начиная от левой
            {"first_wall": 0,
            "second_wall": 0,
            "third_wall": 0,
            "fourth_wall":0}
            length_and_width: ширина и длина располагаемого объекта

        Returns:
            bool: True, если место зарезервировано, иначе False
        """

        def displacement():
            nonlocal figure, data, objects_counter, cycle_counter, cycle_border, displacement_start
            displacement_start += data["displacement_value"]

            data["x"], data["y"] = self.offset(
                data,
                self.room.wall_perimetr,
                self.room.walls_length,
            ).values()
            wall = self.room.wall_definition(data)
            figure = Furniture.corner_markings(object_attributes, data, wall)
            objects_counter = 0
            cycle_counter += 1

        # Задаем переменные, чтобы определить случаи для выхода из цикла
        # переменная необходимая для учета всех объектов, относительно которых
        # делается проверка на пересечение
        objects_counter = 0
        # переменная для подсчета количества циклов, дабы они не были
        # бесконечным
        cycle_counter = 0
        # переменная, указывающая при каком значении будет критическая ошибка
        # о невозможности размещения
        cycle_border = self.room.wall_perimetr
        # Переменная, выводящая из общего цикла при не пересечении объектов
        breaker = 0

        # Задаем данные для дальнейшей их отправки в функцию переноса объекта
        # переменная необходима для обозначения стартовой точки, относительно
        # которой будет смещение
        displacement_start = 0
        # указываем сторону для начального смещения
        data["shift_method"] = "plus"

        # указываем значение на которое будет смещаться объект в зависимости
        # от разрядности периметра
        if self.room.wall_perimetr < 100:
            data["displacement_value"] = 1
        elif self.room.wall_perimetr < 1000:
            data["displacement_value"] = 10
        elif self.room.wall_perimetr < 10000:
            data["displacement_value"] = 100
        elif self.room.wall_perimetr < 100000:
            data["displacement_value"] = 1000

        # сам цикл, в котором мы пытаемся разметить объект заданное количество
        # циклов и проверяем пересечения со всеми объектами
        while cycle_counter < cycle_border and objects_counter < len(
            self.room.coordinates,
        ):
            figure_2 = self.room.coordinates[objects_counter]
            if checks(figure, figure_2, walls):
                # добавляем единицу брейкеру за каждый прошедший проверки
                # пересечения объект, чтобы организовать выход из цикла
                breaker += 1
                objects_counter += 1
            else:
                displacement()
            # если пересечения со всеми объектами были проверены успешно, то
            # выходим из цикла
            if breaker >= len(self.room.coordinates):
                break
            if cycle_counter >= cycle_border:
                raise Exception("Превышено число попыток на размещение")

            breaker = 1

        # Если все проверки прошли, добавляем координаты мебели в словарь
        # coordinates
        final_point = self.convert_coordinates_to_line(data, self.room.walls_length)
        # Тут один сплошной вопрос, должно быть bool!!!
        return (
            self.convert_coordinates_to_line(data, self.room.walls_length),
            figure,
        )

    def shuffle_furniture(self, furniture: list, mode: str) -> list:
        """Функция меняет позиции внутри списка мебели местами для
        предоставления пользователю других результатов при повторной генерации

        Args:
            furniture: список мебели, необходимой для перестановки
            mode: степень серьезности перестановки

        Returns:
            list: список мебели с перемещенными позициями

        """

        def light_or_medium_shuffle(mode: str) -> list:
            """Light mode shuffle have swap position with one step.

            Medium mode shuffle have swap position with two steps.
            """
            if mode == "light":
                step = 1
            if mode == "medium":
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
        if mode == "hard":
            hard_shuffle()
            return furniture
        if mode == "light" or "medium":
            return light_or_medium_shuffle(mode)
