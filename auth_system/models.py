from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

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

    def get_friends(self):
        friendships1 = Friendship.objects.filter(user1=self)
        friendships2 = Friendship.objects.filter(user2=self)
        friends = set()
        for friendship in friendships1:
            friends.add(friendship.user2)
        for friendship in friendships2:
            friends.add(friendship.user1)
        return friends

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


class Friendship(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='friendship_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='friendship_user2', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Friendship between {self.user1.username} and {self.user2.username}"

@receiver(m2m_changed, sender=CustomUserProfile.followers.through)
def update_friendships(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ["post_add", "post_remove"]:
        for follower_pk in pk_set:
            follower = CustomUser.objects.get(pk=follower_pk)
            follower_profile = follower.profiles.first()
            if follower_profile:
                # Check if mutual following exists
                if instance.user in follower_profile.followers.all() and follower in instance.followers.all():
                    # Create friendship if mutual following exists
                    Friendship.objects.get_or_create(user1=instance.user, user2=follower)
                    Friendship.objects.get_or_create(user1=follower, user2=instance.user)
                else:
                    # Delete friendship if mutual following does not exist
                    Friendship.objects.filter(user1=instance.user, user2=follower).delete()
                    Friendship.objects.filter(user1=follower, user2=instance.user).delete()


models.signals.m2m_changed.connect(update_friendships, sender=CustomUserProfile.followers.through)
        

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)