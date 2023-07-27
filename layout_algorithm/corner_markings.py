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


def magnet_to_corners(
        corners_coordinates: dict,
        center: dict,
        walls_len: tuple,
        wall_number: int,
        wall_perimetr: int
) -> dict:
    """
    Функция для смещения мебели к углам,
    если расстояние до угла менее max_shift.
    """

    new_center = center.copy()

    # Переменная MAX_SHIFT меняет значение в зависимости от единиц измерения
    if wall_perimetr < 100:
        max_shift: float = 0.5  # метры
    elif wall_perimetr < 10000:
        max_shift: float = 50  # сантиметры
    elif wall_perimetr < 100000:
        max_shift: float = 500  # миллиметры
    else:
        raise ValueError('Размер стены указан неверно')

    if wall_number == 1:
        if corners_coordinates["north_west"]["y"] <= max_shift:
            shift = corners_coordinates["north_west"]["y"]
            new_center["y"] -= shift
        elif walls_len[0] - corners_coordinates["north_east"]["y"] <= max_shift:
            shift = walls_len[0] - corners_coordinates["north_east"]["y"]
            new_center["y"] += shift

    elif wall_number == 2:
        if corners_coordinates["north_west"]["x"] <= max_shift:
            shift = corners_coordinates["north_west"]["x"]
            new_center["x"] -= shift
        elif walls_len[1] - corners_coordinates["north_east"]["x"] <= max_shift:
            shift = walls_len[1] - corners_coordinates["north_east"]["x"]
            new_center["x"] += shift

    elif wall_number == 3:
        if walls_len[2] - corners_coordinates["north_west"]["y"] <= max_shift:
            shift = walls_len[2] - corners_coordinates["north_west"]["y"]
            new_center["y"] += shift
        elif corners_coordinates["north_east"]["y"] <= max_shift:
            shift = corners_coordinates["north_east"]["y"]
            new_center["y"] -= shift

    elif wall_number == 4:
        if walls_len[3] - corners_coordinates["north_west"]["x"] <= max_shift:
            shift = walls_len[3] - corners_coordinates["north_west"]["x"]
            new_center["x"] += shift
        elif corners_coordinates["north_east"]["x"] <= max_shift:
            shift = corners_coordinates["north_east"]["x"]
            new_center["x"] -= shift

    else:
        raise ValueError('Номер стены указан неверно')

    return new_center
