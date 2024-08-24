from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
import mimetypes

from django.forms import ValidationError

User = get_user_model()

# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')

    class Meta:
        verbose_name = 'Chat_room'
        verbose_name_plural = 'Chat_rooms'


def validate_media_type(value):
    mime = mimetypes.guess_type(value.name)[0]
    if mime not in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/webm']:
        raise ValidationError('Unsupported file type.')


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    media = models.FileField(blank=True, validators=[validate_media_type], null=True, upload_to='chats/')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']