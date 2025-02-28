from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Polygon
from django.db import models

from furniture.validators import minimum_len_width_validator

User = get_user_model()


class Room(models.Model):
    """Model of room."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='Пользователь',
    )
    name = models.CharField(
        'Название комнаты',
        max_length=settings.MAX_LENGTH_ROOM_NAME,
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
    boundary = gis_models.PolygonField(
        verbose_name='Границы комнаты',
        srid=0,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self) -> str:
        return f"Комната: {self.name}"

    def compute_boundary(self):
        width = self.first_wall
        height = self.second_wall
        return Polygon(((0, 0), (width, 0), (width, height), (0, height), (0, 0)))

    def save(self, *args, **kwargs):
        if not self.boundary:
            self.boundary = self.compute_boundary()
        super().save(*args, **kwargs)


class RoomLayout(models.Model):
    """Model of room layout."""

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='layouts',
        verbose_name='Комната',
    )
    name = models.CharField(
        'Название планировки',
        max_length=settings.MAX_LENGTH_ROOM_NAME,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Планировка'
        verbose_name_plural = 'Планировки'

    def __str__(self) -> str:
        return f"Проект {self.name} пользователя {self.user.email}"
