from django.db import models
from django.contrib.auth.models import User
from django.utils  import timezone
from channels.db import database_sync_to_async

class Room(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('UserMessanger', related_name='rooms')
    admin = models.ManyToManyField('UserMessanger')
    
    def add_member(self, user):
        self.members.add(user)
        
    def __str__(self):
        return self.name

class UserMessanger(models.Model):
    name = models.ForeignKey(User ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name.username
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, default=1)
    text = models.TextField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)
    
    @staticmethod
    @database_sync_to_async
    def save_message(room_id, message_text):
        from .models import Room, Message
        try:
            print(f"Attempting to save message to Room ID: {room_id}")
            room = Room.objects.get(id=room_id)
            print(f"Room found: {room.name}")
            return Message.objects.create(room=room, text=message_text)
        except Room.DoesNotExist:
            print(f"Room with ID {room_id} does not exist.")
            return None
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
