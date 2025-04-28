from typing import Any, Optional
import time
from config import CACHE_TEMPO_EXPIRACAO

class Cache:
    _instance = None
    _cache: dict = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Cache, cls).__new__(cls)
        return cls._instance
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < CACHE_TEMPO_EXPIRACAO:
                return data
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        self._cache[key] = (value, time.time())
    
    def clear(self) -> None:
        self._cache.clear()
    
    def invalidate(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key] 