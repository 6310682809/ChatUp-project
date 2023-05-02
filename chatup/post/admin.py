from django.contrib import admin
from django.contrib import admin
from .models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("created_by", "detail", "created_at")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("created_by", "post", "created_at")
class FileAdmin(admin.ModelAdmin):
    list_display = ('post', 'file')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like, LikeAdmin)
admin.site.register(File, FileAdmin)
