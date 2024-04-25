from django.conf import settings
from django.db import models

from furniture.validators import minimum_len_width_validator


class RoomType(models.Model):
    """Типы комнат для мебели."""

    name = models.CharField(
        verbose_name='Наименование комнаты',
        unique=True,
        max_length=128,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Furniture(models.Model):
    """Модель мебели."""

    name = models.CharField(
        'Наименование мебели',
        max_length=settings.MAX_LENGTH_FURNITURE_NAME,
        unique=True,
    )
    name_english = models.CharField(
        'Наименование мебели на английском языке',
        max_length=128,
        unique=True,
    )
    length = models.PositiveIntegerField(
        'Длина мебели',
        help_text='Длина в мм',
        validators=(minimum_len_width_validator,),
    )
    width = models.PositiveIntegerField(
        'Ширина мебели',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator,),
    )
    length_access = models.PositiveIntegerField(
        'Длина мебели c зоной подхода',
        help_text='Длина c зоной подхода в мм',
        validators=(minimum_len_width_validator,),
    )
    width_access = models.PositiveIntegerField(
        'Ширина мебели c зоной подхода',
        help_text='Ширина c зоной подхода в мм',
        validators=(minimum_len_width_validator,),
    )
    image = models.ImageField(
        verbose_name='Изображение мебели',
        upload_to='furniture/',
        blank=True,
        null=True,
    )
    type_of_rooms = models.ForeignKey(
        "RoomType",
        on_delete=models.CASCADE,
        related_name='furniture',
        verbose_name='Комната',
        blank=False,
        null=False,
    )
    power_socket_type = models.CharField(
        'Тип электроточки',
        max_length=settings.MAX_LENGTH_FURNITURE_NAME,
        unique=False,
    )
    first_power_socket_height = models.IntegerField(
        'Высота первой электроточки',
        default=0,
        null=False,
    )
    first_power_socket_width = models.IntegerField(
        'Расположение электроточки относительно середины ширины объекта',
        default=0,
        null=False,
    )
    second_power_socket_height = models.IntegerField(
        'Высота первой электроточки',
        default=0,
        null=False,
    )
    second_power_socket_width = models.IntegerField(
        'Расположение электроточки относительно середины ширины объекта',
        default=0,
        null=False,
    )

    power_socket_image = models.ImageField(
        verbose_name='Изображение мебели',
        upload_to='furniture/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'

    def __str__(self) -> str:
        return f'{self.name}'
