import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Any, Callable, Optional


class AIResponseCache:
    """
    Lightweight cache for AI/LLM API responses.
    Stores responses in a local JSON file with optional TTL (time-to-live).
    """

    def __init__(self, cache_file: str = "cache.json", ttl: Optional[int] = None):
        """
        Initialize the cache.

        Args:
            cache_file (str): Path to the cache file (JSON).
            ttl (int, optional): Time-to-live in seconds. If None, entries never expire.
        """
        self.cache_file = cache_file
        self.ttl = ttl
        self._load_cache()

    def _load_cache(self):
        """Load cache from file, or initialize empty cache."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
            except json.JSONDecodeError:
                self.cache = {}
        else:
            self.cache = {}

    def _save_cache(self):
        """Persist cache to file."""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _make_key(self, prompt: str, **kwargs) -> str:
        """Generate a unique key based on prompt and extra parameters."""
        data = {"prompt": prompt, **kwargs}
        raw = json.dumps(data, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _is_expired(self, timestamp: str) -> bool:
        """Check if a cached entry has expired based on TTL."""
        if self.ttl is None:
            return False
        entry_time = datetime.fromisoformat(timestamp)
        return datetime.utcnow() - entry_time > timedelta(seconds=self.ttl)

    def get(self, prompt: str, **kwargs) -> Optional[Any]:
        """
        Retrieve cached response if available and not expired.

        Args:
            prompt (str): Prompt string.
            kwargs: Additional parameters for hashing.

        Returns:
            Cached response or None if not found/expired.
        """
        key = self._make_key(prompt, **kwargs)
        entry = self.cache.get(key)
        if entry:
            if self._is_expired(entry["timestamp"]):
                del self.cache[key]
                self._save_cache()
                return None
            return entry["response"]
        return None

    def set(self, prompt: str, response: Any, **kwargs):
        """
        Store a response in cache.

        Args:
            prompt (str): Prompt string.
            response (Any): API response to cache.
            kwargs: Additional parameters for hashing.
        """
        key = self._make_key(prompt, **kwargs)
        self.cache[key] = {
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._save_cache()

    def get_or_set(self, prompt: str, func: Callable[[], Any], **kwargs) -> Any:
        """
        Return cached response or compute and cache it using `func`.

        Args:
            prompt (str): Prompt string.
            func (Callable): Function to call if cache miss.
            kwargs: Additional parameters for hashing.

        Returns:
            Response (cached or freshly computed).
        """
        cached = self.get(prompt, **kwargs)
        if cached is not None:
            return cached
        response = func()
        self.set(prompt, response, **kwargs)
        return response
