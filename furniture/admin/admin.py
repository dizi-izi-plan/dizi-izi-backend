from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportActionModelAdmin

from furniture import models
from furniture.admin import resources


@admin.register(models.Furniture)
class FurnitureAdmin(ImportExportActionModelAdmin):
    @admin.display(description="Фото")
    def take_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="80" height="60">',
            )
        return None

    list_display = (
        "id",
        "name",
        "depth",
        "width",
        "take_image",
        # "type_of_rooms",
    )
    search_fields = ("type_of_rooms", "name")
    list_filter = ("type_of_rooms",)
    empty_value_display = "-пусто-"
    resource_class = resources.FurnitureResource


class FurniturePlacementInline(admin.TabularInline):
    """Настройка для размещения мебели в комнате."""

    model = models.FurniturePlacement


class PowerSocketPlacementInline(admin.TabularInline):
    """Настройка для размещения розеток в комнате."""

    model = models.PowerSocketPlacement


class DoorPlacementInline(admin.TabularInline):
    """Настройка для размещения дверей в комнате."""

    model = models.DoorPlacement


class WindowPlacementInline(admin.TabularInline):
    """Настройка для размещения окон в комнате."""

    model = models.WindowPlacement


@admin.register(models.RoomLayout)
class RoomLayoutAdmin(admin.ModelAdmin):
    """Админка комнаты."""

    list_display = (
        "id",
        "name",
        # "first_wall",
        # "second_wall",
        # "third_wall",
        # "fourth_wall",
        "created",
    )
    list_display_links = ("name",)
    inlines = (
        FurniturePlacementInline,
        PowerSocketPlacementInline,
    )


@admin.register(models.RoomType)
class RoomTypeAdmin(ImportExportActionModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("slug",)
    empty_value_display = "-пусто-"
    resource_class = resources.RoomTypeResource
