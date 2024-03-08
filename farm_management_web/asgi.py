"""
ASGI config for farm_management_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .routing import application as websocket_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management_web.settings')
django.setup()
django_asgi_app = get_default_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_application  
        )
    ),
})
