from django.contrib.gis.db import models as gis_models
from django.db import models


class PlacementCoordinates(gis_models.Model):
    """Abstract model with a pointer to a room and coordinates."""

    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        verbose_name='Комната',
        related_name='%(class)ss',
    )
    shape = gis_models.PolygonField(
        verbose_name='Координаты объекта',
        srid=0,
        null=True
    )

    class Meta:
        abstract = True
