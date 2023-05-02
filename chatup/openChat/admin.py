from django.contrib import admin
from .models import *

class OpenChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by', 'group_image')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'open_chat', 'message', 'file', 'created_at')

admin.site.register(OpenChat, OpenChatAdmin)
admin.site.register(Message, MessageAdmin)