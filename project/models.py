from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Project(models.Model):
    name = models.CharField(
        verbose_name=settings.PROJECT_NAME_VERBOSE_NAME,
        max_length=settings.MAX_LENGTH_PROJECT_NAME,
        default=settings.PROJECT_NAME_BY_DEFAULT,
    )
    is_draft = models.BooleanField(
        default=True,
        verbose_name=settings.PROJECT_DRAFT_VERBOSE_NAME,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=settings.PROJECT_CREATED_AT_VERBOSE_NAME,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=settings.PROJECT_UPDATED_AT_VERBOSE_NAME,
    )
    layout_requests_left = models.PositiveSmallIntegerField(
        verbose_name=settings.PROJECT_LAYOUT_REQUESTS_LEFT_VERBOSE_NAME,
        default=settings.PROJECT_LAYOUT_REQUESTS_LEFT_MAX_VALUE,
        validators=[
            MinValueValidator(
                settings.PROJECT_LAYOUT_REQUESTS_LEFT_MIN_VALUE,
                message=settings.PROJECT_LAYOUT_REQUESTS_LEFT_MIN_VALUE_MESSAGE,
            ),
            MaxValueValidator(
                settings.PROJECT_LAYOUT_REQUESTS_LEFT_MAX_VALUE,
                message=settings.PROJECT_LAYOUT_REQUESTS_LEFT_MAX_VALUE_MESSAGE,
            ),
        ],
    )
    preferred_layout_id = models.IntegerField(
        verbose_name=settings.PROJECT_PREFERRED_LAYOUT_VERBOSE_NAME,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = settings.PROJECT_NAME_BY_DEFAULT
        verbose_name_plural = settings.PROJECTS_VERBOSE_NAME_PLURAL

    def __str__(self) -> str:
        return (
            f'Создан проект "{self.name}" для пользователя {self.user} с id {self.pk}'
        )
