from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPStatusError, Request, Response

from utils.caching import (
    Cache,
)
from utils.fetching import (
    fetch,
)


class TestFetching:
    @staticmethod
    @patch("utils.fetching.Client")
    def test_fetch_success(mock):
        mock_instance = mock.return_value.__enter__.return_value
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {"id": 1, "name": "Fake Repo"}
        mock_instance.get.return_value = mock_response

        result = fetch("get", "https://api.github.com", "/repos/user/repo")

        assert result == {"id": 1, "name": "Fake Repo"}
        mock_instance.get.assert_called_once_with("/repos/user/repo")

    @staticmethod
    @patch("utils.fetching.Client")
    def test_fetch_error(mock):
        mock_instance = mock.return_value.__enter__.return_value

        mock_response = Response(
            404, request=Request("GET", "https://api.github.com/404")
        )
        mock_instance.get.return_value = mock_response

        with pytest.raises(HTTPStatusError):
            fetch("get", "https://api.github.com", "/404")


class TestCaching:
    @staticmethod
    @patch("utils.caching.Redis")
    def test_cache_hit(mock):
        mock_redis = mock.return_value
        mock_redis.get.return_value = '{"foo": "bar"}'

        cache = Cache()
        mock_function = MagicMock()

        result = cache.get_set("test_key", mock_function)

        assert result == {"foo": "bar"}
        mock_function.assert_not_called()

    @staticmethod
    @patch("utils.caching.Redis")
    def test_cache_miss(mock):
        mock_redis = mock.return_value
        mock_redis.get.return_value = None

        cache = Cache()
        mock_function = MagicMock(return_value={"foo": "new_data"})

        result = cache.get_set("test_key", mock_function, 3600)

        assert result == {"foo": "new_data"}
        mock_function.assert_called_once()
        mock_redis.setex.assert_called_once_with(
            "test_key", 3600, '{"foo": "new_data"}'
        )
