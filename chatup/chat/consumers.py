import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from user.models import UserInfo
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.roomGroupName = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName ,
            self.channel_name
        )
            
    async def sendMessage(self, event) :
        type = event["type"]
        message = event["message"]
        filePath = event["filePath"]
        username = event["username"]
        receiver = event["receiver"]
        img_profile = event["img_profile"]
        date = event["date"]
        chat_id = event["chat_id"]
        await self.send(text_data = json.dumps({"type":type, "message":message, "filePath":filePath, "username":username, "receiver": receiver, 
                                                "roomGroupName" : self.roomGroupName, "img_profile" : img_profile, "date" : date, "chat_id": chat_id}))

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']
        print(connection_type)
        online_status =  await self.change_online_status(username, connection_type)
        # await self.channel_layer.group_send(
        #         self.room_group_name,{
        #             "username" : "username" ,
        #             "online_status" : online_status ,
        #         })

    async def send_onlineStatus(self, event):
        username = event['username']
        online_status = event['status']
        await self.send(text_data=json.dumps({
            'username':username,
            'online_status':online_status
        }))

    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def change_online_status(self, username, c_type):
        user = User.objects.get(username=username)
        userInfo = UserInfo.objects.get(user_id=user)
        if c_type == 'open':
            userInfo.online_status = True
            userInfo.save()
        else:
            userInfo.last_logout = timezone.now()
            userInfo.save(update_fields=['last_logout'])
            userInfo.online_status = False
            userInfo.save()
        return userInfo.online_status