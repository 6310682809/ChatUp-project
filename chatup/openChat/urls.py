from django.urls import path
from . import views

app_name = 'openchat'

urlpatterns = [
    path('openchat/', views.index, name='index'),
    path('openchat/create/', views.create_openchat, name='create_openchat'),
    path('openchat/<int:openchat_id>', views.view_openchat, name='view_openchat'),
    path('openchat/update/<int:openchat_id>', views.update_openchat, name='update_openchat'),
    path('openchat/remove-member/<int:openchat_id>/<int:member_id>', views.remove_member, name='remove_member'),
    path('openchat/delete/<int:openchat_id>', views.delete_openchat, name='delete_openchat'),
    path('openchat/join/<int:openchat_id>', views.join_openchat, name='join_openchat'),
    path('openchat/leave/<int:openchat_id>', views.leave_openchat, name='leave_openchat'),
    path('openchat/delete-message/<int:openchat_id>/<int:message_id>', views.delete_message, name='delete_message')
]