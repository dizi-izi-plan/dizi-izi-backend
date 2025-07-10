from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from project.literals import project_literals

User = get_user_model()


class Project(models.Model):
    name = models.CharField(
        verbose_name=project_literals.project_name_verbose_name,
        max_length=project_literals.max_length_project_name,
        default=project_literals.project_name_by_default,
    )
    is_draft = models.BooleanField(
        default=True,
        verbose_name=project_literals.project_draft_verbose_name,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=project_literals.project_created_at_verbose_name,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=project_literals.project_updated_at_verbose_name,
    )
    layout_requests_left = models.PositiveSmallIntegerField(
        verbose_name=project_literals.project_layout_requests_left_verbose_name,
        default=project_literals.project_layout_requests_left_max_value,
        validators=[
            MinValueValidator(
                project_literals.project_layout_requests_left_min_value,
                message=project_literals.project_layout_requests_left_min_value_message,
            ),
            MaxValueValidator(
                project_literals.project_layout_requests_left_max_value,
                message=project_literals.project_layout_requests_left_max_value_message,
            ),
        ],
    )
    preferred_layout_id = models.IntegerField(
        verbose_name=project_literals.project_preferred_layout_verbose_name,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = project_literals.project_name_by_default
        verbose_name_plural = project_literals.projects_verbose_name_plural

    def __str__(self) -> str:
        return project_literals.project_str_output.format(
            self.name,
            self.user.username,
            self.pk,
        )
