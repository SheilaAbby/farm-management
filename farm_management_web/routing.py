from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack

from .consumers import ChatConsumer

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/", ChatConsumer.as_asgi()),
        ])
    ),
    })
