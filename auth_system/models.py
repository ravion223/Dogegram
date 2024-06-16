from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ACCESS_CHOICES = [
        ('user', 'User'),
        ('admin', 'Administrator')
    ]
    username = models.CharField(max_length=93)
    access = models.CharField(max_length=31, choices=ACCESS_CHOICES, default='user')

    def __str__(self) -> str:
        return f"User - {self.username}"
    
    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'