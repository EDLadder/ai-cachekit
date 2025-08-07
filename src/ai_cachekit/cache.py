from ai_cachekit.backends.memory_backend import MemoryBackend
from ai_cachekit.backends.file_backend import FileBackend
from ai_cachekit.backends.redis_backend import RedisBackend

class AIResponseCache:
    def __init__(self, backend="memory", **kwargs):
        if backend == "memory":
            self.backend = MemoryBackend()
        elif backend == "file":
            self.backend = FileBackend(**kwargs)
        elif backend == "redis":
            self.backend = RedisBackend(**kwargs)
        else:
            raise ValueError("Invalid backend")

    def get(self, key):
        return self.backend.get(key)

    def set(self, key, value):
        self.backend.set(key, value)
