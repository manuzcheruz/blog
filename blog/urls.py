from django.contrib import admin
#from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'', include('nice.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
