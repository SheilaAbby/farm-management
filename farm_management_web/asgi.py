# """
# ASGI config for farm_management_web project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """

# import os
# # from django.core.asgi import get_asgi_application
# # django_asgi_app = get_asgi_application()

# os.environ['DJANGO_SETTINGS_MODULE'] = 'farm_management_web.settings'

# import django
# django.setup()

# from django.core.asgi import get_asgi_application
# django_asgi_app = get_asgi_application()


# from channels.http import AsgiHandler
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from .routing import websocket_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management_web.settings')

# application = ProtocolTypeRouter({
#     # "http": AsgiHandler(),
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(
#         websocket_application
#     ),
# })

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

from .consumers import ChatConsumer

from farm_management_web.routing import application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farm_management_web.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import farm_management_web.routing

application = ProtocolTypeRouter({
    # Django's ASGI 
    # application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(application))
    ),
})

# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
#         ),
#     }
# )


