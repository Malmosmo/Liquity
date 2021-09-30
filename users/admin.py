from django.contrib import admin

from .models import FriendList, FriendRequest, Profile

admin.site.register(Profile)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
