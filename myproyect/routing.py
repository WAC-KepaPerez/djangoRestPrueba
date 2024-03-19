# myproject/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from wacchat.consumers import YourConsumer  # Import your consumer

websocket_urlpatterns = [
    path('ws/chat/', YourConsumer.as_asgi()),
    # Define WebSocket URL patterns
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
    # Add other protocols if needed
})




