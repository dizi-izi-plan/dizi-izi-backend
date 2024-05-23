from import_export import resources

from . import room_items


class FurnitureResource(resources.ModelResource):
    """Resource класс модели Furniture для работы с import_export библиотекой"""

    class Meta:
        model = room_items.Furniture
        import_id_fields = ("name",)
        skip_unchanged = True


class RoomTypeResource(resources.ModelResource):
    """Resource класс модели RoomType для работы с import_export библиотекой"""

    class Meta:
        model = room_items.RoomType
        import_id_fields = ("name",)
        skip_unchanged = True
