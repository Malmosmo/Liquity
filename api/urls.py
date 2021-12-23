from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from api.views import group, profile, _all

urlpatterns = [
    path('group/<uuid:pk>', group, name="api-group"),
    path('profile/', profile, name="api-profile"),
    path('all/', _all, name="api-all"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
