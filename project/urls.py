from django.contrib import admin
from django.urls import include, path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.github.urls import urlpatterns as github_urls


@api_view(["GET"])
@permission_classes([AllowAny])
def ping(request: Request) -> Response:
    return Response({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", ping),
    path("github/", include(github_urls)),
]
