from django.db import models

from furniture.models.base import PlacementCoordinates
from furniture.validators import minimum_len_width_validator


class FurniturePlacement(PlacementCoordinates):
    """Furniture placement in a room."""

    furniture = models.ForeignKey(
        'Furniture',
        on_delete=models.CASCADE,
        verbose_name='Мебель',
        related_name='placements',
    )
    room_layout = models.ForeignKey(
        'RoomLayout',
        on_delete=models.CASCADE,
        verbose_name='Планировка',
        related_name='furniture_placements',
    )

    class Meta:
        verbose_name = 'Размещение мебели в помещении'
        verbose_name_plural = 'Размещение мебели в помещении'

    def __str__(self):
        return f'{self.furniture.name} расположена в {self.room}'


class PowerSocketPlacement(PlacementCoordinates):
    """Модель размещения розетки в помещении."""

    class Meta:
        verbose_name = 'Розетка в помещении'
        verbose_name_plural = 'Розетки в помещении'

    def __str__(self) -> str:
        return f'Розетка расположена в {self.room}'


class DoorPlacement(PlacementCoordinates):
    """Model of door placement in a room."""

    DOOR_OPENING_CHOICES = [
        ("inside_left", "Внутрь влево"),
        ("inside_right", "Внутрь вправо"),
        ("outside_left", "Наружу влево"),
        ("outside_right", "Наружу вправо"),
    ]

    width = models.PositiveIntegerField(
        verbose_name='Ширина двери',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator,),
    )
    height = models.PositiveIntegerField(
        verbose_name='Высота двери',
        help_text='Высота в мм',
        validators=(minimum_len_width_validator,),
    )
    open_direction = models.CharField(
        verbose_name='Направление открытия двери',
        help_text='Как открывается дверь',
        choices=DOOR_OPENING_CHOICES,
    )

    class Meta:
        verbose_name = 'Дверь в помещении'
        verbose_name_plural = 'Двери в помещении'

    def __str__(self) -> str:
        return f'Дверь расположена в {self.room}'


class WindowPlacement(PlacementCoordinates):
    """Модель размещения окна в помещении."""

    length = models.PositiveIntegerField(
        'Длина окна',
        help_text='Длина в мм',
        validators=(minimum_len_width_validator,),
    )
    width = models.PositiveIntegerField(
        'Ширина окна',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator,),
    )

    class Meta:
        verbose_name = 'Окно в помещении'
        verbose_name_plural = 'Окна в помещении'

    def __str__(self) -> str:
        return f'Окно расположено в {self.room}'
