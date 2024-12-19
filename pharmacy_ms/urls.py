from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index
from useradmin.views import invoices

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("admin_dash/", include("useradmin.urls")),
    path('invoices/<int:sale_id>/', invoices.invoice, name='invoice')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
