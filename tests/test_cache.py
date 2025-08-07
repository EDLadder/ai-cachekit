import pytest
import socket
from ai_cachekit.cache import AIResponseCache

def is_redis_running(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False

@pytest.mark.parametrize("backend, kwargs", [
    ("memory", {}),
    ("file", {"filepath": "test_cache.json"}),
    pytest.param("redis", {"host": "localhost", "port": 6379}, 
                 marks=pytest.mark.skipif(
                     not is_redis_running("localhost", 6379),
                     reason="Redis not running on localhost:6379"))
])
def test_cache_backends(backend, kwargs):
    cache = AIResponseCache(backend=backend, **kwargs)
    cache.set("key", "value")
    assert cache.get("key") == "value"
