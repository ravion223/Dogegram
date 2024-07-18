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

        def clean_media(self):
            post_image = self.cleaned_data.get('post_image')
            if post_image:
                mime = post_image.guess_type(post_image.name)[0]
                if mime not in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/webm']:
                    raise forms.ValidationError('Unsupported file type.')
            return post_image


class PostUpdateForm(forms.models.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'post_image', 'description')
        labels = {
            'title': 'Update the title of your post',
            'post_image': 'Add an image to your post',
            'description': 'Add a content to your post'
        }

        def clean_media(self):
            post_image = self.cleaned_data.get('post_image')
            if post_image:
                mime = post_image.guess_type(post_image.name)[0]
                if mime not in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/webm']:
                    raise forms.ValidationError('Unsupported file type.')
            return post_image


class CommentaryCreateForm(forms.models.ModelForm):
    class Meta:
        model = models.Commentary
        fields = ('content',)