from django.shortcuts import render
from django.views.generic import TemplateView
from auth_system import models
from posts.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

class IndexView(TemplateView):
    template_name = 'main_page/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = models.CustomUserProfile.objects.get(user=self.request.user)
                context['profile'] = profile
            except models.CustomUserProfile.DoesNotExist:
                context['profile'] = None
        else:
            context['profile'] = None
        context['posts'] = Post.objects.all()
        unread_notifications = models.Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        return context