import json, os

class FileBackend:
    def __init__(self, filepath="cache.json"):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump({}, f)

    def _load(self):
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f)

    def get(self, key):
        return self._load().get(key)

    def set(self, key, value):
        data = self._load()
        data[key] = value
        self._save(data)
