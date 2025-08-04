import os
import pytest
from ai_cachekit.cache import AIResponseCache


@pytest.fixture
def cache_file(tmp_path):
    return tmp_path / "cache.json"


def test_set_and_get(cache_file):
    cache = AIResponseCache(cache_file=str(cache_file))
    prompt = "Hello AI"
    response = "Hello back!"

    cache.set(prompt, response)
    assert cache.get(prompt) == response


def test_get_returns_none_if_not_found(cache_file):
    cache = AIResponseCache(cache_file=str(cache_file))
    assert cache.get("Unknown prompt") is None


def test_get_or_set(cache_file):
    cache = AIResponseCache(cache_file=str(cache_file))
    prompt = "What's 2+2?"

    result = cache.get_or_set(prompt, lambda: "4")
    assert result == "4"
    # Second call should use cache, not recompute
    result2 = cache.get_or_set(prompt, lambda: "WRONG")
    assert result2 == "4"


def test_ttl_expiration(cache_file):
    cache = AIResponseCache(cache_file=str(cache_file), ttl=0)
    prompt = "Will expire"
    response = "test"

    cache.set(prompt, response)
    # Simulate expiration by setting ttl=0
    assert cache.get(prompt) is None
