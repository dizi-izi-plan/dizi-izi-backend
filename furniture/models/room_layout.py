from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Polygon
from django.db import models

from furniture.validators import minimum_len_width_validator

User = get_user_model()


class Room(gis_models.Model):
    """Model of room."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='Пользователь',
    )
    name = models.CharField(
        verbose_name='Название комнаты',
        max_length=settings.MAX_LENGTH_ROOM_NAME,
    )
    width = models.PositiveIntegerField(
        verbose_name='Ширина комнаты',
        help_text='Ширина комнаты в мм',
        validators=(minimum_len_width_validator,),
    )
    height = models.PositiveIntegerField(
        verbose_name='Длина комнаты',
        help_text='Длина комнаты в мм',
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
        unique_together = ('user', 'name')

    def __str__(self) -> str:
        return f"Комната: {self.name}"

    def compute_boundary(self):
        return Polygon(((0, 0), (self.width, 0), (self.width, self.height), (0, self.height), (0, 0)))

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
        return f"Проект {self.name} пользователя {self.room.user.email}"
