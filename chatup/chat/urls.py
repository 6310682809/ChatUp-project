from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.index, name='index'),
    path('chat/<int:friend_id>', views.view_chat, name='view_chat'),
    path('delete_message_chat/<int:chat_id>', views.delete_message_chat, name='delete_message_chat'),
]