from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from django.contrib.auth import get_user_model
from auth_system import models as auth_models
# Create your views here.


User = get_user_model()


@login_required
def chat_room(request, room_name):
    room, created = models.ChatRoom.objects.get_or_create(name=room_name)
    messages = models.Message.objects.filter(room=room)

    if request.user not in room.participants.all():
        return redirect('main_page:main-page')

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            models.Message.objects.create(room=room, sender=request.user, content=content)

            participants = room.participants.all()
            friend_user = next(user for user in participants if user != request.user)

            auth_models.Notification.objects.create(user=friend_user, message=f"{request.user.username} has sent you a message!")

            return redirect('chats:chat-room', room_name=room_name)

    return render(request, 'chats/chat_room.html', {
        'room': room,
        'messages': messages,
        'room_name': room_name
    })


def update_message(request, message_id):
    if request.method == 'POST':
        new_text = request.POST.get('new_text')
        message = get_object_or_404(models.Message, id=message_id)
        message.content = new_text
        message.save()
        return JsonResponse({'message': 'Message updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def delete_message(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(models.Message, id=message_id)
        message.delete()
        return JsonResponse({'message': 'Message deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@login_required
def start_chat(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    room_name = f"chat_{min(request.user.id, friend.id)}_{max(request.user.id, friend.id)}"
    room, created = models.ChatRoom.objects.get_or_create(name=room_name)
    
    if created:
        room.participants.set([request.user, friend])
    else:
        current_participants = room.participants.all()
        if current_participants.count() > 2 or request.user not in current_participants or friend not in current_participants:
            room.participants.set([request.user, friend])
    
    return redirect('chats:chat-room', room_name=room_name)