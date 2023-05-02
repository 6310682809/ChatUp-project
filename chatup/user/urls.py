from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('noti/', views.noti, name='noti'),
    path('friendlist/<int:user_id>', views.friend_list, name='friend_list'),
    path('change_phonenumber/', views.change_phonenumber,
         name='change_phonenumber'),
    path('get_profile_picture/<str:id>', views.get_profile_picture,
         name="get_profile_picture"),

]
