from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("admin_dash/", include("useradmin.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, media_root=settings.MEDIA_ROOT)
