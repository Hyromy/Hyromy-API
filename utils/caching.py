import json
from collections.abc import Callable
from typing import Any

from redis import Redis


class Cache:
    def __init__(self, **kwargs):
        kwargs.setdefault("decode_responses", True)
        self.client = Redis(**kwargs)

    def get_set(
        self,
        key: str,
        function: Callable[[], Any] | None = None,
        ttl: int = 3600,
        /,
    ) -> Any | None:
        """Get a value from cache. If isnt set, execute the function and save the result"""

        if cached_value := self.client.get(key):
            try:
                return json.loads(cached_value)

            except json.JSONDecodeError:
                return cached_value

        if function is not None:
            value = function()

            serialized_value = (
                json.dumps(value) if isinstance(value, (dict, list)) else str(value)
            )

            self.client.setex(key, ttl, serialized_value)

            return value

        return None


cache_handler = Cache()
