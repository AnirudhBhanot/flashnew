"""
Redis caching layer for FLASH predictions
"""
import json
import hashlib
import logging
import os
from typing import Optional, Dict, Any, Union
from datetime import timedelta
import pickle

try:
    import redis
    from redis.exceptions import RedisError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("Redis not installed. Caching disabled.")

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis caching for predictions and model results"""
    
    def __init__(
        self,
        host: str = None,
        port: int = None,
        db: int = 0,
        password: str = None,
        default_ttl: int = 3600,  # 1 hour default
        key_prefix: str = "flash:"
    ):
        self.redis_client = None
        self.default_ttl = default_ttl
        self.key_prefix = key_prefix
        self.enabled = False
        
        if REDIS_AVAILABLE:
            # Get connection params from environment or use defaults
            self.host = host or os.getenv("REDIS_HOST", "localhost")
            self.port = port or int(os.getenv("REDIS_PORT", "6379"))
            self.db = db
            self.password = password or os.getenv("REDIS_PASSWORD")
            
            self._connect()
    
    def _connect(self):
        """Establish Redis connection"""
        try:
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=False,  # We'll handle encoding/decoding
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            self.redis_client.ping()
            self.enabled = True
            logger.info(f"Redis cache connected to {self.host}:{self.port}")
            
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Caching disabled.")
            self.enabled = False
            self.redis_client = None
    
    def _generate_key(self, data: Dict[str, Any], prefix: str = "prediction") -> str:
        """Generate a cache key from input data"""
        # Sort keys for consistent hashing
        sorted_data = json.dumps(data, sort_keys=True)
        hash_digest = hashlib.sha256(sorted_data.encode()).hexdigest()[:16]
        return f"{self.key_prefix}{prefix}:{hash_digest}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                # Try to deserialize
                try:
                    return pickle.loads(value)
                except:
                    # Fallback to JSON
                    return json.loads(value)
            return None
            
        except RedisError as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None,
        use_pickle: bool = True
    ) -> bool:
        """Set value in cache with TTL"""
        if not self.enabled or not self.redis_client:
            return False
        
        ttl = ttl or self.default_ttl
        
        try:
            # Serialize value
            if use_pickle:
                serialized = pickle.dumps(value)
            else:
                serialized = json.dumps(value)
            
            # Set with expiration
            self.redis_client.setex(key, ttl, serialized)
            return True
            
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except RedisError as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except RedisError as e:
            logger.error(f"Redis exists error: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching a pattern"""
        if not self.enabled or not self.redis_client:
            return 0
        
        try:
            # Use SCAN to avoid blocking
            deleted = 0
            for key in self.redis_client.scan_iter(match=f"{self.key_prefix}{pattern}*"):
                self.redis_client.delete(key)
                deleted += 1
            
            logger.info(f"Cleared {deleted} keys matching pattern: {pattern}")
            return deleted
            
        except RedisError as e:
            logger.error(f"Redis clear pattern error: {e}")
            return 0
    
    def get_prediction(self, features: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached prediction result"""
        key = self._generate_key(features, "prediction")
        return self.get(key)
    
    def set_prediction(
        self, 
        features: Dict[str, Any], 
        result: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """Cache prediction result"""
        key = self._generate_key(features, "prediction")
        # Use longer TTL for predictions (4 hours default)
        ttl = ttl or (4 * 3600)
        return self.set(key, result, ttl)
    
    def get_pattern_analysis(self, features: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached pattern analysis"""
        key = self._generate_key(features, "pattern")
        return self.get(key)
    
    def set_pattern_analysis(
        self,
        features: Dict[str, Any],
        patterns: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """Cache pattern analysis"""
        key = self._generate_key(features, "pattern")
        # Pattern analysis can be cached longer (8 hours)
        ttl = ttl or (8 * 3600)
        return self.set(key, patterns, ttl)
    
    def get_metrics_summary(self) -> Optional[Dict[str, Any]]:
        """Get cached metrics summary"""
        key = f"{self.key_prefix}metrics:summary"
        return self.get(key)
    
    def set_metrics_summary(
        self,
        metrics: Dict[str, Any],
        ttl: int = 60  # 1 minute for metrics
    ) -> bool:
        """Cache metrics summary"""
        key = f"{self.key_prefix}metrics:summary"
        return self.set(key, metrics, ttl, use_pickle=False)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.enabled or not self.redis_client:
            return {"enabled": False}
        
        try:
            info = self.redis_client.info()
            return {
                "enabled": True,
                "connected": True,
                "used_memory_mb": info.get("used_memory", 0) / (1024 * 1024),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": (
                    info.get("keyspace_hits", 0) / 
                    max(1, info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0))
                ) * 100
            }
        except Exception as e:
            logger.error(f"Failed to get Redis stats: {e}")
            return {"enabled": True, "connected": False, "error": str(e)}
    
    def invalidate_all_predictions(self) -> int:
        """Invalidate all cached predictions"""
        return self.clear_pattern("prediction:")
    
    def invalidate_all_patterns(self) -> int:
        """Invalidate all cached pattern analyses"""
        return self.clear_pattern("pattern:")


# Global cache instance
redis_cache = RedisCache()


# Decorator for caching function results
def cache_result(ttl: int = 3600, prefix: str = "func"):
    """Decorator to cache function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached = redis_cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            redis_cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test Redis cache
    print("Testing Redis cache...")
    
    cache = RedisCache()
    
    if cache.enabled:
        print("✅ Redis connected")
        
        # Test basic operations
        test_data = {"test": "data", "number": 42}
        
        # Set
        if cache.set("test:key", test_data, ttl=10):
            print("✅ Set operation successful")
        
        # Get
        retrieved = cache.get("test:key")
        if retrieved == test_data:
            print("✅ Get operation successful")
        
        # Prediction caching
        features = {
            "total_capital_raised_usd": 1000000,
            "team_size_full_time": 10,
            "funding_stage": "seed"
        }
        
        prediction_result = {
            "success_probability": 0.75,
            "verdict": "PASS",
            "confidence_score": 0.8
        }
        
        if cache.set_prediction(features, prediction_result):
            print("✅ Prediction caching successful")
        
        cached_prediction = cache.get_prediction(features)
        if cached_prediction == prediction_result:
            print("✅ Prediction retrieval successful")
        
        # Stats
        stats = cache.get_stats()
        print(f"\nCache stats: {json.dumps(stats, indent=2)}")
        
        # Cleanup
        cache.delete("test:key")
        cache.invalidate_all_predictions()
        
    else:
        print("❌ Redis not available - install with: pip install redis")