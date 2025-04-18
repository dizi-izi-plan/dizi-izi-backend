from rest_framework import serializers


class AbstractCoordinates(serializers.Serializer):
    """Абстрактная модель для координат в сериализаторах."""

    class Meta:
        abstract = True
