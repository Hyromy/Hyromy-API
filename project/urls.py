from django.contrib import admin
from django.urls import include, path

from apps._ping.urls import urlpatterns as ping_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", include(ping_urls)),
]
