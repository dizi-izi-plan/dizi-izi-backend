from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Tariff(models.Model):
    """Тариф"""
    name = models.CharField(
        verbose_name='Наименование тарифа',
        max_length=256,
        unique=True
    )
    name_english = models.CharField(
        verbose_name='Наименование тарифа на английском языке',
        max_length=256,
        unique=True
    )
    description = models.TextField(verbose_name='Описание тарифа')
    cost = models.PositiveSmallIntegerField(
        verbose_name='Стоимость',
        blank=False,
        null=False,
        validators=[MinValueValidator(
            0,
            message='Тариф должен быть больше 0 руб в мес'
        )]
    )
    period = models.DurationField(
        default=timedelta(days=30,),
        verbose_name='Период действия тарифа',
        help_text='Дни, часы, минуты'
    )

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self) -> str:
        return f'{self.name}'


class UsersTariffs(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='пользователь'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name='Тариф Пользователя'
    )
    start_date = models.DateTimeField(
        verbose_name='Дата начала',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Пользователь: Тариф'
        verbose_name_plural = 'Пользователи: Тарифы'

    def __str__(self) -> str:
        return f'{self.user} {self.tariff}'
