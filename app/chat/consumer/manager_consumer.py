import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from core.models import Message, CustomUser  # Adjust import paths as needed


class ManagerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user_from_token()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        if isinstance(self.user, AnonymousUser) or not self.user.is_staff:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        # Send all previous messages in the room
        messages = await self.get_messages(self.room_name)
        for msg in messages:
            await self.send(text_data=json.dumps(msg))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if message:
            await self.save_message(self.room_name, self.user, message)

            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": f"{self.user.firstName} {self.user.lastName}".strip(),
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    @database_sync_to_async
    def get_user_from_token(self):
        query_string = self.scope["query_string"].decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        if not token:
            return AnonymousUser()

        try:
            validated_token = AccessToken(token)
            user_id = validated_token["user_id"]
            return CustomUser.objects.get(id=user_id)
        except Exception:
            return AnonymousUser()

    @database_sync_to_async
    def save_message(self, room_name, sender, content):
        return Message.objects.create(room_name=room_name, sender=sender, content=content)

    @database_sync_to_async
    def get_messages(self, room_name):
        messages = Message.objects.filter(room_name=room_name).select_related("sender").order_by("timestamp")
        return [
            {
                "message": msg.content,
                "timestamp": str(msg.timestamp),
                "sender": f"{msg.sender.firstName} {msg.sender.lastName}".strip() if msg.sender else "Unknown",
            }
            for msg in messages
        ]
