from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from utils.healthcheck import healthcheck

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autos.urls')),
    path("api/health/", healthcheck, name="healthcheck"),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )

handler404 = None  # Ссылка на функцию-обработчик 404
