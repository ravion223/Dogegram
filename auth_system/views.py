from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, SignInForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, View, UpdateView, ListView
from . import models
from .utils import get_friend_request_or_false
from .friend_request_status import FriendRequestStatus

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


def profile_view(request, *args, **kwargs):
    context = {}
    profile_id = kwargs.get('pk')
    try:
        profile = models.CustomUserProfile.objects.get(pk=profile_id)
    except models.CustomUserProfile.DoesNotExist:
        return HttpResponse('Profile not found.')

    context['profile'] = profile
    user = profile.user

    try:
        friend_list = models.FriendList.objects.get(user=user)
    except models.FriendList.DoesNotExist:
        friend_list = models.FriendList(user=user)
        friend_list.save()

    friends = friend_list.friends.all()
    context['friends'] = friends
    five_friends = friend_list.get_first_five_friends()
    context['five_friends'] = five_friends

    is_self = True
    is_friend = False
    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

    if request.user.is_authenticated:
        if request.user != user:
            is_self = False
            if friends.filter(pk=request.user.id).exists():
                is_friend = True
            else:
                is_friend = False
                if get_friend_request_or_false(sender=user, receiver=request.user):
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=user, receiver=request.user).id
                elif get_friend_request_or_false(sender=request.user, receiver=user):
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
        else:
            try:
                friend_requests = models.FriendRequest.objects.filter(receiver=request.user, is_active=True)
            except models.FriendRequest.DoesNotExist:
                friend_requests = None
    else:
        is_self = False

    context['is_self'] = is_self
    context['is_friend'] = is_friend
    context['request_sent'] = request_sent
    context['friend_requests'] = friend_requests if is_self else None
    context['posts'] = user.posts.all()

    return render(
        request,
        'auth_system/profile-detail.html',
        context
    )

# class ProfileDetailView(DetailView):
#     model = models.CustomUserProfile
#     template_name = 'auth_system/profile-detail.html'
#     context_object_name = 'profile'


# def get_my_profile_view(request):
#     my_profile = models.CustomUserProfile.objects.get(user=request.user)
#     profile = models.CustomUserProfile.objects.get(user=request.user)

#     context = {
#         'my_profile': my_profile,
#         'profile': profile
#     }

#     return render(
#         request,
#         'auth_system/my-profile-detail.html',
#         context
#     )


def update_profile_view(request):
    if request.method == 'POST':
        profile = models.CustomUserProfile.objects.get(user=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/my-profile/')
    else:
        form = ProfileUpdateForm()
        profile = models.CustomUserProfile.objects.get(user=request.user)
    
    context = {
        'form': form,
        'profile': profile
    }

    return render(
        request,
        'auth_system/my-profile-update.html',
        context
    )

# @login_required
# def send_friend_request(request, to_user_id):
#     if request.method == 'POST':
#         to_user = models.CustomUser.objects.get(id=to_user_id)
#         if to_user != request.user:
#             friendship, created = models.Friendship.objects.get_or_create(from_user=request.user, to_user=to_user)
#             if created:
#                 messages.success(request, f'Friend request sent to {to_user.username}.')
#                 models.Notification.objects.create(user=to_user, message=f'{request.user.username} has sent you friend request!')
#             else:
#                 messages.warning(request, f'Friend request already sent to {to_user.username}.')
#         else:
#             messages.error(request, 'You cannot send a friend request to yourself.')

#     return redirect(
#         'auth_system:profile-detail',
#         pk=to_user_id
#     )


# def accept_friend_request(request, from_user):
#     friendship = models.Friendship.objects.get(from_user=from_user, to_user=request.user)
#     friendship.status = 'accepted'
#     friendship.save()
#     return friendship


# def remove_friend(request, other_user):
#     models.Friendship.objects.filter(
#         models.Q(from_user=request.user, to_user=other_user) |
#         models.Q(from_user=other_user, to_user=request.user)
#     ).delete()


# def friends(request):
#     friends = models.Friendship.objects.filter(
#         models.Q(from_user=request.user, status='accepted') |
#         models.Q(to_user=request.user, status='accepted')
#     ).select_related('from_user', 'to_user')
#     return [f.from_user if f.from_user != request.user else f.to_user for f in friends]


class NotificationListView(ListView):
    model = models.Notification
    template_name = 'auth_system/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user).order_by("-timestamp")