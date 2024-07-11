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


class PostUpdateForm(forms.models.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'post_image', 'description')
        labels = {
            'title': 'Update the title of your post',
            'post_image': 'Add an image to your post',
            'description': 'Add a content to your post'
        }


class CommentaryCreateForm(forms.models.ModelForm):
    class Meta:
        model = models.Commentary
        fields = ('content',)