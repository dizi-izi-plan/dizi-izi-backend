from django.db import models

from furniture.models.abstract_models import AbstractLayoutPlacement


class FurniturePlacement(AbstractLayoutPlacement):
    """Furniture placement in a room."""

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
        return f'{self.furniture.name} расположена в {self.room_layout}'


class PowerSocketPlacement(AbstractLayoutPlacement):
    """Socket placement in a room."""

    class Meta:
        verbose_name = 'Розетка в помещении'
        verbose_name_plural = 'Розетки в помещении'

    def __str__(self) -> str:
        return f'Розетка расположена в {self.room}'
