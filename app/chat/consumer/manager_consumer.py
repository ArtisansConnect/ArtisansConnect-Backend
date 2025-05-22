# chat/consumers/manager_consumer.py

import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Message
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class ManagerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token()
        if isinstance(self.user, AnonymousUser) or not self.user.is_staff:
            await self.close()
            return

        await self.channel_layer.group_add("manager_room", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("manager_room", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        room = data['room']  # Example: "client_5"

        await self.save_message(self.user, room, message)

        await self.channel_layer.group_send(
            room,
            {
                'type': 'chat_message',
                'message': message,
                'sender': "Manager",
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'room': event.get('room', None),
        }))

    @sync_to_async
    def save_message(self, sender, room, content):
        try:
            client_id = int(room.split('_')[1])
            client = User.objects.get(id=client_id)
            Message.objects.create(sender=sender, receiver=client, content=content, room_name=room)
        except (IndexError, ValueError, User.DoesNotExist):
            pass  # log error or handle appropriately

    @sync_to_async
    def get_user_from_token(self):
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        if not token:
            return AnonymousUser()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return User.objects.get(id=payload['user_id'])
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return AnonymousUser()
