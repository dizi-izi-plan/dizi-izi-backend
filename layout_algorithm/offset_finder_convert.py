from typing import Union


class MiddlePointAndShift:
    """
    Функция для нахождения средней точки в оставшемся пустом пространстве
    комнаты. Получает на вход координаты точек и длины стен.
    Возвращает координаты средней точки.

    Args:

    Returns:

    """

    def convert_coordinates_to_line(
            self,
            coordinates: dict,
            walls_length
    ) -> Union[float, int]:
        """Функция преобразует координаты в точку на прямой.

        Args:
        Returns:

        """
        if coordinates['x'] == 0:
            return coordinates['y']
        elif coordinates['y'] == walls_length[0]:
            return walls_length[0] + coordinates['x']
        elif coordinates['x'] == walls_length[1]:
            return sum(walls_length[:3]) - coordinates['y']
        return sum(walls_length) - coordinates['x']

    def convert_line_to_coordinates(
            self, dot: Union[float, int], walls_length, wall_perimetr) -> dict:
        """Функция преобразует точку на прямой в координаты

    Args:

    Returns:

    """

        if 0 <= dot <= walls_length[0]:
            return {'x': 0, 'y': dot}
        elif walls_length[0] < dot <= sum(walls_length[:2]):
            return {'x': dot - walls_length[0],
                    'y': walls_length[0]}
        elif sum(walls_length[:2]) < dot <= sum(walls_length[:3]):
            return {'x': walls_length[1],
                    'y': sum(walls_length[:3]) - dot}
        elif sum(walls_length[:3]) < dot <= wall_perimetr:
            return {'x': wall_perimetr - dot, 'y': 0}
        raise Exception(
            'Ошибка данных, нет возможности разместить среднюю точку на одной из стен комнаты.', 
            'Входящие данные:', dot, walls_length, wall_perimetr
        )

    def middle_point_finder(self, points: dict, wall_perimetr, walls_length):
        """

        Args:

        Returns:

        """

        point_1 = self.convert_coordinates_to_line(points['left_corner'], walls_length)
        point_2 = self.convert_coordinates_to_line(points['right_corner'], walls_length)
        middle_point = (
            (point_2 + point_1) / 2
            if point_1 < point_2
            else (point_2 + point_1 + wall_perimetr) / 2
        )
        if middle_point > wall_perimetr:
            middle_point = middle_point - wall_perimetr
        return self.convert_line_to_coordinates(middle_point, walls_length, wall_perimetr)

    def offset(self, data, wall_perimetr, walls_length):
        """

        Args:

        Returns:

        """

        point = self.convert_coordinates_to_line({"x": data["x"], "y": data["y"]}, walls_length)  # отправить дотс целиком
        if data["shift_method"] == "plus":
            shifted_point = point + data["displacement_value"]
        elif data["shift_method"] == "minus":
            shifted_point = point - data["displacement_value"]
        else:
            raise Exception('Неправильно введенный метод')

        if shifted_point < 0:
            shifted_point = wall_perimetr - abs(shifted_point)
        elif shifted_point > wall_perimetr:
            shifted_point = abs(shifted_point) - wall_perimetr
        # else:
        #     raise Exception('Неправильно переменные')

        return self.convert_line_to_coordinates(shifted_point, walls_length, wall_perimetr)
