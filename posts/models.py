from django.db import models
from django.forms import ValidationError
from auth_system.models import CustomUser
import mimetypes
from communities.models import Community

# Create your models here.
def validate_media_type(value):
    mime = mimetypes.guess_type(value.name)[0]
    if mime not in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/webm']:
        raise ValidationError('Unsupported file type.')


class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(CustomUser, related_name='liked_post', blank=True)

    title = models.CharField(max_length=100, blank=True, null=True)
    post_image = models.FileField(upload_to='posts/', validators=[validate_media_type], blank=True, null=True)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Post by {self.author.username}"
    
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-creation_date']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Commentary(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commentaries')
    likes = models.ManyToManyField(CustomUser, related_name='liked_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commentary_post')

    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Commentary to {self.post.title} by {self.author.username}"
    
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-creation_date']
        verbose_name = 'Commentary'
        verbose_name_plural = 'Commentaries'