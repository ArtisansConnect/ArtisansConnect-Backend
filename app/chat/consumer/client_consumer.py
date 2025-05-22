import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Message
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token()
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.room_name = f"client_{self.user.id}"
        self.scope['user'] = self.user

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        await self.send_history()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data['message']

        # Save the client's message
        await self.save_message(self.user, None, content)

        # Forward the message to the manager group
        await self.channel_layer.group_send(
            "manager_room",
            {
                'type': 'chat_message',
                'message': content,
                'sender': f"{self.user.firstName} {self.user.lastName}".strip() or self.user.email,
                'room': self.room_name,
            }
        )

    async def chat_message(self, event):
        if event.get('room') == self.room_name:
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'sender': event['sender'],
            }))

    async def send_history(self):
        messages = await sync_to_async(self.get_messages)()
        for msg in messages:
            await self.send(text_data=json.dumps({
                "message": msg.content,
                "timestamp": str(msg.timestamp),
                "sender": msg.sender_id,
            }))

    def get_messages(self): 
        return list(Message.objects.filter(room_name=self.room_name).order_by('timestamp'))



    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            room_name=f"client_{sender.id}"
        )

    @database_sync_to_async
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
