import json
import hashlib
import os
from datetime import datetime, timedelta

class AIResponseCache:
    def __init__(self, cache_file="cache.json", ttl=None):
        self.cache_file = cache_file
        self.ttl = ttl  # Time-to-live in seconds
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def _save_cache(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _make_key(self, prompt, **kwargs):
        data = {"prompt": prompt, **kwargs}
        raw = json.dumps(data, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, prompt, **kwargs):
        key = self._make_key(prompt, **kwargs)
        entry = self.cache.get(key)
        if entry:
            if self.ttl:
                timestamp = datetime.fromisoformat(entry["timestamp"])
                if datetime.utcnow() - timestamp > timedelta(seconds=self.ttl):
                    del self.cache[key]
                    self._save_cache()
                    return None
            return entry["response"]
        return None

    def set(self, prompt, response, **kwargs):
        key = self._make_key(prompt, **kwargs)
        self.cache[key] = {
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._save_cache()

    def get_or_set(self, prompt, func, **kwargs):
        cached = self.get(prompt, **kwargs)
        if cached is not None:
            return cached
        response = func()
        self.set(prompt, response, **kwargs)
        return response
