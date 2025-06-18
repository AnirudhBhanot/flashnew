#!/usr/bin/env python3
"""
Clear cache for DeepSeek API testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_cache import simple_cache

def clear_cache():
    """Clear all cached responses"""
    if hasattr(simple_cache, 'cache'):
        keys_to_remove = []
        for key in simple_cache.cache.keys():
            if key.startswith('llm:'):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del simple_cache.cache[key]
            print(f"Cleared cache key: {key}")
        
        print(f"\nTotal cache entries cleared: {len(keys_to_remove)}")
    else:
        print("No cache found")

if __name__ == "__main__":
    print("Clearing DeepSeek API cache...")
    clear_cache()
    print("Cache cleared successfully!")