"""
ASGI config for lab1 project.

It exposes the ASGI callable as a module-level variable named ``order``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab1.settings')

order = get_asgi_application()
