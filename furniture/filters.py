from django_filters import rest_framework as filters

from furniture.models import Furniture


class FurnitureFilter(filters.FilterSet):
    type_of_rooms = filters.CharFilter(field_name='type_of_rooms__slug')

    class Meta:
        model = Furniture
        fields = (
            'type_of_rooms',
        )
