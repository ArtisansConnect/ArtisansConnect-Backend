# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Message
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send_history()

    async def send_history(self):
        from asgiref.sync import sync_to_async
        messages = await sync_to_async(list)(
            Message.objects.filter(room_name=self.room_name).order_by('-timestamp')[:50]
        )
        for msg in reversed(messages):
            await self.send(text_data=json.dumps({
                'message': msg.message,
                'sender': msg.sender,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }))    

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data.get('sender', 'Anonymous')

        # 1. Save to DB
        await self.save_message(sender, self.room_name, message)

        # 2. Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @staticmethod
    async def save_message(sender, room, message):
        from asgiref.sync import sync_to_async
        await sync_to_async(Message.objects.create)(
            sender=sender,
            room_name=room,
            message=message
        )
