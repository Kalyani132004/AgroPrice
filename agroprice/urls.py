"""Root URL configuration — includes every app's URLconf under its namespace."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include(("core.urls", "core"), namespace="core")),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("crops/", include(("crops.urls", "crops"), namespace="crops")),
    path("prices/", include(("prices.urls", "prices"), namespace="prices")),
    path("analytics/", include(("analytics.urls", "analytics"), namespace="analytics")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),

    path("api/v1/", include(("api.urls", "api"), namespace="api")),
]

# Custom error handlers
handler404 = "core.views.error_404_view"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
