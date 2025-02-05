from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'

    def __str__(self) -> str:
        return f'{self.name}'


class PowerSocket(models.Model):
    """Power socket model."""

    socket_type = models.CharField(
        verbose_name='Тип электроточки',
        max_length=settings.MAX_LENGTH_FURNITURE_NAME,
        unique=False,
    )
    height = models.IntegerField(
        verbose_name='Высота электроточки',
        default=0,
        null=False,
    )
    width = models.IntegerField(
        verbose_name='Ширина электроточки',
        default=0,
        null=False,
    )
    power_socket_image = models.ImageField(
        verbose_name='Изображение электроточки',
        upload_to='power_sockets/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Электроточка'
        verbose_name_plural = 'Электроточки'

    def __str__(self):
        return f"{self.socket_type} ({self.width}x{self.height})"


class PowerSocketPosition(models.Model):
    """Model of the relationship between room objects and the position of the socket."""

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип объекта (мебель или дверь)',
        related_name='socket_connections',
    )
    object_id = models.PositiveIntegerField(
        verbose_name='ID объекта (мебель или дверь)',
    )
    connected_object = GenericForeignKey('content_type', 'object_id')

    power_socket = models.ForeignKey(
        'PowerSocket',
        on_delete=models.CASCADE,
        verbose_name='Электроточка',
        related_name='object_connections',
    )
    offset_width = models.IntegerField(
        verbose_name='Смещение электроточки по ширине относительно центра объекта',
        default=0,
        null=False,
    )
    offset_height = models.IntegerField(
        verbose_name='Высота электроточки от пола',
        default=0,
        null=False,
    )

    class Meta:
        verbose_name = 'Расположение электроточки'
        verbose_name_plural = 'Расположения электроточек'
        unique_together = ('content_type', 'object_id', 'power_socket')

    def __str__(self):
        return f'{self.power_socket} для {self.connected_object}'
