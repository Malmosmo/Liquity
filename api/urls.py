from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import group, single, profile

urlpatterns = [
    path('group/', group, name="group"),
    path('single/', single, name="single"),
    path('profile/', profile, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
