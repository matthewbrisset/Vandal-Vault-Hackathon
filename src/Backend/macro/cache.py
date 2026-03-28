# src/Backend/macro/cache.py
from cachetools import TTLCache
from functools import wraps

# Cache up to 10 different API responses, each valid for 1 hour
_cache = TTLCache(maxsize=10, ttl=3600)

def ttl_cache(key: str):
    """Decorator that caches a function's return value by key for 1 hour."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key in _cache:
                print(f"[cache] Returning cached data for '{key}'")
                return _cache[key]
            result = func(*args, **kwargs)
            _cache[key] = result
            return result
        return wrapper
    return decorator
