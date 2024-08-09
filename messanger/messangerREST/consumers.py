import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    
    @staticmethod
    @database_sync_to_async
    def save_message(room_id, message_text, user):
        from .models import Room, Message, User
        try:
            print(f"Пытаемся сохранить сообщение в комнату с ID: {room_id}")
            room = Room.objects.get(id=room_id)
            print(f"Комната найдена: {room.name}")
            
            # Проверьте пользователя
            sender = User.objects.get(id=user.id)  # Используем текущего пользователя
            print(f"Пользователь найден: {sender.username}")
            
            # Создайте сообщение
            new_message = Message.objects.create(room=room, text=message_text, sender=sender)
            print(f"Сообщение сохранено: {new_message.id}")
        except Room.DoesNotExist:
            print(f"Комната с ID {room_id} не существует.")
            return None
        except User.DoesNotExist:
            print(f"Пользователь с ID {user.id} не существует.")
            return None
        except Exception as e:
            print(f"Ошибка при сохранении сообщения: {e}")
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
        message = data.get('message')
        user = self.scope['user'] 
        room_id = self.room_id

        await self.save_message(room_id, message, user)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event.get('sender', 'Unknown sender') 
        time = event.get('time', 'Unknown time')

        await self.send(text_data=json.dumps({
        'message': message,
        'sender': sender,
        'time': time,
    }))