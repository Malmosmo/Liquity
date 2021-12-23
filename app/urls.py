from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import drinks, group_single, groups, homepage, overview

urlpatterns = [
    path('', homepage, name="home"),
    path('groups/', groups, name="groups"),
    path('groups/<int:pk>/', group_single, name="group-single"),
    path('drinks/', drinks, name="drinks"),
    path('overview/', overview, name="overview"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
