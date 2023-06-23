from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Furniture, Placement, Room, PowerSocket, Door, Window,
                     TypeOfRoom)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(get_user_model())


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    @admin.display(description='Фото')
    def take_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="80" height="60">'
            )
        return None

    list_display = ('name', 'take_image', 'type_of_rooms')
    search_fields = ('type_of_rooms', 'name')
    list_filter = ('type_of_rooms', )
    empty_value_display = '-пусто-'


class PlacementInline(admin.TabularInline):
    """Настройка для размещения мебели в комнате."""
    model = Placement


class PowerSocketInline(admin.TabularInline):
    """Настройка для размещения розеток в комнате."""
    model = PowerSocket


class DoorInline(admin.TabularInline):
    """Настройка для размещения дверей в комнате."""
    model = Door


class WindowInline(admin.TabularInline):
    """Настройка для размещения окон в комнате."""
    model = Window


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Админка комнаты."""
    list_display = (
        'id',
        'user',
        'name',
        'first_wall',
        'second_wall',
        'third_wall',
        'fourth_wall'
    )
    list_display_links = (
        'user',
        'name',
    )
    inlines = (PlacementInline, PowerSocketInline, DoorInline, WindowInline)


@admin.register(TypeOfRoom)
class TypeOfRoomAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'
