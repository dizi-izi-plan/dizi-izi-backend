from django.db import models
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import AbstractUser
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


# class User(AbstractUser):
#     """Модель пользователя."""
#     pass


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
    image = models.ImageField(
        verbose_name='Изображение мебели',
        upload_to='furniture/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'

    def __str__(self) -> str:
        return f'{self.name}'


class RoomCoordinates(models.Model):
    """Абстарктная модель с указателем на помещение и координаты."""
    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        verbose_name='Комната',
        related_name='%(class)ss'
    )
    nw_coordinate = models.PositiveIntegerField(
        verbose_name='Координата north_west',
        default=0
    )
    ne_coordinate = models.PositiveIntegerField(
        verbose_name='Координата north-east',
        default=0
    )
    sw_coordinate = models.PositiveIntegerField(
        verbose_name='Координата south-west',
        default=0
    )
    se_coordinate = models.PositiveIntegerField(
        verbose_name='Координата south-east',
        default=0
    )

    class Meta:
        abstract = True


class Placement(RoomCoordinates):
    """Размещение мебели в помещении."""
    furniture = models.ForeignKey(
        'Furniture',
        on_delete=models.CASCADE,
        verbose_name='Мебель',
    )

    class Meta:
        verbose_name = 'Размещение мебели в помещении'
        verbose_name_plural = 'Размещение мебели в помещении'

    def __str__(self):
        return (
            f'{self.furniture.name} расположена в {self.room} '
            f'в координатах {self.nw_coordinate}, {self.ne_coordinate}, '
            f'{self.sw_coordinate}, {self.se_coordinate}'
        )


class Room(models.Model):
    """Модель помещения."""
    name = models.CharField(
        'Название помещения',
        max_length=128
    )
    first_wall = models.PositiveIntegerField(
        'Длина 1 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator, )
    )
    second_wall = models.PositiveIntegerField(
        'Длина 2 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator, )
    )
    third_wall = models.PositiveIntegerField(
        'Длина 3 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator, )
    )
    fourth_wall = models.PositiveIntegerField(
        'Длина 4 стены',
        help_text='Длина стены в мм',
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
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    def __str__(self) -> str:
        return f'{self.name} пользователя {self.user}'


class PowerSocket(RoomCoordinates):
    """Модель размещения розетки в помещении."""
    class Meta:
        verbose_name = 'Розетка в помещении'
        verbose_name_plural = 'Розетки в помещении'

    def __str__(self) -> str:
        return f'Розетка расположена в {self.room}'


class Door(RoomCoordinates):
    """Модель размещения двери в помещении."""
    width = models.PositiveIntegerField(
        'Ширина двери',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator, )
    )
    open_inside = models.BooleanField(
        'Направление открытия двери внутрь помещения',
        help_text='Открытие в помещении - 1, из помещения - 0'
    )

    class Meta:
        verbose_name = 'Дверь в помещении'
        verbose_name_plural = 'Двери в помещении'

    def __str__(self) -> str:
        return f'Дверь расположена в {self.room}'


class Window(RoomCoordinates):
    """Модель размещения окна в помещении."""
    length = models.PositiveIntegerField(
        'Длина окна',
        help_text='Длина в мм',
        validators=(minimum_len_width_validator, )
    )
    width = models.PositiveIntegerField(
        'Ширина окна',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator, )
    )

    class Meta:
        verbose_name = 'Окно в помещении'
        verbose_name_plural = 'Окна в помещении'

    def __str__(self) -> str:
        return f'Окно расположено в {self.room}'
