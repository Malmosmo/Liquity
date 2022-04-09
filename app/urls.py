from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import drinks, group_single, groups, homepage, overview, drink_edit

urlpatterns = [
    path('', homepage, name="home"),

    path('drinks/', drinks, name="drinks"),
    path('drinks/edit/<uuid:pk>', drink_edit, name="drink-edit"),

    path('overview/', overview, name="overview"),

    path('groups/', groups, name="groups"),
    path('groups/<uuid:pk>/', group_single, name="group-single"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
