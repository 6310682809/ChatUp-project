from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'post'

urlpatterns = [
    path('post/', views.post, name='post'),
    path('post/<int:post_id>', views.view_post, name='view_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('delete_comment/<int:post_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('like_post/<int:post_id>', views.like_post, name='like_post'),

]