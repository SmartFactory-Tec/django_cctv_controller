from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.routing import get_default_application
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from . import consumers

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        re_path(
                            r"ws/stream/(?P<camera_id>\w+)/$", StreamConsumer.as_asgi()
                        ),
                    ]
                )
            )
        ),
    }
)
