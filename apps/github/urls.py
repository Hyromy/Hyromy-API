from django.urls import path

from .views import (
    repo,
    repos,
)

urlpatterns = [
    path("repos/<str:repo_name>/", repo),
    path("repos/", repos),
]
