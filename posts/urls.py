from django.urls import path
from . import views


urlpatterns = [
    path('create/post/', views.PostCreateView.as_view(), name='create-post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail-post'),
    path('like/post/<int:pk>/', views.like_post, name='like-post')
]

app_name = 'posts'