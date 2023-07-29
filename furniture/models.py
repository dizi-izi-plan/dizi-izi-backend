from django.contrib.auth import get_user_model
from django.db import models

from api.utils import get_name
from config.settings import (
    MAX_LENGTH_FURNITURE_NAME,
    MAX_LENGTH_ROOM_NAME,
)
from furniture.validators import minimum_len_width_validator

User = get_user_model()


class TypeOfRoom(models.Model):
    """Типы комнат для мебели."""
    name = models.CharField(
        verbose_name='Наименование комнаты',
        unique=True,
        max_length=128
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
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
        max_length=MAX_LENGTH_FURNITURE_NAME,
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
        TypeOfRoom,
        on_delete=models.CASCADE,
        related_name='furniture',
        verbose_name='Комната',
        blank=False,
        null=False
    )
    power_socket_type = models.CharField(
        'Тип электроточки',
        max_length=MAX_LENGTH_FURNITURE_NAME,
        unique=False,
    )
    first_power_socket_height = models.IntegerField(
        'Высота первой электроточки',
        default=0,
        null=False
    )
    first_power_socket_width = models.IntegerField(
        'Расположение электроточки относительно середины ширины объекта',
        default=0,
        null=False
    )
    second_power_socket_height = models.IntegerField(
        'Высота первой электроточки',
        default=0,
        null=False
    )
    second_power_socket_width = models.IntegerField(
        'Расположение электроточки относительно середины ширины объекта',
        default=0,
        null=False
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


class Coordinate(models.Model):
    """Модель координаты."""
    x = models.PositiveIntegerField(
        verbose_name='X'
    )
    y = models.PositiveIntegerField(
        verbose_name='Y'
    )

    def __str__(self):
        return f'x={self.x}, y={self.y}'


class RoomCoordinates(models.Model):
    """Абстрактная модель с указателем на помещение и координаты."""

    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        verbose_name='Комната',
        related_name='%(class)ss',
    )
    north_west = models.OneToOneField(
        'Coordinate',
        verbose_name='Координата north-west',
        on_delete=models.PROTECT,
        null=True
    )
    north_east = models.OneToOneField(
        'Coordinate',
        verbose_name='Координата north-east',
        on_delete=models.PROTECT,
        null=True,
        related_name='+'
    )
    south_west = models.OneToOneField(
        'Coordinate',
        verbose_name='Координата south-west',
        on_delete=models.PROTECT,
        null=True,
        related_name='+'
    )
    south_east = models.OneToOneField(
        'Coordinate',
        verbose_name='Координата south-east',
        on_delete=models.PROTECT,
        null=True,
        related_name='+'
    )

    class Meta:
        abstract = True


class Placement(RoomCoordinates):
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


class Room(models.Model):
    """Модель помещения."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='Пользователь',
    )
    name = models.CharField(
        'Название планировки',
        max_length=MAX_LENGTH_ROOM_NAME,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
        db_index=True,
    )
    first_wall = models.PositiveIntegerField(
        'Длина 1 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator,),
    )
    second_wall = models.PositiveIntegerField(
        'Длина 2 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator,),
    )
    third_wall = models.PositiveIntegerField(
        'Длина 3 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator,),
    )
    fourth_wall = models.PositiveIntegerField(
        'Длина 4 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator,),
    )
    furniture_placement = models.ManyToManyField(
        'Furniture',
        through='Placement',
    )

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    def __str__(self) -> str:
        return f"Проект {self.name} пользователя {self.user.email}"

    def copy(self, request):
        """
        Returns a copy of the Room instance with a new primary key and the
        same attribute values.

        M2M relations are not copied.
        """
        return Room.objects.create(
            user=self.user,
            name=get_name(self.user),
            first_wall=self.first_wall,
            second_wall=self.second_wall,
            third_wall=self.third_wall,
            fourth_wall=self.fourth_wall,
        )


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


class Window(RoomCoordinates):
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
