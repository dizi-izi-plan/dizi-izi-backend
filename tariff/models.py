from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from constants import Constants
from users.models import CustomUser


class PossibleActions(models.Model):
    name = models.CharField(
        verbose_name="Возможные действия",
        unique=True,
        max_length=256,
    )

    class Meta:
        verbose_name = "Возможные действия"
        verbose_name_plural = "Возможные действия"

    def __str__(self) -> str:
        return f"{self.name}"


class Tariff(models.Model):
    """Модель тарифов.

    Attributes:
        name: Наименование тарифа.
        name_english: Наименование тарифа на английском языке.
        description: Описание тарифа.
        cost: Стоимость.
        period: Период действия тарифа.
        actions: Действия тарифа.
        is_default: Является ли тарифом по умолчанию?
    """

    name = models.CharField(
        verbose_name="Наименование тарифа",
        max_length=256,
        unique=True,
    )
    name_english = models.SlugField(
        verbose_name="Наименование тарифа на английском языке",
        unique=True,
    )
    description = models.TextField(verbose_name="Описание тарифа")
    cost = models.PositiveSmallIntegerField(
        verbose_name="Стоимость",
        blank=False,
        null=False,
        validators=[
            MinValueValidator(
                0,
                message="Тариф должен быть больше 0 руб в мес",
            ),
        ],
    )
    period = models.DurationField(
        default=timedelta(days=365),
        verbose_name="Период действия тарифа",
        choices=Constants.CHOICES,
        help_text="Выберите период действия",
    )
    # actions = models.ManyToManyField(
    #     PossibleActions,
    #     blank=True,
    #     through='PossibleActionsTariff',
    #     verbose_name='Действия',
    #     related_name='tariff'
    # )
    project_limit = models.PositiveIntegerField(
        verbose_name="Количество планировок",
        default=0,
    )
    rooms_limit = models.PositiveIntegerField(
        verbose_name="Количество комнат",
        default=0,
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="по умолчанию",
    )

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """Сохранение тарифа по умолчанию.

        Если назначается тариф по умолчанию, то в остальных тарифах он
        становится не по умолчанию. (остаться должен только один!).
        """

        if self.is_default:
            Tariff.objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class PossibleActionsTariff(models.Model):
    """Пока не понятно, что это. Не использовал."""

    action = models.ForeignKey(
        PossibleActions,
        blank=False,
        null=False,
        verbose_name="Действия",
        on_delete=models.CASCADE,
        related_name="action_tariff",
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        related_name="action_tariff",
    )

    class Meta:
        verbose_name = "Опции тарифа"
        verbose_name_plural = "Опции тарифа"
        constraints = [
            UniqueConstraint(
                fields=["action", "tariff"],
                name="double_actions",
            ),
        ]

    def __str__(self):
        return f"{self.tariff} {self.action}"


class UsersTariffs(models.Model):
    """Связь тарифа и пользователя.

    Attributes:
        user(User): Пользователь.
        tariff(Tariff): Тариф Пользователя.
        start_date(datetime): Дата приобретения тарифа.
    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name="пользователь",
        related_name="user_tariff",
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name="Тариф Пользователя",
        related_name="user_tariff",
    )
    start_date = models.DateTimeField(
        verbose_name="Тариф приобретен",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Пользователь: Тариф"
        verbose_name_plural = "Пользователи: Тарифы"

    def __str__(self) -> str:
        return f"{self.user} {self.tariff}"
