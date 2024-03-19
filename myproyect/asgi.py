import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from wacchat.consumers import YourConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path('ws/chat/', YourConsumer.as_asgi()),
        # Add more WebSocket routes as needed
    ]),
    # Add other protocol handlers if needed
})

