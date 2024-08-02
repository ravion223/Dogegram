from django.db import models
from django.forms import ValidationError
from auth_system.models import CustomUser
import mimetypes


# Create your models here.

class Community(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='communities')
    members = models.ManyToManyField(CustomUser, related_name='community_members')

    name = models.CharField(max_length=100)
    description = models.TextField()
    community_logo = models.ImageField(upload_to='communities/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} community"
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'