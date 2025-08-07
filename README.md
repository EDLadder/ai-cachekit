# AI CacheKit

[![Tests](https://github.com/EDLadder/ai-cachekit/actions/workflows/python-tests.yml/badge.svg)](https://github.com/EDLadder/ai-cachekit/actions)
[![PyPI version](https://badge.fury.io/py/ai-cachekit.svg)](https://badge.fury.io/py/ai-cachekit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lightweight caching library for AI/LLM API responses.  
Reduce costs and improve performance by storing API responses locally with hash-based keys and optional TTL.

---

## Features
- 🔹 Simple API: `get`, `set`
- 🔹 Local JSON storage (no external DB required)
- 🔹 Optional TTL (time-to-live) for cache expiration
- 🔹 Perfect for OpenAI, Anthropic, Ollama, etc.

---

## Installation

**From GitHub (development version):**
```bash
pip install git+https://github.com/EDLadder/ai-cachekit.git
```

**From PyPI (after release):**
```bash
pip install ai-cachekit
```

---

## Usage

```python
from ai_cachekit import AIResponseCache

cache = AIResponseCache(backend="memory")
cache.set("question", "answer")
print(cache.get("question"))
```

### File-Based Cache (JSON)

```python
cache = AIResponseCache(backend="file", filepath="my_cache.json")
cache.set("key", "value")
print(cache.get("key"))
```

### Redis Cache

```python
cache = AIResponseCache(backend="redis", host="localhost", port=6379)
cache.set("key", "value")
print(cache.get("key"))
```

---

## Why?
- Avoid repeated API calls (save cost & time)
- Minimal dependencies and setup
- Flexible for any AI API (OpenAI, LLaMA, etc.)

---

## Development

Clone repo and install dev dependencies:
```bash
git clone https://github.com/EDLadder/ai-cachekit.git
cd ai-cachekit
pip install -r requirements.txt
pytest
```

---

## Plans
- [x] Support for Redis and SQLite backends.
- [ ] CLI tool for managing cache.
- [ ] Built-in stats: hit rate, saved cost estimation.
- [ ] Encryption for cached data.

---

## License
MIT License – free to use and modify.
