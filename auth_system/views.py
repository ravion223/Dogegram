from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, SignInForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import DetailView, View, UpdateView
from . import models

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


class ProfileDetailView(DetailView):
    model = models.CustomUserProfile
    template_name = 'auth_system/profile-detail.html'
    context_object_name = 'profile'


def get_my_profile_view(request):
    my_profile = models.CustomUserProfile.objects.get(user=request.user)
    profile = models.CustomUserProfile.objects.get(user=request.user)

    context = {
        'my_profile': my_profile,
        'profile': profile
    }

    return render(
        request,
        'auth_system/my-profile-detail.html',
        context
    )


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