from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/openchat/<int:openchat_id>/', consumers.ChatConsumer.as_asgi()),
]