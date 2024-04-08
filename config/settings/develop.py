from .base import *  # noqa: F403, F401

# Переопределяем бэкенд для отправки электронных писем на консольный бэкенд в среде разработки.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
