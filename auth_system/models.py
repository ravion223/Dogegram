from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ACCESS_CHOICES = [
        ('user', 'User'),
        ('admin', 'Administrator')
    ]
    username = models.CharField(max_length=93, unique=True)
    access = models.CharField(max_length=31, choices=ACCESS_CHOICES, default='user')

    def __str__(self) -> str:
        return f"User - {self.username}"
    
    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class CustomUserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profiles')
    followers = models.ManyToManyField(CustomUser, related_name='followed_profile')

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField()
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile/')
    creation_date = models.DateField(auto_now_add=True)

    def total_followers(self):
        return self.followers.count()

    def __str__(self) -> str:
        return f'Profile of {self.user.username} user'
    
    class Meta:
        ordering = ['creation_date']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'