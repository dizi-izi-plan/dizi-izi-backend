from django.db import models

from furniture.models.abstract_models import AbstractRoomPlacement
from furniture.validators import minimum_len_width_validator


class DoorPlacement(AbstractRoomPlacement):
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


class WindowPlacement(AbstractRoomPlacement):
    """Model of window placement in a room."""

    height = models.PositiveIntegerField(
        verbose_name='Высота окна',
        help_text='Высота в мм',
        validators=(minimum_len_width_validator,),
    )
    width = models.PositiveIntegerField(
        verbose_name='Ширина окна',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator,),
    )

    class Meta:
        verbose_name = 'Окно в помещении'
        verbose_name_plural = 'Окна в помещении'

    def __str__(self) -> str:
        return f'Окно расположено в {self.room}'
