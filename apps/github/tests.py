from unittest.mock import patch

import pytest
from httpx import HTTPStatusError, Request, Response
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@patch("apps.github.views.cache_handler.get_set")
def test_github_repo_view_success(mock, client):
    mock.return_value = {"name": "hyromy-api", "stars": 10}

    response = client.get("/github/repos/hyromy-api/")

    assert response.status_code == 200
    assert response.json() == {"name": "hyromy-api", "stars": 10}


@patch("apps.github.views.cache_handler.get_set")
def test_github_repo_view_error(mock, client):
    error_response = Response(404, request=Request("GET", "url"))
    mock.side_effect = HTTPStatusError(
        "Not found", request=error_response.request, response=error_response
    )

    response = client.get("/github/repos/repositorio-falso/")

    assert response.status_code == 404
    assert "error" in response.json()
