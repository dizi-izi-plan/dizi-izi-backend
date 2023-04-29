from django.contrib import admin
from .models import Furniture, Placement, Room
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(get_user_model())
admin.site.register(Furniture)


class PlacementInline(admin.TabularInline):
    """Настройка для добавления документов в товары."""
    model = Placement


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Админка услуг."""
    list_display = (
        'id',
        'user',
        'name',
        'length',
        'width',
    )
    list_display_links = (
        'user',
        'name',
    )
    inlines = [PlacementInline, ]
