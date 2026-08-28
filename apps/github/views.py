from httpx import HTTPStatusError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from project.config import config
from utils.caching import cache_handler
from utils.fetching import fetch

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {config.GH_API_TOKEN}",
}
GITHUB_API = "https://api.github.com/"
DEV = config.GH_USERNAME


def _generic_exception(e: HTTPStatusError) -> Response:
    return Response(
        {
            "error": str(e),
        },
        status=e.response.status_code,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def repo(request: Request, repo_name: str) -> Response:
    try:
        return Response(
            cache_handler.get_set(
                f"repos:{repo_name}",
                lambda: fetch(
                    "get", GITHUB_API, f"/repos/{DEV}/{repo_name}", headers=HEADERS
                ),
            )
        )

    except HTTPStatusError as e:
        return _generic_exception(e)


@api_view(["GET"])
@permission_classes([AllowAny])
def repos(request: Request) -> Response:
    try:
        return Response(
            cache_handler.get_set(
                "repos",
                lambda: fetch("get", GITHUB_API, f"users/{DEV}/repos", headers=HEADERS),
            ),
        )

    except HTTPStatusError as e:
        return _generic_exception(e)
