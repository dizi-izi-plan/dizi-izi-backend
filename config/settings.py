from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    'django-insecure-zc))j&u4h!-r1r!8#!a_8p9q1kkt#7+64$*amhm107m$k(c*sm'
)

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'furniture',
    'users',
    'rest_framework.authtoken',
    'djoser',
    'api',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'dizi.izi.plan@gmail.com'
DEFAULT_FROM_EMAIL = 'dizi.izi.plan@gmail.com'
EMAIL_HOST_PASSWORD = 'tkttxsrnycqeijpw'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Di-zi',
    'DESCRIPTION': 'Super impa project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'ACTIVATION_URL': 'api/v1/auth/users/activate/{uid}/{token}',
    # тут подключается фронт с активацией на url: /api/v1/auth/users/activation/
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'LOGIN_FIELD': 'email',
    'PASSWORD_RESET_CONFIRM_URL': 'api/v1/auth/users/password/reset/confirm/{uid}/{token}',
    # тут подключается фронт с отправкой на url: /api/v1/auth/users/reset_password_confirm/
    'SERIALIZERS': {
        'user_create': 'api.v1.serializers.CustomUserCreateSerializer',
        'user': 'api.v1.serializers.CustomUserCreateSerializer',
        'current_user': 'api.v1.serializers.CustomUserCreateSerializer',
    },
    'PERMISSIONS': {
        'user_delete': ['rest_framework.permissions.IsAdminUser'],
    },



    'EMAIL': {
        'activation': 'users.emails.CustomActivationEmail',
        'password_reset': 'users.emails.CustomPasswordResetEmail'
    }

}

AUTH_USER_MODEL = 'users.CustomUser'
# константы проекта, если их будет много, то нужно будет их организовать в
# отдельно файлике с разбивкой по тематике
MAX_LENGTH_PROJECT_NAME = 128
MAX_LENGTH_ROOM_NAME = 128
MAX_LENGTH_FURNITURE_NAME = 128
