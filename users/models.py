from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('У пользователя должен быть email.')

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email), password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        'Email', db_index=True, max_length=254, unique=True
    )
    password = models.CharField('Password', max_length=150)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
