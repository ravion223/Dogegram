from typing import Any
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, on_delete=models.CASCADE, related_name='chat_rooms')

    class Meta:
        verbose_name = 'Chat_room'
        verbose_name_plural = 'Chat_rooms'


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)