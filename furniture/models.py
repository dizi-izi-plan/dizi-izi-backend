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
    x_coordinate = models.FloatField(
        verbose_name='Координата мебели X',
        default=0
    )
    y_coordinate = models.FloatField(
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