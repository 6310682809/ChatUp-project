from os import truncate
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from sympy import Min
from .models import *
from user.models import UserInfo, Friend
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import timedelta

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        userInfo = UserInfo.objects.get(user_id=user)
        all_friend = Friend.objects.filter(user_id=userInfo, status=True)

        last_chat_friend = {}
        for f in all_friend:
            all_chat_sender = Chat.objects.filter(sender=userInfo, reciever=f.friend_id)
            all_chat_reciever = Chat.objects.filter(sender=f.friend_id, reciever=userInfo)
            try:
                all_chat_ = (all_chat_sender | all_chat_reciever).order_by("-created_at")[0]
            except:
                first_message = "คุณ " + userInfo.user_id.username + " และคุณ " + f.friend_id.user_id.username + " เป็นเพื่อนกันแล้ว"
                chat = Chat.objects.create(sender=userInfo, reciever=f.friend_id, message=first_message)
                last_chat_friend[chat.created_at] = chat
                continue
            last_chat_friend[all_chat_.created_at] = all_chat_

        sort_last_chat_friend = sorted(last_chat_friend.items(), reverse=True)
        return render(request, 'chat/chat.html', {
            'userInfo': userInfo,
            'sort_last_chat_friend': sort_last_chat_friend,
        })
    
def view_chat(request, friend_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    user = User.objects.get(username=request.user.username)
    userInfo = UserInfo.objects.get(user_id=user)
    all_friend = Friend.objects.filter(user_id=userInfo, status=True)

    last_chat_friend = {}
    for f in all_friend:
        all_chat_sender = Chat.objects.filter(sender=userInfo, reciever=f.friend_id)
        all_chat_reciever = Chat.objects.filter(sender=f.friend_id, reciever=userInfo)
        try:
            all_chat_ = (all_chat_sender | all_chat_reciever).order_by("-created_at")[0]
        except:
            first_message = "คุณ " + userInfo.user_id.username + " และคุณ " + f.friend_id.user_id.username + " เป็นเพื่อนกันแล้ว"
            chat = Chat.objects.create(sender=userInfo, reciever=f.friend_id, message=first_message)
            last_chat_friend[chat.created_at] = chat
            continue
        last_chat_friend[all_chat_.created_at] = all_chat_

    sort_last_chat_friend = sorted(last_chat_friend.items(), reverse=True)

    friend = User.objects.get(id=friend_id)
    
    friendInfo = UserInfo.objects.get(user_id=friend)

    if request.method == 'POST':
        message = request.POST['message']
        files = request.FILES.getlist('images')

        if(userInfo.user_id.id > friendInfo.user_id.id):
            room_name = f'chat_{userInfo.user_id.id}-{friendInfo.user_id.id}'
        else:
            room_name = f'chat_{friendInfo.user_id.id}-{userInfo.user_id.id}'
        if(message):
            chat = Chat.objects.create(sender=userInfo, reciever=friendInfo, message=message)

            date = chat.created_at
            date = date.strftime('%H:%M')

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                room_name,
                {
                    'type': 'sendMessage',
                    'message': message,
                    "filePath": "",
                    "username" : userInfo.user_id.username ,
                    "receiver" : friendInfo.user_id.username ,
                    "img_profile" : userInfo.profile_image.url ,
                    "date" : date,
                    "chat_id": chat.id
                }
            )
        elif(len(files) > 0):
            for file in files:
                chat = Chat.objects.create(sender=userInfo, reciever=friendInfo, file=file)

                date = chat.created_at
                date += timedelta(hours=7)
                date = date.strftime('%H:%M')

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    room_name,
                    {
                        'type': 'sendMessage',
                        'message': "",
                        "filePath": chat.file.url,
                        "username" : userInfo.user_id.username ,
                        "receiver" : friendInfo.user_id.username ,
                        "img_profile" : userInfo.profile_image.url ,
                        "date" : date,
                        "chat_id": chat.id
                    }
                )
        Notification.objects.create(
            chat = chat,
            detail = str(chat),
            reciever = friend,
            create_by = user,
        ).save()
        return redirect(reverse('chat:view_chat', args=[friend_id]))
    
    all_chat_sender = Chat.objects.filter(sender=userInfo, reciever=friendInfo)
    all_chat_reciever = Chat.objects.filter(sender=friendInfo, reciever=userInfo)
    all_chat = (all_chat_sender | all_chat_reciever).order_by("created_at")


    current_day =""
    all_chat_and_first_chat_of_day = {}
    for c in all_chat:
        date = c.created_at
        date += timedelta(hours=7)
        date = date.strftime('%m/%d/%Y')
        if (date != current_day):
            all_chat_and_first_chat_of_day[c] = "1"
            current_day = date
        else:
            all_chat_and_first_chat_of_day[c] = "0"

    return render(request, 'chat/view_chat.html', {
        'userInfo': userInfo,
        'friendInfo': friendInfo,
        'sort_last_chat_friend': sort_last_chat_friend,
        "all_chat_and_first_chat_of_day": all_chat_and_first_chat_of_day,
    })

def delete_message_chat(request, chat_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    chat = Chat.objects.get(id=chat_id)
    id = chat.reciever.user_id.id
    chat.delete()
    return HttpResponseRedirect(reverse('chat:view_chat', args=(id, )))