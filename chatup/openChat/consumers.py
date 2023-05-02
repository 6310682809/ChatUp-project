import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Message, OpenChat
from django.contrib.auth.models import User

import sys
sys.path.append("..")

from user.models import UserInfo

import base64

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['openchat_id']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_data):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room = text_data_json['room']
        file = text_data_json['file']
        
        try:
            file_binary = base64.b64decode(file.split(',')[1])

            with open('./new_file.jpg', 'wb') as f:
                f.write(file_binary)
        except:
            file_binary = ''

        message_obj, profile_image, new_date = await self.save_message(username, room, message)

        if message_obj != 'EMPTY':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'file': '',
                    'room': room,
                    'message_id': message_obj.id,
                    'profile_image': profile_image,
                    'new_date': new_date
                }
            )

    async def chat_message(self, event):
        message = event['message']
        file = event['file']
        username = event['username']
        room = event['room']
        message_id = event['message_id']
        profile_image = event['profile_image']
        new_date = event['new_date']

        await self.send(text_data=json.dumps({
            'message': message,
            'file': file,
            'username': username,
            'room': room,
            'message_id': message_id,
            'profile_image': profile_image,
            'new_date': new_date
        }))

    @sync_to_async
    def save_message(self, username, openchat_id, message):
        user = User.objects.get(username=username)
        user_info = UserInfo.objects.get(user_id=user)
        openchat = OpenChat.objects.get(pk=openchat_id)

        format = '%d %B, %Y'

        try:
            last_message = Message.objects.filter(open_chat=openchat).last()
            last_date = last_message.created_at.strftime(format)
        except:
            last_date = None

        if message != "":
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

            profile_image = user_info.profile_image.url

            return message, profile_image, new_date
        else:
            return 'EMPTY'