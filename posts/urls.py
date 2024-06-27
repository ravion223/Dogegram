from django.urls import path
from . import views


urlpatterns = [
    path('create/post/', views.PostCreateView.as_view(), name='create-post'),
]

app_name = 'posts'