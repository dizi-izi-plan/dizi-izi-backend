def rib_crossover_check(object, object_2):
    """

    Args:

    Returns:

    """

    # Проверка на пересечение ребер в левом нижнем углу
    if (object["south_east"]["y"] > object_2["south_east"]["y"]
            > object_2["south_west"]["y"] > object["north_east"]["y"]
            and object_2["south_east"]["x"] > object["south_west"]["x"]
            > object["south_east"]["x"] > object_2["north_east"]["x"]):
        return False
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
        return False
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
        return False
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
        return False
    return True


def corner_crossover_check(object, object_2):
    """

    Args:

    Returns:

    """

    # Проверка на вхождение углов объектов в левом нижнем углу комнаты
    if (
            object_2["south_west"]["x"]
            > object["south_east"]["x"]
            > object_2["north_west"]["x"]
            and object_2["south_east"]["y"]
            > object["south_east"]["y"]
            > object_2["north_west"]["y"]
    ):
        return False
    # Проверка на вхождение углов объектов в левом верхнем углу комнаты
    elif (
            object_2["south_east"]["x"]
            > object["south_east"]["x"]
            > object_2["south_west"]["x"]
            and object_2["north_west"]["y"]
            > object["south_east"]["y"]
            > object_2["south_west"]["y"]
    ):
        return False
    # Проверка на вхождение углов объектов в правом верхнем углу комнаты
    elif (
            object_2["north_east"]["x"]
            > object["south_east"]["x"]
            > object_2["south_east"]["x"]
            and object_2["south_west"]["y"]
            > object["south_east"]["y"]
            > object_2["south_east"]["y"]
    ):
        return False
    # Проверка на вхождение углов объектов в правом нижнем углу комнаты
    elif (
            object_2["south_west"]["x"]
            > object["south_east"]["x"]
            > object_2["south_east"]["x"]
            and object_2["south_west"]["y"]
            > object["south_east"]["y"]
            > object_2["north_east"]["y"]
    ):
        return False

    return True


def layering_of_objects_check(object, object_2):
    """

    Args:

    Returns:

    """

    items = [
        object["north_west"],
        object["north_east"],
        object["south_west"],
        object["south_east"],
    ]

    for item in items:
        # Проверяем пересечение с другими объектами в комнате
        if (object_2["north_west"]["x"] <= item["x"] <= object_2["north_east"]["x"]
                and object_2["south_east"]["y"] <= item["y"] <= object_2["north_east"]["y"]):
            return False

        elif (object_2["north_west"]["x"] >= item["x"] >= object_2["north_east"]["x"]
              and object_2["south_east"]["y"] >= item["y"] >= object_2["north_east"]["y"]):
            return False

        elif (object_2["north_west"]["x"] <= item["x"] <= object_2["north_east"]["x"]
              and object_2["south_east"]["y"] <= item["y"] <= object_2["south_west"]["y"]):
            return False

        elif (object_2["north_west"]["x"] >= item["x"] >= object_2["north_east"]["x"]
              and object_2["south_east"]["y"] >= item["y"] >= object_2["south_west"]["y"]):
            return False

    return True


def room_crossover_check(figure, walls):
    if figure["north_east"]["x"] > walls["second_wall"] \
            or figure["south_east"]["x"] > walls["second_wall"] \
            or figure["south_west"]["x"] > walls["second_wall"] \
            or figure["north_west"]["x"] > walls["second_wall"]:
        return False


    elif figure["north_east"]["y"] > walls["first_wall"] \
            or figure["south_east"]["y"] > walls["first_wall"] \
            or figure["south_west"]["y"] > walls["first_wall"] \
            or figure["north_west"]["y"] > walls["first_wall"]:
        return False

    elif figure["south_west"]["x"] < 0 or figure["south_west"]["y"] < 0:
        return False

    return True


def checks(figure, figure_2, walls):
    # Проверяем пересечение противоположных объектов
    if not layering_of_objects_check(figure, figure_2):
        return False
    # Проверяем объекты на поглощение друг друга
    if not layering_of_objects_check(figure_2, figure):
        return False
    # Проверка пересечения ребер, если объекты находятся с одной и с другой стороны друг от друга
    if not rib_crossover_check(figure, figure_2):
        return False
    if not rib_crossover_check(figure_2, figure):
        return False
    # Проверяем на вхождение углов объектов внутрь друг друга
    if not corner_crossover_check(figure, figure_2):
        return False
    if not corner_crossover_check(figure_2, figure):
        return False
    # Проверяем, что мебель не выходит за пределы комнаты
    if not room_crossover_check(figure, walls):
        return False
    return True
