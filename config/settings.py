import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_KEY", "some_key")

DEBUG = os.getenv("DEBUG_KEY", "False")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://*.127.0.0.1",
    "https://*localhost",
    "http://localhost",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "furniture",
    "users",
    "rest_framework.authtoken",
    "social_django",
    "djoser",
    "api",
    "info",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", default="5433"),
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "dizi.izi.plan@gmail.com"
DEFAULT_FROM_EMAIL = "dizi.izi.plan@gmail.com"
EMAIL_HOST_PASSWORD = "tkttxsrnycqeijpw"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
        "users.throttling.SustainedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "2/second",  # Лимит для AnonRateThrottle
        "user": "5/second",
        "long_time": "10/minute",
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Dizi-izi API",
    "DESCRIPTION": "Документация для проекта Dizi-izi-backend",
    "VERSION": "v1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "CONTACT": {"email": "dizi.izi.plan@gmail.com"},
    "LICENSE": {"name": "MIT License"},
}

DJOSER = {
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "ACTIVATION_URL": "api/v1/auth/users/activate/{uid}/{token}",
    # тут подключается фронт с активацией на url: /api/v1/auth/users/activation/
    "SEND_ACTIVATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "LOGIN_FIELD": "email",
    "PASSWORD_RESET_CONFIRM_URL": "api/v1/auth/users/password/reset/confirm/{uid}/{token}",
    # тут подключается фронт с отправкой на url: /api/v1/auth/users/reset_password_confirm/
    "SERIALIZERS": {
        "user_create": "users.serializers.CustomUserCreateSerializer",
        "user": "users.serializers.CustomUserCreateSerializer",
        "current_user": "users.serializers.CustomUserCreateSerializer",
        "user_create_password_retype": "users.serializers.CustomUserCreatePasswordRetypeSerializer",
    },
    "PERMISSIONS": {
        "user_delete": ["rest_framework.permissions.IsAdminUser"],
    },
    "EMAIL": {
        "activation": "users.emails.CustomActivationEmail",
        "password_reset": "users.emails.CustomPasswordResetEmail",
    },
}

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.vk.VKOAuth2",
    "social_core.backends.yandex.YandexOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

#Social auth keys
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_YANDEX_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_KEY')
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_SECRET')

# константы проекта, если их будет много, то нужно будет их организовать в
# отдельно файлике с разбивкой по тематике
MAX_LENGTH_PROJECT_NAME = 128
MAX_LENGTH_ROOM_NAME = 128
MAX_LENGTH_FURNITURE_NAME = 128
PROJECT_NAME_BY_DEFAULT = "Проект"
