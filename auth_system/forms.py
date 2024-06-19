from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser, CustomUserProfile


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')


class SignInForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = CustomUserProfile
        fields = ('first_name', 'last_name', 'bio', 'profile_pic')
        labels = {
            'first_name': 'Update your first_name',
            'last_name': 'Update your last_name',
            'bio': 'Update your bio',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['bio'].required = False
        self.fields['profile_pic'].required = False