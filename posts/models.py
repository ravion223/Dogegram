from django.db import models
from auth_system.models import CustomUser

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(CustomUser, related_name='liked_post')

    title = models.CharField(max_length=100, blank=True, null=True)
    post_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Post by {self.author.username}"
    
    class Meta:
        ordering = ['creation_date']
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
    
    class Meta:
        ordering = ['creation_date']
        verbose_name = 'Commentary'
        verbose_name_plural = 'Commentaries'