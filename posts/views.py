from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from auth_system import models as auth_models
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
    

class PostDetailView(DetailView):
    model = models.Post
    template_name = 'posts/post-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        form = forms.CommentaryCreateForm()

        if self.request.user.is_authenticated:
            try:
                profile = auth_models.CustomUserProfile.objects.get(user=self.request.user)
                context['profile'] = profile
            except models.CustomUserProfile.DoesNotExist:
                context['profile'] = None
        else:
            context['profile'] = None

        total_likes = post.total_likes()

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        context.update({
            "post": post,
            "commentaries": post.commentary_post.all(),
            "form": form,
            'total_likes': total_likes,
            'liked': liked,
        })

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = forms.CommentaryCreateForm(request.POST)

        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.post = post
            commentary.author = request.user
            commentary.save()
            return redirect('posts:detail-post', pk=post.id)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


def like_post(request, pk):
    post = get_object_or_404(models.Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('posts:detail-post', args=[str(pk)]))