"""cognitev URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/', include('technical_task.urls')),
    #path(r'^docs/', include('rest_framework_docs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
