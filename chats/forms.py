from django import forms
from . import models
import mimetypes

class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ('content', 'media')

    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            mime = mimetypes.guess_type(media.name)[0]
            if mime not in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/webm']:
                raise forms.ValidationError('Unsupported file type.')
        return media