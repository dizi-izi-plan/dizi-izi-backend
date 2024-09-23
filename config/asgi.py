"""
ASGI config for dizi_izi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Checking the value of a variable has been replaced by an explicit definition of the value
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.settings'

application = get_asgi_application()
