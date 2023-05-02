from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from user.models import *
class Post(models.Model):
    created_by = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name='post_by')
    detail = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f'{ self.created_by.user_id.username } post { self.detail }'

        
class File(models.Model):
    file = models.FileField(upload_to ='image_post/', blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return f'{ self.file }'

class Like(models.Model):
   created_by = models.ForeignKey(
       UserInfo, on_delete=models.CASCADE, related_name='like_by')
   post = models.ForeignKey(
       Post, on_delete=models.CASCADE, related_name='like_post')
   created_at = models.DateTimeField(default=timezone.now, blank=True)

   def __str__(self):
       return f'{ self.created_by.user_id.username } like { self.post.detail }'

class Comment(models.Model):
    created_by = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name='comment_by')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comment_post')
    detail = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f'{ self.created_by.username } post { self.detail }'