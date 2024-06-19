from django.shortcuts import render
from django.views.generic import TemplateView
from auth_system import models

# Create your views here.

class IndexView(TemplateView):
    template_name = 'main_page/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        profile = models.CustomUserProfile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context