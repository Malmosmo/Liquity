from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (drink_add, drink_create, friend_add,
                    friend_remove, friend_rq_accept, friend_rq_cancel,
                    friend_rq_decline, group_leave, group_rename,
                    group_user_add, group_user_remove, groups_create,
                    groups_delete, overview_delete, profile_delete,
                    profile_update)

urlpatterns = [
    path('drink/create', drink_create, name="action-drink-create"),
    path('drink/add', drink_add, name="action-drink-add"),
    # drink delete
    path('overview/delete/<uuid:pk>', overview_delete, name="action-overview-delete"),

    path('groups/delete/<uuid:pk>', groups_delete, name="action-groups-delete"),
    path('groups/create', groups_create, name="action-groups-create"),

    path('group/rename/<uuid:pk>', group_rename, name="action-group-rename"),
    path('group/remove/<uuid:pk>/<uuid:user_pk>', group_user_remove, name="action-group-remove"),
    path('group/leave/<uuid:pk>', group_leave, name="action-group-leave"),
    path('group/add/<uuid:pk>', group_user_add, name="action-group-add"),

    path('profile/delete/<uuid:pk>', profile_delete, name="action-profile-delete"),
    path('profile/update/<uuid:pk>', profile_update, name="action-profile-update"),

    path('friend/add/<uuid:pk>', friend_add, name="action-friend-add"),
    path('friend/remove/<uuid:pk>', friend_remove, name="action-friend-remove"),

    path('friend/accept/<uuid:pk>', friend_rq_accept, name="action-friend-accept"),
    path('friend/decline/<uuid:pk>', friend_rq_decline, name="action-friend-decline"),
    path('friend/cancel/<uuid:pk>', friend_rq_cancel, name="action-friend-cancel"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
