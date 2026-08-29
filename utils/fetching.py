from typing import Any, Literal

from httpx import Client, Response


def fetch(
    method: Literal["get", "post", "put", "patch", "delete"],
    base_url: str,
    endpoint: str,
    /,
    **kwargs,
) -> Any:
    """
    Request a source by http

    Args:
        method: HTTP method
        base_url: base url to fetch
        endpoint: endpoint to fetch

    Raise:
        HTTPStatusError

    Example:
    ```
    data = fetch(
        "get",
        "https://some-site.com",
        "/some/endpoint",
        headers={
            "Authorization": "Bearer TOKEN"
        }
    )
    ```

    """

    with Client(base_url=base_url) as client:
        response: Response = getattr(client, method)(endpoint, **kwargs)
        response.raise_for_status()

        return response.json()
