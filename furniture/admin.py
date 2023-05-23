from django.contrib import admin
from .models import Furniture, Placement, Room, PowerSocket, Door, Window
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(get_user_model())
admin.site.register(Furniture)


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
