from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from . import models
from . import forms

# Create your views here.

# class PostListView(ListView):
#     model = models.Post
#     template_name = 'main_page/index.html'
#     context_object_name = 'posts'



class PostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostCreateForm
    template_name = 'posts/post-create.html'
    success_url = reverse_lazy('main_page:main-page')

    def form_valid(self, form) -> HttpResponse:
        form.instance.author.id = self.request.user.id
        return super().form_valid(form)