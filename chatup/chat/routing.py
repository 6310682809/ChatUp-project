from django.urls import path , include
from chat.consumers import ChatConsumer, OnlineStatusConsumer
 
# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    path("ws/chat/<int:id>/" , ChatConsumer.as_asgi()) ,
    path('ws/online/', OnlineStatusConsumer.as_asgi()) ,
]