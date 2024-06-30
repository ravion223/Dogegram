from django import forms
from . import models


class PostCreateForm(forms.models.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'post_image', 'description')
        labels = {
            'title': 'Enter the title of your post (*optional)',
            'post_image': 'Add an image to your post (*optional)',
            'description': 'Add a content to your post (*required)'
        }


class CommentaryCreateForm(forms.models.ModelForm):
    class Meta:
        model = models.Commentary
        fields = ('content',)