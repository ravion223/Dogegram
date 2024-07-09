from django.urls import path
from . import views


urlpatterns = [
    path('create/post/', views.PostCreateView.as_view(), name='create-post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail-post'),
    path('like/post/<int:pk>/', views.like_post, name='like-post'),
    path('like-post/<int:post_id>/', views.like_post_main, name='like-post-main'),
    path('update-text/<int:comment_id>/', views.update_text, name='update-comment'),
    path('delete-comment/<int:comment_id>/', views.delete_commentary, name='delete-commentary')
]

app_name = 'posts'