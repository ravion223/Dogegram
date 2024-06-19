from django.urls import path
from . import views

app_name = 'auth_system'

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('log-out/', views.logout_view, name='log-out'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('my-profile/', views.get_my_profile_view, name='my-profile-detail'),
    path('my-profile/update/', views.update_profile_view, name='my-profile-update')
]