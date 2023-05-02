from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from chat.models import Notification

from user.models import *
from .models import *

from .consumers import ChatConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user_id=user)

        my_openchats = OpenChat.objects.filter(members__pk=user_info.id)
        all_openchats = OpenChat.objects.all().difference(my_openchats)

        return render(request, 'openChat/index.html', {
            'user': user,
            'user_info': user_info,
            'my_openchats': my_openchats,
            'all_openchats': all_openchats
        })

def create_openchat(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user_id=user)

        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['description']

            openchat = OpenChat.objects.create(
                name = name,
                description = description,
                created_by = user_info
            )
            openchat.members.add(user_info)
            openchat.save()

            return HttpResponseRedirect(reverse('openchat:index'))
        else:
            return render(request, 'openChat/create_openChat.html', {
            'user': user,
            'user_info': user_info
        })

def view_openchat(request, openchat_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user_id=user)

        openchats = [opc for opc in OpenChat.objects.filter(members__pk=user_info.id)]
        openchat = OpenChat.objects.filter(pk=openchat_id, members__pk=user_info.id).first()

        if request.method == 'POST':
            message = request.POST['message']
            files = request.FILES.getlist('img')

            room_group_name = f'chat_{openchat_id}'
            channel_layer = get_channel_layer()

            format = '%d %B, %Y'
            try:
                last_message = Message.objects.filter(open_chat=openchat).last()
                last_date = last_message.created_at.strftime(format)
            except:
                last_date = None

            profile_image = user_info.profile_image.url
            
            if message:
                message = Message.objects.create(
                    created_by=user_info,
                    open_chat=openchat,
                    message=message,
                )
                message.save()

                add_message = Message.objects.filter(open_chat=openchat).last()
                check_date = add_message.created_at.strftime(format)

                if last_date != check_date or last_date == None:
                    new_date = check_date
                else:
                    new_date = None

                async_to_sync(channel_layer.group_send)(
                    room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message.message,
                        'file': '',
                        'username': user.username,
                        'room': openchat_id,
                        'message_id': message.id,
                        'profile_image': profile_image,
                        'new_date': new_date
                    }
                )

            for file in files:
                try:
                    last_message = Message.objects.filter(open_chat=openchat).last()
                    last_date = last_message.created_at.strftime(format)
                except:
                    last_date = None
                
                message = Message.objects.create(
                    created_by=user_info,
                    open_chat=openchat,
                    message='',
                    file=file,
                )
                message.save()

                add_message = Message.objects.filter(open_chat=openchat).last()
                check_date = add_message.created_at.strftime(format)

                if last_date != check_date or last_date == None:
                    new_date = check_date
                else:
                    new_date = None

                async_to_sync(channel_layer.group_send)(
                    room_group_name,
                    {
                        'type': 'chat_message',
                        'message': '',
                        'file': message.file.url,
                        'username': user.username,
                        'room': openchat_id,
                        'message_id': message.id,
                        'profile_image': profile_image,
                        'new_date': new_date
                    }
                )
            recievers = openchat.members.exclude(user_id=user)
            for reciever in recievers:
                Notification.objects.create(
                    openchat = openchat,
                    detail = f"{user_info} has sent message to {openchat}",
                    create_by = user,
                    reciever = reciever.user_id,
                ).save()
            return HttpResponseRedirect(reverse('openchat:view_openchat', kwargs={'openchat_id':openchat_id}))
        
        lastest_message = ''
        for opc in openchats:
            try:
                message = Message.objects.filter(open_chat=opc).last()

                if message.created_by != user_info:
                    lastest_message += message.created_by.user_id.username + ': '

                if message.message:
                    opc.lastest_message = lastest_message + message.message
                else:
                    opc.lastest_message = lastest_message + 'sent file'
            except:
                opc.lastest_message = ''

        if openchat is not None:
            messages = Message.objects.filter(open_chat=openchat)

            show_date = None
            for message in messages:
                create_at = message.created_at
                format = '%H:%M'
                message.created_at = create_at.strftime(format)

                format = '%d %B, %Y'
                message.show_date = create_at.strftime(format)

                if show_date == None or show_date != message.show_date:
                    show_date = message.show_date
                else:
                    message.show_date = None
                
            return render(request, 'openChat/openChat_room.html', {
                'user_info': user_info,
                'openchats': openchats,
                'openchat': openchat,
                'messages': messages
            })
        else:
            return HttpResponseRedirect(reverse('openchat:index'))
    
def update_openchat(request, openchat_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user_id=user)

        friends = [friend.friend_id for friend in Friend.objects.filter(user_id=user_info)]

        openchat = OpenChat.objects.filter(pk=openchat_id, members__pk=user_info.id).first()

        if openchat is None:
            return HttpResponseRedirect(reverse('openchat:index'))

        members = [val for val in openchat.members.all()]

        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['description']

            try:
                group_image = request.FILES.getlist('images')[0]

                openchat = OpenChat.objects.get(pk=openchat_id, created_by=user_info)
                openchat.group_image = group_image
                openchat.save()
            except:
                pass

            OpenChat.objects.filter(pk=openchat_id, created_by=user_info).update(
                name =  name,
                description = description
            )

            return HttpResponseRedirect(reverse('openchat:view_openchat', kwargs={'openchat_id':openchat_id}))
        else:
            return render(request, 'openChat/update_openChat.html', {
            'user': user,
            'user_info': user_info,
            'openchat': openchat,
            'members': members,
            'friends': friends,
            'openchat_id': openchat_id,
        })

def remove_member(request, openchat_id, member_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user_id=user)

        openchat = OpenChat.objects.get(pk=openchat_id, created_by=user_info)
        member = UserInfo.objects.get(pk=member_id)

        openchat.members.remove(member)
        openchat.save()

        if openchat.members.count() == 0:
            return HttpResponseRedirect(reverse('openchat:delete_openchat', kwargs={'openchat_id':openchat_id}))

        openchat = OpenChat.objects.filter(pk=openchat_id).first()

        OpenChat.objects.filter(pk=openchat_id).update(
            created_by = openchat.members.first()
        )

        return HttpResponseRedirect(reverse('openchat:update_openchat', kwargs={'openchat_id':openchat_id}))
    
def delete_openchat(request, openchat_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        openchat = OpenChat.objects.get(pk=openchat_id)

        if openchat is not None:
            openchat.delete()

        return HttpResponseRedirect(reverse('openchat:index'))
    
def join_openchat(request, openchat_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user_id=user)

        openchat = OpenChat.objects.get(pk=openchat_id)
        openchat.members.add(user_info)
        openchat.save()

        return HttpResponseRedirect(reverse('openchat:view_openchat', kwargs={'openchat_id':openchat_id}))

def leave_openchat(request, openchat_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user_id=user)

        openchat = OpenChat.objects.get(pk=openchat_id, members__pk=user_info.id)

        openchat.members.remove(user_info)
        openchat.save()

        openchat = OpenChat.objects.get(pk=openchat_id)

        if openchat.members.count() == 0:
            return HttpResponseRedirect(reverse('openchat:delete_openchat', kwargs={'openchat_id':openchat_id}))

        return HttpResponseRedirect(reverse('openchat:update_openchat', kwargs={'openchat_id':openchat_id}))
    
def delete_message(request, openchat_id, message_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    else:
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user_id=user)

        message = Message.objects.filter(pk=message_id, created_by=user_info)

        if message is not None:
            Message.objects.filter(pk=message_id).delete()

        return HttpResponseRedirect(reverse('openchat:view_openchat', kwargs={'openchat_id':openchat_id}))