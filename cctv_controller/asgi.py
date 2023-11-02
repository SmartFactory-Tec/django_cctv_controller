import os
import django

from django.core.asgi import get_asgi_application
from django.urls import re_path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

django_asgi_app = get_asgi_application()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cctv_controller.settings")

django.setup()

from api.consumers import StreamConsumer

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        re_path(
                            r"ws/stream/(?P<camera_id>\w+)/$", StreamConsumer.as_asgi()
                        )
                    ]
                )
            )
        ),
    }
)
