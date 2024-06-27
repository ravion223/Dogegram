from . import models

def get_friend_request_or_false(sender, receiver):
    try:
        return models.FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except models.FriendRequest.DoesNotExist:
        return False







