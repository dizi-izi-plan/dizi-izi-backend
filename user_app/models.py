from django.db import models


class Furniture(models.Model):
    """Table Furniture."""
    name = models.CharField(max_length=30)
    lenght = models.IntegerField('lenght furniture')
    width = models.IntegerField('width furniture')
    x_coordinate = models.FloatField(default=0)
    y_coordinate = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.name
    