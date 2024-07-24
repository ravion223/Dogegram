from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('community/create/', views.create_community, name='community-create'),
    path('community/<int:pk>/', views.CommunityDetailView.as_view(), name='community-detail'),
    path('community/<int:pk>/update/', views.CommunityUpdateView.as_view(), name='community-update'),
    path('community/<int:pk>/delete/', views.CommunityDeleteView.as_view(), name='community-delete')
]