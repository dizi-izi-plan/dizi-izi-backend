import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator
from django.db import models

from users.validators import PastDateValidator

# TODO: раскомментировать после создания моделей тарифов
# from users.services import initialize_basic_user_tariff


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("У пользователя должен быть email.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, **extra_fields)

        # при регистрации пользователя создается тариф по умолчанию
        # TODO: раскомментировать после создания моделей тарифов
        # initialize_basic_user_tariff(user)

        return user  # noqa: R504

    def create_superuser(self, email, password=None, **extra_fields):
        user = self._create_user(
            email,
            password=password,
            **extra_fields,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractUser):
    # Присваивает каждому пользователю уникальный id с использованием uuid4 для обеспечения безопасности.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(
        db_index=True,
        max_length=254,
        unique=True,
        validators=[EmailValidator()],
        verbose_name="Email",
        error_messages={
            "unique": "Пользователь с таким email уже существует.",
        },
    )
    city = models.CharField(
        verbose_name="Город",
        max_length=50,
        null=True,
        blank=True
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        validators=[PastDateValidator()],  # ограничивает дату текущим днем
        help_text="Введите дату в прошлом. Будущие даты не допустимы.",
        verbose_name="дата рождения",
    )
    is_designer = models.BooleanField(
        default=False,
        verbose_name="дизайнер"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "city", "birthday", "is_designer"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
