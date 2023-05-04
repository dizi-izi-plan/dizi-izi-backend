from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


def minimum_len_width_validator(value):
    """Проверка минимального значения для длины и ширины мебели."""
    min_value_len_width = 1
    if value < min_value_len_width:
        raise ValidationError(
            (
                f'Минимальное значение для длины '
                f'и ширины равно {min_value_len_width}'
            )
        )
    return value


class User(AbstractUser):
    """Модель пользователя."""
    pass


class Furniture(models.Model):
    """Модель мебели"""
    name = models.CharField(
        'Наименование мебели',
        max_length=128,
        unique=True
    )
    name_english = models.CharField(
        'Наименование мебели на английском языке',
        max_length=128,
        unique=True
    )
    length = models.PositiveIntegerField(
        'Длина мебели',
        help_text='Длина в мм',
        validators=(minimum_len_width_validator, )
    )
    width = models.PositiveIntegerField(
        'Ширина мебели',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator, )
    )
    length_access = models.PositiveIntegerField(
        'Длина мебели c зоной подхода',
        help_text='Длина c зоной подхода в мм',
        validators=(minimum_len_width_validator, )
    )
    width_access = models.PositiveIntegerField(
        'Ширина мебели c зоной подхода',
        help_text='Ширина c зоной подхода в мм',
        validators=(minimum_len_width_validator, )
    )

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'

    def __str__(self) -> str:
        return f'{self.name}'


class Placement(models.Model):
    """Размещение мебели в комнате."""
    furniture = models.ForeignKey(
        'Furniture',
        on_delete=models.CASCADE,
        verbose_name='Мебель',
    )
    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        verbose_name='Комната',
        related_name='room_placement'
    )
    x_coordinate = models.PositiveIntegerField(
        verbose_name='Координата мебели X',
        default=0
    )
    y_coordinate = models.PositiveIntegerField(
        verbose_name='Координата мебели Y',
        default=0
    )

    class Meta:
        verbose_name = 'Связь размещения мебели для пользователя'
        verbose_name_plural = 'Связи размещения мебели для пользователя'

    def __str__(self) -> str:
        return (
            f'{self.furniture.name} расположена  в {self.room}'
            f'в координатах {self.x_coordinate}, {self.y_coordinate}'
        )


class Room(models.Model):
    """Модель помещения."""
    name = models.CharField(
        'Название комнаты',
        max_length=128
    )
    length = models.FloatField(
        'Длина комнаты',
        help_text='Длина в мм',
        validators=(minimum_len_width_validator, )
    )
    width = models.FloatField(
        'Ширина комнаты',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator, )
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='Пользователь'
    )
    furniture_placement = models.ManyToManyField(
        'Furniture',
        through='Placement'
    )

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self) -> str:
        return (
            f'{self.name} пользователя {self.user}'
        )


class PowerSocket(models.Model):
    """Модель размещения розетки в комнате."""
    room = models.ForeignKey(
        'Room',
        verbose_name='Комната',
        help_text='Комната, где размещена розетка',
        on_delete=models.CASCADE,
        related_name='power_sockets'
    )
    x_coordinate = models.PositiveIntegerField(
        verbose_name='Координата розетки X',
        default=0
    )
    y_coordinate = models.PositiveIntegerField(
        verbose_name='Координата розетки Y',
        default=0
    )


class Door(models.Model):
    """Модель размещения двери в комнате."""
    room = models.ForeignKey(
        'Room',
        verbose_name='Комната',
        help_text='Комната, где размещена дверь',
        on_delete=models.CASCADE,
        related_name='doors'
    )
    width = models.PositiveIntegerField(
        'Ширина двери',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator, )
    )
    x_coordinate = models.PositiveIntegerField(
        verbose_name='Координата двери X',
        default=0
    )
    y_coordinate = models.PositiveIntegerField(
        verbose_name='Координата двери Y',
        default=0
    )
    open_inside = models.BooleanField(
        'Направление открытия двери',
        help_text='Открытие в комнату - 1, из комнаты - 0'
    )


class Window(models.Model):
    """Модель размещения окна в комнате."""
    room = models.ForeignKey(
        'Room',
        verbose_name='Комната',
        help_text='Комната, где размещено окно',
        on_delete=models.CASCADE,
        related_name='windows'
    )
    height = models.PositiveIntegerField(
        'Высота окна',
        help_text='Высота в мм',
        validators=(minimum_len_width_validator, )
    )
    width = models.PositiveIntegerField(
        'Ширина окна',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator, )
    )
    x_coordinate = models.PositiveIntegerField(
        verbose_name='Координата окна X',
        default=0
    )
    y_coordinate = models.PositiveIntegerField(
        verbose_name='Координата окна Y',
        default=0
    )
