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
        distances = {}

        for i in range(len(objects)):
            first_object = objects[i]
            second_object = objects[(i + 1) % len(objects)]  # Циклический переход к первому объекту
            self._calculate_and_store_distance(first_object, second_object, distances)

        return distances[max(distances)]

    def _calculate_and_store_distance(self, first_object, second_object, distances):

        first_right_corner = self._get_right_corner(first_object)
        second_left_corner = self._get_left_corner(second_object)

        first_point = self.convert_coordinates_to_line(
            first_object[first_right_corner], self.room.walls_length,
        )
        second_point = self.convert_coordinates_to_line(
            second_object[second_left_corner], self.room.walls_length,
        )

        distance = self._calculate_linear_distance(first_point, second_point)

        distances[distance] = {
            "left_corner": first_object[first_right_corner],
            "right_corner": second_object[second_left_corner],
        }
        # расстояния могут быть одинаковые, но нам по сути неважно какой
        # из вариантов брать, а значит мы можем просто перезаписать ключ
        # словаря

    def _get_right_corner(self, obj):
        if obj["north_east"] in self.room.room_coordinates_tuple:
            return "south_east"
        else:
            return "north_east"

    def _get_left_corner(self, obj):
        if obj["north_west"] in self.room.room_coordinates_tuple:
            return "south_west"
        else:
            return "north_west"

    def _calculate_linear_distance(self, first_point, second_point):
        wall_perimeter = self.room.wall_perimetr
        if second_point >= first_point:
            distance = second_point - first_point
        else:
            distance = second_point + (wall_perimeter - first_point)
        return distance

    def placing_in_coordinates(
        self,
        data: dict,
        figure: dict,
        walls: dict,
        object_attributes: dict,
    ):
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

        """

        cycle_counter = 0
        max_attempts = self.room.wall_perimetr
        # Задаем данные для дальнейшей их отправки в функцию переноса объекта
        # переменная необходима для обозначения стартовой точки, относительно
        # которой будет смещение
        data["displacement_start"] = 0
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
        while cycle_counter < max_attempts:
            if self._check_collisions(figure, walls):
                break
            else:
                data, figure = self._displace_furniture(data, object_attributes)
                cycle_counter += 1
        else:
            raise Exception("Превышено число попыток на размещение")

        final_point = self.convert_coordinates_to_line(data, self.room.walls_length)
        return final_point, figure

    def _check_collisions(self, figure, walls):
        for existing_figure in self.room.room_objects_coordinates:
            if not checks(figure, existing_figure, walls):
                return False
        return True

    def _displace_furniture(self, data, object_attributes):
        data["displacement_start"] += data["displacement_value"]

        data["x"], data["y"] = self.offset(
            data,
            self.room.wall_perimetr,
            self.room.walls_length,
        ).values()
        wall = self.room.wall_definition(data)
        furniture_obj = Furniture(
            length=object_attributes["length"],
            width=object_attributes["width"],
            center=data,
            wall_number=wall,
        )
        figure = furniture_obj.corners_coordinates

        return data, figure

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
