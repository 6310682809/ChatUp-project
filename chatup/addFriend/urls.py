from django.urls import path, include, re_path
from django.conf import settings
from . import views
app_name = 'addFriend'
urlpatterns = [
    path('addFriend/<int:id>',views.addFriend, name="addFriend"),
    path('deleteFriend/<int:id>', views.deleteFriend, name="deleteFriend"),
    path('acceptFriend/<int:id>',views.acceptFriend, name="acceptFriend"),
    path('rejectFriend/<int:id>',views.rejectFriend, name="rejectFriend"),
]