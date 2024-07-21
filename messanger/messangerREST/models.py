from django.db import models
from django.contrib.auth.models import User
from django.utils  import timezone


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
    
