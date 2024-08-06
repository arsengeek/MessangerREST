import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    
    @staticmethod
    @database_sync_to_async
    def save_message(room_id, message_text):
        from .models import Room, Message
        try:
            room = Room.objects.get(id=room_id)
            return Message.objects.create(room=room, text=message_text)
        except Room.DoesNotExist:
            print(f"Room with ID {room_id} does not exist.")
            return None
        except Exception as e:
            print(f"Error saving message: {e}")
            return None

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')
        room_id = self.scope['url_route']['kwargs']['room_id']

        await self.save_message(room_id, message_text)
        print(f"Received data: {text_data}")
        message = data['message']
        print(f"Processing message: {message}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
