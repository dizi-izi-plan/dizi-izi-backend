from typing import Union


def convert_coordinates_to_line(
        coordinates: dict, walls_length,
) -> Union[float, int]:
    """Функция преобразует координаты в точку на прямой.

    Args:
    Returns:

    """
    if coordinates["x"] == 0:
        return coordinates["y"]
    elif coordinates["y"] == walls_length[0]:
        return walls_length[0] + coordinates["x"]
    elif coordinates["x"] == walls_length[1]:
        return sum(walls_length[:3]) - coordinates["y"]
    return sum(walls_length) - coordinates["x"]


def convert_line_to_coordinates(
        dot: Union[float, int], walls_length, wall_perimetr,
) -> dict:
    """Функция преобразует точку на прямой в координаты."""
    if 0 <= dot <= walls_length[0]:
        return {"x": 0, "y": dot}
    elif walls_length[0] < dot <= sum(walls_length[:2]):
        return {"x": dot - walls_length[0], "y": walls_length[0]}
    elif sum(walls_length[:2]) < dot <= sum(walls_length[:3]):
        return {"x": walls_length[1], "y": sum(walls_length[:3]) - dot}
    elif sum(walls_length[:3]) < dot <= wall_perimetr:
        return {"x": wall_perimetr - dot, "y": 0}
    raise Exception(
        "Ошибка данных, нет возможности разместить среднюю точку на одной "
        "из стен комнаты.", "Входящие данные:",
        dot,
        walls_length,
        wall_perimetr,
    )