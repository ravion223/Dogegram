from django.shortcuts import redirect, render
from . import forms

# Create your views here.

def create_community(request):
    if request.method == 'POST':
        form = forms.CommunityCreateForm(request, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.owner = request.user
            community.members.add(request.user)
            community.save()
            return redirect('communities:community-detail', pk=community.id)
    else:
        form = forms.CommunityCreateForm()
    
    context = {
        'form': form,
        'community': community
    }

    return render(request, 'communities/community-create.html', context)