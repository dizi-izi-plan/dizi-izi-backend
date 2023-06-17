from user_app import models


def get_furniture(name: str) -> tuple[int, int]:
    """Возвращает ширину и длину мебели."""
    furniture = models.Furniture.objects.get(name=name)
    return (furniture.width, furniture.lenght)


def set_furniture_coordinates(
    name: str,
    x_coordinate: int,
    y_coordinate: int,
) -> None:
    """Назначает координаты для мебели."""
    furniture = models.Furniture.objects.get(name=name)
    furniture.x_coordinate = x_coordinate
    furniture.y_coordinate = y_coordinate
