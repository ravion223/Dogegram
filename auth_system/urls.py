from django.urls import path
from . import views

app_name = 'auth_system'

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('log-out/', views.logout_view, name='log-out'),
    path('profile/<int:pk>/', views.profile_view, name='profile-detail'),
    # path('my-profile/', views.get_my_profile_view, name='my-profile-detail'),
    path('my-profile/update/', views.update_profile_view, name='my-profile-update'),
    # path('send_friend_request/<int:to_user_id>', views.send_friend_request, name='send_friend_request'),
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),

]