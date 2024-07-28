from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, SignInForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, View, UpdateView, ListView
from . import models
from .utils import get_friend_request_or_false
from django.contrib.auth.views import LoginView

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth_system:sign-in')
    else:
        form = SignUpForm()
    
    return render(
        request,
        'auth_system/sign-up.html',
        {'form': form}
    )


def login_view(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page:main-page')
            else:
                messages.error(request, "Wrong username or password")
    else:
        form = SignInForm()

    return render(
        request,
        'auth_system/sign-in.html',
        {'form': form}
    )



def logout_view(request):
    logout(request)
    return redirect('auth_system:sign-in')


@login_required
def profile_view(request, **kwargs):
    profile_id = kwargs.get('pk')
    user = get_object_or_404(models.CustomUser, id=profile_id)
    profile = user.profiles.first()
    is_friend = False

    if request.user.is_authenticated:
        is_friend = models.Friendship.objects.filter(
            user1=request.user, user2=user
        ).exists()

    friendships = models.Friendship.objects.filter(user1=user) | models.Friendship.objects.filter(user2=user)
    friends = set()
    for friendship in friendships:
        if friendship.user1 == user:
            friends.add(friendship.user2)
        else:
            friends.add(friendship.user1)

    context = {
        'profile_user': user,
        'profile': profile,
        'is_friend': is_friend,
        'posts': user.posts.all(),
        'friends': friends
    }
    return render(request, 'auth_system/profile-detail.html', context)


def update_profile_view(request):
    profile = models.CustomUserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('auth_system:profile-detail', profile.id)
    else:
        form = ProfileUpdateForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile
    }

    return render(
        request,
        'auth_system/my-profile-update.html',
        context
    )


def follow_unfollow_view(request, profile_id):
    profile = get_object_or_404(models.CustomUserProfile, id=profile_id)
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
        models.Notification.objects.create(user=profile.user, message=f"{request.user.username} started following you")
    return redirect('auth_system:profile-detail', pk=profile_id)

class NotificationListView(ListView):
    model = models.Notification
    template_name = 'auth_system/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user).order_by("-timestamp")