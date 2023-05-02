from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    profile_image = models.ImageField(upload_to ='uploads/', blank=True)
    chatup_id = models.CharField(max_length=10, unique=True)
    prefix_phone_number = models.CharField(max_length=3, default='+66')
    phone_number = models.CharField(max_length=15)
    online_status = models.BooleanField(default=False, blank=True)
    last_logout = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f'{ self.user_id.username }'

class Friend(models.Model):
    user_id = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name='user')
    friend_id = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name='friend')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{ self.friend_id.user_id.username } is { self.user_id.user_id.username }'s friend"
