# chat/consumers.py

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

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        self.user = await self.get_user_from_token()
        self.scope['user'] = self.user

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_history()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        if isinstance(self.user, AnonymousUser):
            sender_display_name = "Anonymous"
            sender_user = None
        else:
            sender_display_name = f"{self.user.firstName} {self.user.lastName}".strip() or self.user.email
            sender_user = self.user

        await self.save_message(sender_user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_display_name,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    async def send_history(self):
        messages = await self.get_messages()
        for msg in messages:
            sender = await self.get_message_sender(msg)
            sender_display_name = (
                f"{sender.firstName} {sender.lastName}".strip()
                if sender else "Anonymous"
            )
            await self.send(text_data=json.dumps({
                'message': msg.message,
                'sender': sender_display_name,
            }))

    @sync_to_async
    def get_messages(self):
        return Message.objects.filter(room_name=self.room_name).order_by('-timestamp')[:20][::-1]

    @sync_to_async
    def get_message_sender(self, msg):
        return msg.sender if msg.sender_id else None

    @sync_to_async
    def save_message(self, sender, message):
        Message.objects.create(sender=sender, content=message, room_name=self.room_name)

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
