from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/', views.chat_room, name='chat-room'),
    path('start_chat/<int:friend_id>/', views.start_chat, name='start-chat'),
    path('update-message/<int:message_id>/', views.update_message, name='update-message'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete-message'),
    path('chat/<str:room_name>/check_new_messages/', views.check_new_messages, name='check-new-messages')
]

app_name = 'chats'