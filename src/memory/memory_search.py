"""
Memory Search and Retrieval System

This module provides optimized search and retrieval capabilities for both temporary 
and permanent memory systems, reducing token usage through efficient lookups.
"""

import time
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
import heapq
from datetime import datetime, timedelta
import numpy as np
from functools import lru_cache

class MemorySearchEngine:
    """
    Optimized search engine for memory systems with caching and hybrid search techniques.
    
    Features:
    - Multi-tier caching for frequent queries
    - Hybrid retrieval combining keyword and semantic approaches
    - Optimized query preprocessing
    - Analytics for measuring search efficiency
    """
    
    def __init__(self, cache_size: int = 100, cache_ttl: int = 3600):
        """
        Initialize the search engine.
        
        Args:
            cache_size: Maximum number of cached results to store
            cache_ttl: Time-to-live for cached results in seconds (default: 1 hour)
        """
        # Cache for storing search results
        self.result_cache: Dict[str, Tuple[List[Dict[str, Any]], datetime]] = {}
        self.cache_size = cache_size
        self.cache_ttl = timedelta(seconds=cache_ttl)
        
        # Analytics data
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_searches = 0
        self.search_times: List[float] = []
        
        # Search weights
        self.weights = {
            "exact_match": 1.0,
            "keyword_match": 0.6,
            "semantic_match": 0.8
        }
    
    @lru_cache(maxsize=128)
    def preprocess_query(self, query: str) -> Tuple[str, List[str]]:
        """
        Preprocess a query to optimize search effectiveness.
        
        Args:
            query: The raw search query
            
        Returns:
            Tuple of (normalized query, keyword list)
        """
        # Convert to lowercase
        normalized = query.lower().strip()
        
        # Extract keywords (simple implementation - could be enhanced)
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 
                     'at', 'to', 'for', 'with', 'by', 'about', 'like', 'and'}
        
        keywords = [word for word in normalized.split() if word not in stop_words]
        
        return normalized, keywords
    
    def search(self, 
               query: str, 
               memory_items: List[Dict[str, Any]], 
               semantic_search_fn: Optional[Callable] = None,
               top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search memory items using an optimized hybrid approach.
        
        Args:
            query: The search query
            memory_items: List of memory items to search
            semantic_search_fn: Optional function for semantic search
            top_k: Maximum number of results to return
            
        Returns:
            List of memory items sorted by relevance
        """
        # Increment total searches counter
        self.total_searches += 1
        
        # Check cache first
        cache_key = query.strip().lower()
        cached_result = self._check_cache(cache_key)
        if cached_result:
            self.cache_hits += 1
            return cached_result
        
        self.cache_misses += 1
        
        # Start timing the search
        start_time = time.time()
        
        # Preprocess query
        normalized_query, keywords = self.preprocess_query(query)
        
        # Search using different methods and combine results
        results = []
        
        # 1. First pass: Fast filtering with exact and keyword matches
        for item in memory_items:
            content = item.get('content', '').lower()
            relevance = 0.0
            
            # Exact match (highest priority)
            if normalized_query in content:
                position = content.find(normalized_query)
                length_ratio = len(normalized_query) / max(len(content), 1)
                # Earlier matches with better length coverage get higher scores
                exact_score = (1.0 - position / max(len(content), 1)) * 0.5 + length_ratio * 0.5
                relevance += exact_score * self.weights["exact_match"]
            
            # Keyword matches
            keyword_matches = 0
            for keyword in keywords:
                if keyword in content:
                    keyword_matches += 1
            
            if keywords:  # Avoid division by zero
                keyword_score = keyword_matches / len(keywords)
                relevance += keyword_score * self.weights["keyword_match"]
            
            # Store the initial score
            if relevance > 0:
                result = item.copy()
                result['relevance'] = relevance
                results.append(result)
        
        # 2. Second pass: If we have a semantic search function and not enough results
        if semantic_search_fn and (len(results) < top_k):
            semantic_results = semantic_search_fn(query, memory_items)
            
            # Add semantic results with their scores
            for semantic_item in semantic_results:
                # Check if this item is already in our results
                existing = next((r for r in results if r.get('id') == semantic_item.get('id')), None)
                
                if existing:
                    # Combine scores, giving preference to the higher score
                    semantic_score = semantic_item.get('relevance', 0) * self.weights["semantic_match"]
                    existing['relevance'] = max(existing['relevance'], semantic_score)
                else:
                    # Add new semantic result
                    semantic_item['relevance'] = semantic_item.get('relevance', 0.5) * self.weights["semantic_match"]
                    results.append(semantic_item)
        
        # Sort by relevance (highest first)
        results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        # Record search time
        end_time = time.time()
        search_time = end_time - start_time
        self.search_times.append(search_time)
        
        # Cache the results
        top_results = results[:top_k]
        self._cache_results(cache_key, top_results)
        
        return top_results
    
    def _check_cache(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """
        Check if results for this query are cached and still valid.
        
        Args:
            query: The search query
            
        Returns:
            Cached results if valid, None otherwise
        """
        if query in self.result_cache:
            results, timestamp = self.result_cache[query]
            
            # Check if cache entry is still valid
            if datetime.now() - timestamp < self.cache_ttl:
                return results
            
            # Cache expired, remove it
            del self.result_cache[query]
        
        return None
    
    def _cache_results(self, query: str, results: List[Dict[str, Any]]) -> None:
        """
        Cache search results for future use.
        
        Args:
            query: The search query
            results: The search results to cache
        """
        # If cache is full, remove the oldest entry
        if len(self.result_cache) >= self.cache_size:
            # Find the oldest entry
            oldest_query = None
            oldest_time = datetime.now()
            
            for q, (_, timestamp) in self.result_cache.items():
                if timestamp < oldest_time:
                    oldest_time = timestamp
                    oldest_query = q
            
            # Remove oldest entry
            if oldest_query:
                del self.result_cache[oldest_query]
        
        # Add new cache entry
        self.result_cache[query] = (results, datetime.now())
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Get search analytics data.
        
        Returns:
            Dictionary with analytics
        """
        avg_search_time = sum(self.search_times) / max(len(self.search_times), 1)
        cache_hit_rate = self.cache_hits / max(self.total_searches, 1)
        
        return {
            "total_searches": self.total_searches,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": cache_hit_rate,
            "cache_size": len(self.result_cache),
            "max_cache_size": self.cache_size,
            "avg_search_time_ms": avg_search_time * 1000,
            "searches_per_minute": len(self.search_times) / (sum(self.search_times) / 60) if self.search_times else 0
        }
    
    def clear_cache(self) -> None:
        """Clear the result cache."""
        self.result_cache.clear()
        
    def adjust_weights(self, weight_updates: Dict[str, float]) -> None:
        """
        Adjust the weights used for combining search methods.
        
        Args:
            weight_updates: Dictionary mapping weight names to new values
        """
        for name, value in weight_updates.items():
            if name in self.weights:
                self.weights[name] = value 