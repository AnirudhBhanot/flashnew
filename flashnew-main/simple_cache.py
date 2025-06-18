"""
Simple in-memory cache implementation as Redis alternative
"""
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class SimpleCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, default_ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        logger.info("Initialized in-memory cache")
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache if not expired"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry["expires_at"]:
                logger.debug(f"Cache hit for {key}")
                return entry["value"]
            else:
                # Remove expired entry
                del self.cache[key]
                logger.debug(f"Cache expired for {key}")
        return None
    
    def setex(self, key: str, ttl: int, value: str):
        """Set value with expiration time"""
        self.cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
            "created_at": time.time()
        }
        logger.debug(f"Cached {key} for {ttl} seconds")
        
        # Clean up old entries periodically
        self._cleanup_expired()
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self):
        """Clear entire cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def _cleanup_expired(self):
        """Remove expired entries (called periodically)"""
        # Only cleanup every 100 operations to avoid overhead
        if len(self.cache) % 100 == 0:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self.cache.items()
                if current_time >= entry["expires_at"]
            ]
            for key in expired_keys:
                del self.cache[key]
            if expired_keys:
                logger.debug(f"Cleaned up {len(expired_keys)} expired entries")
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        valid_entries = sum(
            1 for entry in self.cache.values()
            if current_time < entry["expires_at"]
        )
        
        return {
            "total_entries": len(self.cache),
            "valid_entries": valid_entries,
            "expired_entries": len(self.cache) - valid_entries,
            "memory_usage_bytes": sum(
                len(entry["value"]) for entry in self.cache.values()
            )
        }
    
    # Redis-compatible methods
    def ping(self) -> bool:
        """Redis compatibility - always returns True"""
        return True
    
    def close(self):
        """Redis compatibility - no-op for in-memory cache"""
        pass


# Global cache instance
simple_cache = SimpleCache()