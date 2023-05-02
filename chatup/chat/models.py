from user.models import UserInfo
from post.models import Post
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from post.models import *
from user.models import *
from openChat.models import *
import sys
sys.path.append("../post")
from post.models import Post
from user.models import UserInfo
from django_cryptography.fields import encrypt

def chat_image_directory_path(instance, filename):
    if(instance.sender.user_id.id > instance.reciever.user_id.id):
        room_name = f'chat_{instance.sender.user_id.id}-{instance.reciever.user_id.id}'
    else:
        room_name = f'chat_{instance.reciever.user_id.id}-{instance.sender.user_id.id}'
    return 'chat/images/{0}/{1}/image_{2}.{3}'.format(room_name, instance.sender.user_id.username, instance.created_at.strftime('%H:%M:%S'), filename.split('.')[-1])

class Chat(models.Model):
    sender = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name='chat_from')
    reciever = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name='chat_to')
    message = encrypt(models.CharField(max_length=255, blank=True))
    file = encrypt(models.FileField(upload_to =chat_image_directory_path, blank=True))
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f'{ self.sender.user_id.username } send { self.message } \
                to {self.reciever.user_id.username}'

class Notification(models.Model):
    openchat = models.ForeignKey(OpenChat, on_delete=models.CASCADE, blank=True, null=True)
    like = models.ForeignKey(Like, on_delete=models.CASCADE, blank=True, null=True, related_name="like")
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='noti_chat', blank=True, null=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,blank=True, null=True)
    add_friend = models.ForeignKey(Friend, on_delete=models.CASCADE,blank=True, null=True)
    detail = models.CharField(max_length=255)
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='noti_reciever')
    created_at = models.DateTimeField(
        default=timezone.now, blank=True, null=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{ self.detail }'

    def get_detail(self):
        return self.detail[:35].rstrip() + ("" if len(self.detail) <= 35 else "...")
