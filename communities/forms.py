from django import forms
from . import models

class CommunityCreateForm(forms.ModelForm):
    class Meta:
        model = models.Community
        fields = ('name', 'description', 'community_logo')


class CommunityUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Community
        fields = ('name', 'description', 'community_logo')