from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import CustomUser

CHOICES = (
    (timedelta(days=30), 'месяц'),
    (timedelta(days=90), '3 месяца'),
    (timedelta(days=180), '6 месяцев'),
    (timedelta(days=270), '9 месяцев'),
    (timedelta(days=365), 'год'),
)


class PossibleActions(models.Model):
    name = models.CharField(
        verbose_name='Возможные действия',
        unique=True,
        max_length=256
    )

    class Meta:
        verbose_name = 'Возможные действия'
        verbose_name_plural = 'Возможные действия'

    def __str__(self) -> str:
        return f'{self.name}'


class Tariff(models.Model):
    """Тариф."""
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
        default=timedelta(days=365),
        verbose_name='Период действия тарифа',
        choices=CHOICES,
        help_text='Выберите период действия'
    )
    actions = models.ManyToManyField(
        PossibleActions,
        blank=False,
        through='PossibleActionsTariff',
        verbose_name='Действия',
        related_name='tariff'
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='по умолчанию'
    )

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.is_default:
            Tariff.objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class PossibleActionsTariff(models.Model):
    action = models.ForeignKey(
        PossibleActions,
        blank=False,
        null=False,
        verbose_name='Действия',
        on_delete=models.CASCADE,
        related_name='action_tariff'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        related_name='action_tariff'
    )

    class Meta:
        verbose_name = 'Опции тарифа'
        verbose_name_plural = 'Опции тарифа'
        constraints = [
            UniqueConstraint(
                fields=['action', 'tariff'],
                name='double_actions'
            )
        ]

    def __str__(self):
        return f'{self.tariff} {self.action}'


class UsersTariffs(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='пользователь',
        related_name='user_tariff'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name='Тариф Пользователя',
        related_name='user_tariff'
    )
    start_date = models.DateTimeField(
        verbose_name='Тариф приобретен',
        auto_now_add=True,

    )

    class Meta:
        verbose_name = 'Пользователь: Тариф'
        verbose_name_plural = 'Пользователи: Тарифы'

    def __str__(self) -> str:
        return f'{self.user} {self.tariff}'
