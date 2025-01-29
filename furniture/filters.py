from django_filters import rest_framework as filters

from furniture.models import Furniture, RoomType


class FurnitureFilter(filters.FilterSet):
    type_of_rooms = filters.CharFilter(field_name='type_of_rooms__slug')

    class Meta:
        model = Furniture
        fields = (
            'type_of_rooms',
        )


class RoomTypeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name')

    class Meta:
        model = RoomType
        fields = (
            'name',
        )
