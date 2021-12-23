from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import FriendList, FriendRequest, Profile, User

admin.site.register(Profile)
admin.site.register(FriendList)
admin.site.register(FriendRequest)

admin.site.register(User, UserAdmin)
