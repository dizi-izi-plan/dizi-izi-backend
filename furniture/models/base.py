from django.db import models


class Coordinate(models.Model):
    """Модель координаты."""

    x = models.PositiveIntegerField(
        verbose_name='X',
    )
    y = models.PositiveIntegerField(
        verbose_name='Y',
    )

    def __str__(self):
        return f'x={self.x}, y={self.y}'


class PlacementCoordinates(models.Model):
    """Абстрактная модель с указателем на помещение и координаты."""

    room = models.ForeignKey(
        "RoomLayout",
        on_delete=models.CASCADE,
        verbose_name='Комната',
        related_name='%(class)ss',
    )
    north_west = models.OneToOneField(
        'Coordinate',
        verbose_name='Координата north-west',
        on_delete=models.PROTECT,
        null=True,
    )
    north_east = models.OneToOneField(
        'Coordinate',
        verbose_name='Координата north-east',
        on_delete=models.PROTECT,
        null=True,
        related_name='+',
    )
    south_west = models.OneToOneField(
        'Coordinate',
        verbose_name='Координата south-west',
        on_delete=models.PROTECT,
        null=True,
        related_name='+',
    )
    south_east = models.OneToOneField(
        'Coordinate',
        verbose_name='Координата south-east',
        on_delete=models.PROTECT,
        null=True,
        related_name='+',
    )

    class Meta:
        abstract = True
