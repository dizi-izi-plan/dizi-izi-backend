
def corner_markings(length_and_width: dict, center: dict, wall_number: int) -> dict:
    """Эта функция необходима, чтобы, имея центр объекта и его размеры, относительно
    конкретной стены обозначить его углы координатами.
    Args:
        length_and_width: dict: ширина и длина объекта {length: 1, width: 1}
        center (dict): центр стороны объекта, примыкающей к стене {"x": 0, "y": 0},
        wall_number: сторона комнаты с учетом, что левая сторона первая, а дальнейшие нумеруются по часовой стрелке
    Returns:
        dict: словарь с координатами углов
                {
                "north_west": {"x": 0, "y": 0},
                "north_east": {"x": 0, "y": 0},
                "south_west": {"x": 0, "y": 0},
                "south_east": {"x": 0, "y": 0},
                }
    """

    corners_coordinates = {
        "north_west": {"x": 0, "y": 0},
        "north_east": {"x": 0, "y": 0},
        "south_west": {"x": 0, "y": 0},
        "south_east": {"x": 0, "y": 0},
    }

    # последующие шесть строчек нужны для визуального сокращения кода
    north_east = corners_coordinates["north_east"]
    north_west = corners_coordinates["north_west"]
    south_east = corners_coordinates["south_east"]
    south_west = corners_coordinates["south_west"]

    length = length_and_width["length"]
    width = length_and_width["width"]

    # так как примыкающая сторона объекта смещает внутренние стороны света углов, то относительно каждой
    # стороны координаты вычисляются по-разному
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
