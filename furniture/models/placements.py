from django.db import models

from furniture.models.base import PlacementCoordinates
from furniture.validators import minimum_len_width_validator


class FurniturePlacement(PlacementCoordinates):
    """Размещение мебели в помещении."""

    furniture = models.ForeignKey(
        'Furniture',
        on_delete=models.CASCADE,
        verbose_name='Мебель',
        related_name='placements',
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
    """Модель размещения двери в помещении."""

    width = models.PositiveIntegerField(
        'Ширина двери',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator,),
    )
    open_inside = models.BooleanField(
        'Направление открытия двери внутрь помещения',
        help_text='Открытие в помещении - 1, из помещения - 0',
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
