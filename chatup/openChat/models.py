from django.db import models
from django.contrib.auth.models import User

import sys
sys.path.append("..")

from user.models import UserInfo
from django_cryptography.fields import encrypt

class OpenChat(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, unique=False, blank=False)
    members = models.ManyToManyField(UserInfo, blank=True)
    group_image = models.ImageField(
        upload_to ='file_in_openchat/', blank=True, default='./static/assets/default_profile_image/avatar.jpg')
    created_by = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name='open_chat_created_by')

    def __str__(self):
        return f'{ self.name }'
    
class Message(models.Model):
    created_by = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name='message_created_by')
    open_chat = models.ForeignKey(
        OpenChat, on_delete=models.CASCADE, related_name='open_chat')
    message = encrypt(models.TextField(unique=False, blank=False))
    file = encrypt(models.FileField(upload_to ='file_in_openchat/', blank=True))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return self.message