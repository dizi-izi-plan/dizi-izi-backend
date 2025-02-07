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
    """Furniture model."""

    name = models.CharField(
        verbose_name='Наименование мебели',
        max_length=settings.MAX_LENGTH_FURNITURE_NAME,
    )
    name_eng = models.CharField(
        verbose_name='Наименование мебели на английском языке',
        max_length=settings.MAX_LENGTH_FURNITURE_NAME,
    )
    length = models.PositiveIntegerField(
        verbose_name='Длина мебели',
        help_text='Длина в мм',
        validators=(minimum_len_width_validator,),
    )
    width = models.PositiveIntegerField(
        verbose_name='Ширина мебели',
        help_text='Ширина в мм',
        validators=(minimum_len_width_validator,),
    )
    length_with_access_zone = models.PositiveIntegerField(
        verbose_name='Длина мебели c зоной подхода',
        help_text='Длина c зоной подхода в мм',
        validators=(minimum_len_width_validator,),
    )
    width_with_access_zone = models.PositiveIntegerField(
        verbose_name='Ширина мебели c зоной подхода',
        help_text='Ширина c зоной подхода в мм',
        validators=(minimum_len_width_validator,),
    )
    image = models.ImageField(
        verbose_name='Изображение мебели',
        upload_to='furniture/',
        blank=True,
        null=True,
    )
    type_of_rooms = models.ManyToManyField(
        "RoomType",
        related_name='furniture',
        verbose_name='Комнаты',
    )

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'
        unique_together = ('name', 'length', 'width')

    def __str__(self) -> str:
        return f'{self.name}'
