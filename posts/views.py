from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from auth_system import models as auth_models
from . import models
from . import forms
from communities.models import Community

# Create your views here.

# class PostListView(ListView):
#     model = models.Post
#     template_name = 'main_page/index.html'
#     context_object_name = 'posts'



class PostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostCreateForm
    template_name = 'posts/post-create.html'

    def get_success_url(self) -> str:
        community_id = self.kwargs.get('community_id')
        if community_id:
            return reverse_lazy('communities:community-detail', kwargs={'pk': community_id})
        else:
            return reverse_lazy('main_page:main-page')

    def form_valid(self, form, **kwargs) -> HttpResponse:
        form.instance.author = self.request.user
        community_id = self.kwargs.get('community_id')
        if community_id:
            community = get_object_or_404(Community, id=community_id)
            form.instance.community = community
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community_id = self.kwargs.get('community_id')
        if community_id:
            context['community'] = get_object_or_404(Community, id=community_id)
        return context
    

class PostUpdateView(UpdateView):
    model = models.Post
    form_class = forms.PostUpdateForm
    template_name = 'posts/post-update.html'
    
    def get_success_url(self, **kwargs) -> str:
        return reverse_lazy('posts:detail-post', kwargs={'pk': self.object.id})


def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(models.Post, id=post_id)
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully'}) and  redirect('main_page:main-page')
    else:
        return JsonResponse({'error': 'Invalid request method'})


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
        auth_models.Notification.objects.create(user=post.author, message=f"{request.user.username} liked your post!")

    return HttpResponseRedirect(reverse('posts:detail-post', args=[str(pk)]))


def like_comment(request, pk, post_id):
    comment = get_object_or_404(models.Commentary, pk=pk)
    liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
        auth_models.Notification.objects.create(user=comment.author, message=f"{request.user.username} liked your comment!")

    return HttpResponseRedirect(reverse('posts:detail-post', args=[str(post_id)]))


def update_text(request, comment_id):
    if request.method == 'POST':
        new_text = request.POST.get('new_text')
        commentary = get_object_or_404(models.Commentary, id=comment_id)
        commentary.content = new_text
        commentary.save()
        return JsonResponse({'message': 'Text updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def delete_commentary(request, comment_id):
    if request.method == 'POST':
        commentary = get_object_or_404(models.Commentary, id=comment_id)
        commentary.delete()
        return JsonResponse({'message': 'Commentary deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})