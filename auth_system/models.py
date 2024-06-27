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


# class Friendship(models.Model):
#     from_user = models.ForeignKey(CustomUser, related_name='friendship_requests_sent', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(CustomUser, related_name='friendship_requests_received', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=[('requested', 'Requested'), ('accepted', 'Accepted')], default='requested')
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('from_user', 'to_user')

#     def __str__(self):
#         return f"{self.from_user.username} to {self.to_user.username} ({self.status})"


class FriendList(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(CustomUser, blank=True, related_name='friends')

    def __str__(self) -> str:
        return self.user.username
    
    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False
    
    def get_first_five_friends(self):
        return self.friends.all()[:5]


class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')

    is_active = models.BooleanField(default=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.sender.username
    
    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
        

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)