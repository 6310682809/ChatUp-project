from django.urls import path, include
from . import views

app_name = 'searchFriend'

urlpatterns = [
    path('searchFriend/', views.searchFriend, name='searchFriend'),
    path('friend/<str:username>', views.friend, name='friend')
]
