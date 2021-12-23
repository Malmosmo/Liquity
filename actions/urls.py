from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (drink_add, drink_create, drink_delete, friend_add,
                    friend_remove, friend_rq_accept, friend_rq_cancel,
                    friend_rq_decline, group_leave, group_rename,
                    group_user_add, group_user_remove, groups_create,
                    groups_delete, overview_delete, profile_delete,
                    profile_update)

urlpatterns = [
    path('drink/create', drink_create, name="action-drink-create"),
    path('drink/add', drink_add, name="action-drink-add"),
    # drink delete
    path('overview/delete', overview_delete, name="action-overview-delete"),

    path('groups/delete', groups_delete, name="action-groups-delete"),
    path('groups/create', groups_create, name="action-groups-create"),

    path('group/rename/<int:pk>', group_rename, name="action-group-rename"),
    path('group/remove/<int:pk>', group_user_remove, name="action-group-remove"),
    path('group/leave/<int:pk>', group_leave, name="action-group-leave"),
    path('group/add/<int:pk>', group_user_add, name="action-group-add"),

    path('profile/delete/<int:pk>', profile_delete, name="action-profile-delete"),
    path('profile/update/<int:pk>', profile_update, name="action-profile-update"),

    path('friend/add/<int:pk>', friend_add, name="action-friend-add"),
    path('friend/remove/<int:pk>', friend_remove, name="action-friend-remove"),

    path('friend/accept/<int:pk>', friend_rq_accept, name="action-friend-accept"),
    path('friend/decline/<int:pk>', friend_rq_decline, name="action-friend-decline"),
    path('friend/cancel/<int:pk>', friend_rq_cancel, name="action-friend-cancel"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
