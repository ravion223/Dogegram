from django.shortcuts import render
from django.views.generic import TemplateView
from auth_system import models
from posts.models import Post
from communities.models import Community
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
        context['communities'] = Community.objects.all()
        unread_notifications = models.Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        return context
    

def search_view(request):
    query = request.GET.get('q', '')
    users = models.CustomUser.objects.filter(username__icontains=query)
    posts = Post.objects.filter(description__icontains=query)
    
    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'main_page/search-results.html', context)