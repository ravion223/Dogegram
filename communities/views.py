from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from . import forms
from . import models

# Create your views here.

def create_community(request):
    if request.method == 'POST':
        form = forms.CommunityCreateForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.owner = request.user
            community.save()
            community.members.add(request.user)
            return redirect('communities:community-detail', pk=community.id)
    else:
        form = forms.CommunityCreateForm()
    
    context = {
        'form': form
    }

    return render(request, 'communities/community-create.html', context)


class CommunityDetailView(generic.DetailView):
    model = models.Community
    template_name = 'communities/community-detail.html'
    context_object_name = 'community'

class CommunityUpdateView(generic.UpdateView):
    model = models.Community
    form_class = forms.CommunityUpdateForm
    template_name = 'communities/community-update.html'
    
    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('communities:community-detail', kwargs={'pk': self.object.pk})


class CommunityDeleteView(generic.DeleteView):
    model = models.Community
    template_name = 'communities/community-delete.html'
    success_url = reverse_lazy('main_page:main-page')