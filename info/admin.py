from django.contrib import admin

from info.models import Tariff, UsersTariffs


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cost', 'period')
    search_fields = ('name', 'cost', 'period')
    list_filter = ('cost', 'period',)
    empty_value_display = '-пусто-'


@admin.register(UsersTariffs)
class UsersTariffsAdmin(admin.ModelAdmin):
    @admin.display(description='Дата окончания')
    def stop_date(self, obj):
        return obj.start_date + obj.tariff.period

    list_display = ('user', 'tariff', 'start_date', 'stop_date')
    search_fields = ('user', 'tariff', 'start_date', 'stop_date')
    list_filter = ('user', 'tariff', 'start_date')
    empty_value_display = '-пусто-'
