from django.contrib import admin
from chat.models import *

class ChatAdmin(admin.ModelAdmin):
    list_display = ("sender", "reciever", "message", "file", "created_at")

admin.site.register(Chat, ChatAdmin)
admin.site.register(Notification)