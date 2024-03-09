from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack, OriginValidator, TokenAuthMiddleware

from .consumers import ChatConsumer

# websocket_application = ProtocolTypeRouter(
#     {
#         "websocket": AuthMiddlewareStack(
#         URLRouter([
#             path("ws/chat/", ChatConsumer.as_asgi()),
#         ])
#     ),
#     })

application = ProtocolTypeRouter({
    'websocket': OriginValidator(
        TokenAuthMiddleware(
            URLRouter([
                 path("ws/chat/", ChatConsumer.as_asgi()),
            ])
        ),
        ['*'],
    ),
})
