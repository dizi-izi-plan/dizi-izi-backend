from django.contrib import admin

from info.models import (
    Tariff,
    UsersTariffs,
    PossibleActionsTariff,
    PossibleActions,
)


class PossibleActionsTariffAdmin(admin.TabularInline):
    model = PossibleActionsTariff
    min_num = 1


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    @admin.display(description='Возможности')
    def action_list(self, obj):
        if obj.actions:
            return list(action for action in obj.actions.all())
        return None

    list_display = ('id', 'name', 'is_default', 'cost', 'period', 'action_list')
    search_fields = ('name', 'cost', 'period')
    list_filter = ('cost', 'period',)
    empty_value_display = '-пусто-'
    inlines = [PossibleActionsTariffAdmin, ]


@admin.register(UsersTariffs)
class UsersTariffsAdmin(admin.ModelAdmin):
    @admin.display(description='Дата окончания')
    def stop_date(self, obj):
        return obj.start_date + obj.tariff.period

    list_display = ('id', 'user', 'tariff', 'start_date', 'stop_date')
    search_fields = ('user', 'tariff', 'start_date', 'stop_date')
    list_filter = ('user', 'tariff', 'start_date')
    empty_value_display = '-пусто-'


@admin.register(PossibleActions)
class PossibleActionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
