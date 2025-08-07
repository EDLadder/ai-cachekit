import pytest
from ai_cachekit.cache import AIResponseCache

@pytest.mark.parametrize("backend, kwargs", [
    ("memory", {}),
    ("file", {"filepath": "test_cache.json"}),
    ("redis", {"host": "localhost", "port": 6379})
])
def test_cache_backends(backend, kwargs):
    cache = AIResponseCache(backend=backend, **kwargs)
    cache.set("key", "value")
    assert cache.get("key") == "value"
