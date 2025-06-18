#!/usr/bin/env python3
"""
Caching layer for framework recommendations
"""

import json
import hashlib
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class FrameworkCache:
    """Simple in-memory cache for framework recommendations"""
    
    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds
        
    def _generate_key(self, context: Dict[str, Any]) -> str:
        """Generate a cache key from context"""
        # Sort keys for consistent hashing
        sorted_context = json.dumps(context, sort_keys=True)
        return hashlib.md5(sorted_context.encode()).hexdigest()
    
    def get(self, context: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Get cached recommendations if available and not expired"""
        key = self._generate_key(context)
        
        if key in self.cache:
            entry = self.cache[key]
            # Check if expired
            if time.time() - entry['timestamp'] < self.ttl_seconds:
                logger.info(f"Cache hit for key {key[:8]}...")
                return entry['data']
            else:
                # Remove expired entry
                del self.cache[key]
                logger.info(f"Cache expired for key {key[:8]}...")
        
        return None
    
    def set(self, context: Dict[str, Any], recommendations: List[Dict[str, Any]]):
        """Cache recommendations"""
        key = self._generate_key(context)
        self.cache[key] = {
            'data': recommendations,
            'timestamp': time.time(),
            'context': context
        }
        logger.info(f"Cached recommendations for key {key[:8]}...")
    
    def clear(self):
        """Clear all cached entries"""
        self.cache.clear()
        logger.info("Framework cache cleared")
    
    def cleanup_expired(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time - entry['timestamp'] >= self.ttl_seconds:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        active_entries = 0
        
        for entry in self.cache.values():
            if current_time - entry['timestamp'] < self.ttl_seconds:
                active_entries += 1
        
        return {
            'total_entries': len(self.cache),
            'active_entries': active_entries,
            'expired_entries': len(self.cache) - active_entries,
            'ttl_seconds': self.ttl_seconds
        }

# Global cache instance
framework_cache = FrameworkCache(ttl_seconds=3600)  # 1 hour TTL

# Decorator for caching
def cache_framework_recommendations(func):
    """Decorator to cache framework recommendations"""
    async def wrapper(*args, **kwargs):
        # Extract context from arguments
        if args and hasattr(args[0], 'dict'):
            context = args[0].dict()
        elif 'context' in kwargs:
            context = kwargs['context']
        else:
            # Try to build context from known parameters
            context = {
                'company_name': kwargs.get('company_name', ''),
                'industry': kwargs.get('industry', ''),
                'stage': kwargs.get('stage', ''),
                'challenges': kwargs.get('challenges', [])
            }
        
        # Check cache
        cached = framework_cache.get(context)
        if cached is not None:
            return cached
        
        # Call original function
        result = await func(*args, **kwargs)
        
        # Cache result
        if result:
            framework_cache.set(context, result)
        
        return result
    
    return wrapper

def cache_framework_analysis(func):
    """Decorator to cache framework analysis"""
    async def wrapper(*args, **kwargs):
        # Extract framework_id and context
        framework_id = kwargs.get('framework_id', args[0] if args else None)
        assessment_data = kwargs.get('assessment_data', args[1] if len(args) > 1 else {})
        
        cache_key = {
            'framework_id': framework_id,
            'company': assessment_data.get('company_name', ''),
            'industry': assessment_data.get('sector', assessment_data.get('industry', '')),
            'stage': assessment_data.get('funding_stage', '')
        }
        
        # Check cache with shorter TTL for analysis (30 minutes)
        cached = framework_cache.get(cache_key)
        if cached is not None:
            return cached
        
        # Call original function
        result = await func(*args, **kwargs)
        
        # Cache result
        if result:
            framework_cache.set(cache_key, result)
        
        return result
    
    return wrapper

# Usage example in api_framework_intelligent.py:
# @cache_framework_recommendations
# async def recommend_frameworks_dynamic(request: FrameworkRequest):
#     ...
#
# @cache_framework_analysis  
# async def analyze_with_framework(framework_id: str, assessment_data: Dict[str, Any]):
#     ...