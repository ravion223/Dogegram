from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.CustomUser)
admin.site.register(models.CustomUserProfile)

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = models.FriendList

admin.site.register(models.FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender__username', 'receiver__username']

    class Meta:
        model = models.FriendRequest

admin.site.register(models.FriendRequest, FriendRequestAdmin)