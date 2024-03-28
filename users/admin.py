from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


User = get_user_model()
# Отменяет регистрацию модели User для избежания конфликтов при кастомизации админ-панели.
admin.site.unregister(User)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ["email", "is_active", "is_designer", "is_staff", "is_superuser",]
    list_filter = ["is_active", "is_designer", "is_staff", "is_superuser",]
    ordering = [
        "email",
    ]
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2",)}),
        ("Персональная информация", {"fields": ("first_name", "city", "birthday",)}),
        ("Права доступа", {"fields": ("is_active", "is_designer", "is_staff", "is_superuser")}),
        ("Даты регистрации и последнего входа", {"fields": ("date_joined", "last_login",)}),
    )
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Персональная информация", {"fields": ("first_name", "city", "birthday",)}),
        ("Права доступа", {"fields": ("is_active", "is_designer", "is_staff", "is_superuser")}),
        ("Даты регистрации и последнего входа", {"fields": ("date_joined", "last_login",)}),
        ("Разрешения пользователя", {"fields": ("user_permissions",)})
    )
