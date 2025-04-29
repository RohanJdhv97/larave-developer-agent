"""
Optimized Memory System Integration

This module integrates all memory optimization components (search, relevance scoring,
and compression) to provide a unified interface for token-efficient memory operations.
"""

from typing import Dict, List, Any, Optional, Tuple, Union, Callable
import os
import json
from datetime import datetime
import time

from src.memory.dual_memory import DualMemorySystem
from src.memory.memory_search import MemorySearchEngine
from src.memory.relevance_scoring import RelevanceScorer
from src.memory.memory_compression import MemoryCompressor
from src.memory.memory_visualization import MemoryVisualization


class OptimizedMemorySystem:
    """
    A cost-optimized memory system that integrates search, relevance scoring, and compression.
    
    Features:
    - Efficient memory storage through automatic compression
    - Intelligent search with caching for frequent queries
    - Relevance-based item prioritization
    - Usage analytics and cost tracking
    - Memory operation visualization and transparency
    """
    
    def __init__(
        self,
        dual_memory: Optional[DualMemorySystem] = None,
        search_engine: Optional[MemorySearchEngine] = None,
        relevance_scorer: Optional[RelevanceScorer] = None,
        memory_compressor: Optional[MemoryCompressor] = None,
        memory_visualizer: Optional[MemoryVisualization] = None,
        auto_compress: bool = True,
        compression_threshold: int = 1000,  # Characters threshold for compression
        enable_analytics: bool = True,
        enable_visualization: bool = True
    ):
        """
        Initialize the optimized memory system.
        
        Args:
            dual_memory: Optional existing DualMemorySystem
            search_engine: Optional existing MemorySearchEngine
            relevance_scorer: Optional existing RelevanceScorer
            memory_compressor: Optional existing MemoryCompressor
            memory_visualizer: Optional existing MemoryVisualization
            auto_compress: Whether to automatically compress large memory items
            compression_threshold: Character count threshold for auto-compression
            enable_analytics: Whether to track analytics data
            enable_visualization: Whether to enable memory operation visualization
        """
        # Initialize component systems
        self.dual_memory = dual_memory or DualMemorySystem()
        self.search_engine = search_engine or MemorySearchEngine()
        self.relevance_scorer = relevance_scorer or RelevanceScorer()
        self.memory_compressor = memory_compressor or MemoryCompressor()
        self.memory_visualizer = memory_visualizer or MemoryVisualization() if enable_visualization else None
        
        # Configuration
        self.auto_compress = auto_compress
        self.compression_threshold = compression_threshold
        self.enable_analytics = enable_analytics
        self.enable_visualization = enable_visualization
        
        # Analytics data
        self.token_usage = {
            "searches": 0,
            "compressions": 0,
            "retrievals": 0,
            "estimated_tokens_saved": 0
        }
        
        # Token estimation factors
        self.chars_per_token = 4  # Approximate character-to-token ratio
        
        # Usage tracking
        self.operation_times = {
            "search": [],
            "retrieval": [],
            "compression": [],
            "add_message": [],
            "store_knowledge": []
        }
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """
        Add a message to temporary memory with optimization.
        
        Args:
            message: The message to add
        """
        start_time = time.time()
        
        # Start visualization tracking if enabled
        if self.enable_visualization and self.memory_visualizer:
            operation_id = self.memory_visualizer.start_operation(
                "add_message", 
                query=f"Adding message {message.get('id', 'unknown')}"
            )
            
            # Log the message content size
            if 'content' in message:
                self.memory_visualizer.log_analysis_step(
                    "content_analysis",
                    {"content_length": len(message['content']), "role": message.get('role', 'unknown')}
                )
        
        # Add message to dual memory
        self.dual_memory.add_message(message)
        
        # Apply compression if configured and message is large
        if self.auto_compress and 'content' in message:
            content = message.get('content', '')
            if len(content) > self.compression_threshold:
                # Note: We don't actually compress messages in temporary memory
                # since they need to be fully available for analysis
                # Instead, we'll track potential savings
                estimated_tokens = len(content) / self.chars_per_token
                self.token_usage["estimated_tokens_saved"] += estimated_tokens * 0.3  # Assume 30% savings
                
                # Log compression analysis if visualization is enabled
                if self.enable_visualization and self.memory_visualizer:
                    self.memory_visualizer.log_analysis_step(
                        "compression_analysis",
                        {
                            "original_size": len(content),
                            "estimated_compressed_size": int(len(content) * 0.7),
                            "estimated_tokens_saved": int(estimated_tokens * 0.3)
                        }
                    )
                
        # Track execution time
        if self.enable_analytics:
            self.operation_times["add_message"].append(time.time() - start_time)
            
        # End visualization tracking if enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.end_operation(
                summary=f"Added message {message.get('id', 'unknown')} to temporary memory"
            )
    
    def search_memory(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search across memory with optimization.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with relevance scores
        """
        start_time = time.time()
        
        # Start visualization tracking if enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.start_operation("search", query=query)
            self.memory_visualizer.log_analysis_step(
                "search_parameters",
                {"max_results": max_results, "query_length": len(query)}
            )
        
        # Use the search engine to find potential matches from both memory types
        # Get temporary memory items
        temp_items = self.dual_memory.temporary_memory.get_messages()
        
        # Get permanent memory items
        perm_items = self.dual_memory.permanent_memory.get_all_knowledge()
        
        # Log memory access if visualization is enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.log_analysis_step(
                "memory_access",
                {
                    "temporary_items_count": len(temp_items),
                    "permanent_items_count": len(perm_items),
                    "total_items": len(temp_items) + len(perm_items)
                }
            )
        
        # Combined items (with source field added)
        combined_items = []
        for item in temp_items:
            item_copy = item.copy()
            item_copy['source'] = 'temporary'
            combined_items.append(item_copy)
            
            # Log item access if visualization is enabled
            if self.enable_visualization and self.memory_visualizer and 'id' in item:
                self.memory_visualizer.log_memory_access(
                    item_id=item['id'],
                    item_type="temporary",
                    reason="Included in search scope"
                )
            
        for item in perm_items:
            item_copy = item.copy()
            item_copy['source'] = 'permanent'
            combined_items.append(item_copy)
            
            # Log item access if visualization is enabled
            if self.enable_visualization and self.memory_visualizer and 'id' in item:
                self.memory_visualizer.log_memory_access(
                    item_id=item['id'],
                    item_type="permanent",
                    reason="Included in search scope"
                )
        
        # Search using the optimized search engine
        search_results = self.search_engine.search(
            query=query,
            memory_items=combined_items,
            top_k=max_results * 2  # Get more results than needed for scoring
        )
        
        # Log search engine results if visualization is enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.log_analysis_step(
                "initial_search",
                {
                    "results_count": len(search_results),
                    "search_method": "hybrid",
                    "cache_hit": self.search_engine.cache_hits > 0
                }
            )
        
        # Apply relevance scoring
        scored_results = []
        for item in search_results:
            # Pre-calculated semantic relevance from search
            semantic_sim = item.get('relevance', 0.0)
            
            # Apply comprehensive scoring
            score = self.relevance_scorer.score_item(
                item=item,
                query=query,
                semantic_similarity=semantic_sim
            )
            
            # Add the final score
            item['final_score'] = score
            item['confidence'] = self.relevance_scorer.get_confidence_level(score)
            
            scored_results.append(item)
            
            # Log detailed scoring if visualization is enabled
            if self.enable_visualization and self.memory_visualizer and 'id' in item:
                self.memory_visualizer.log_analysis_step(
                    "relevance_scoring",
                    {
                        "item_id": item.get('id', 'unknown'),
                        "semantic_similarity": semantic_sim,
                        "final_score": score,
                        "confidence": item['confidence'],
                        "score_details": item.get('_score_details', {})
                    }
                )
        
        # Sort by final score
        scored_results.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        
        # Take top results
        top_results = scored_results[:max_results]
        
        # Log final results if visualization is enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.log_search_results(top_results)
        
        # Update analytics
        if self.enable_analytics:
            self.token_usage["searches"] += 1
            self.operation_times["search"].append(time.time() - start_time)
            
            # Estimate token savings
            query_len = len(query)
            results_len = sum(len(json.dumps(r)) for r in top_results)
            naive_search_len = query_len + len(json.dumps(combined_items))
            optimized_search_len = query_len + results_len
            
            tokens_saved = (naive_search_len - optimized_search_len) / self.chars_per_token
            self.token_usage["estimated_tokens_saved"] += max(0, tokens_saved)
            
            # Log token savings if visualization is enabled
            if self.enable_visualization and self.memory_visualizer:
                self.memory_visualizer.log_analysis_step(
                    "token_optimization",
                    {
                        "naive_search_len": naive_search_len,
                        "optimized_search_len": optimized_search_len,
                        "estimated_tokens_saved": max(0, int(tokens_saved))
                    }
                )
        
        # End visualization tracking
        if self.enable_visualization and self.memory_visualizer:
            summary = f"Found {len(top_results)} relevant results for query: {query}"
            self.memory_visualizer.end_operation(summary=summary)
            
        return top_results
    
    def store_knowledge(self, knowledge_entries: List[Dict[str, Any]]) -> None:
        """
        Store knowledge in permanent memory with optimization.
        
        Args:
            knowledge_entries: List of knowledge entries to store
        """
        start_time = time.time()
        
        # Start visualization tracking if enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.start_operation(
                "store_knowledge", 
                query=f"Storing {len(knowledge_entries)} knowledge entries"
            )
        
        # Apply compression if configured
        compressed_entries = []
        for entry in knowledge_entries:
            # Check if entry is large enough to compress
            content = entry.get('content', '')
            if self.auto_compress and len(content) > self.compression_threshold:
                # Log compression start if visualization is enabled
                if self.enable_visualization and self.memory_visualizer:
                    self.memory_visualizer.log_analysis_step(
                        "compression_start",
                        {
                            "item_id": entry.get('id', 'unknown'),
                            "original_size": len(content),
                            "compression_threshold": self.compression_threshold
                        }
                    )
                
                # Compress the entry
                compressed_entry = self.memory_compressor.compress_item(entry)
                compressed_entries.append(compressed_entry)
                
                # Track compression analytics
                if self.enable_analytics:
                    self.token_usage["compressions"] += 1
                    # Estimate token savings
                    original_size = len(content)
                    compressed_size = len(compressed_entry.get('content', ''))
                    tokens_saved = (original_size - compressed_size) / self.chars_per_token
                    self.token_usage["estimated_tokens_saved"] += tokens_saved
                
                # Log compression results if visualization is enabled
                if self.enable_visualization and self.memory_visualizer:
                    compression_ratio = compressed_entry.get('compression', {}).get('compression_ratio', 1.0)
                    self.memory_visualizer.log_analysis_step(
                        "compression_complete",
                        {
                            "item_id": compressed_entry.get('id', 'unknown'),
                            "original_size": original_size,
                            "compressed_size": compressed_size,
                            "compression_ratio": compression_ratio,
                            "tokens_saved": int(tokens_saved)
                        }
                    )
            else:
                # No compression needed
                compressed_entries.append(entry)
                
                # Log skipped compression if visualization is enabled
                if self.enable_visualization and self.memory_visualizer:
                    self.memory_visualizer.log_analysis_step(
                        "compression_skipped",
                        {
                            "item_id": entry.get('id', 'unknown'),
                            "content_size": len(content),
                            "reason": "Below threshold" if len(content) <= self.compression_threshold else "Unknown"
                        }
                    )
        
        # Store in permanent memory directly using the permanent_memory object
        # instead of going through dual_memory to avoid method name mismatch
        for entry in compressed_entries:
            self.dual_memory.permanent_memory.add_knowledge(entry)
            
            # Log storage if visualization is enabled
            if self.enable_visualization and self.memory_visualizer:
                self.memory_visualizer.log_memory_access(
                    item_id=entry.get('id', 'unknown'),
                    item_type="permanent",
                    reason="Stored in permanent memory"
                )
        
        # Track execution time
        if self.enable_analytics:
            self.operation_times["store_knowledge"].append(time.time() - start_time)
            
        # End visualization tracking
        if self.enable_visualization and self.memory_visualizer:
            summary = f"Stored {len(knowledge_entries)} knowledge entries in permanent memory"
            self.memory_visualizer.end_operation(summary=summary)
    
    def retrieve_item(self, item_id: str, decompress: bool = True) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific item from memory, decompressing if needed.
        
        Args:
            item_id: ID of the item to retrieve
            decompress: Whether to decompress compressed items
            
        Returns:
            The memory item, or None if not found
        """
        start_time = time.time()
        
        # Start visualization tracking if enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.start_operation(
                "retrieve_item", 
                query=f"Retrieving item {item_id}"
            )
        
        # Try temporary memory first
        item = self.dual_memory.temporary_memory.get_message_by_id(item_id)
        
        # Log memory access if found in temporary memory
        if item and self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.log_memory_access(
                item_id=item_id,
                item_type="temporary",
                reason="Direct retrieval by ID"
            )
        
        # If not found, try permanent memory
        if not item:
            item = self.dual_memory.permanent_memory.get_knowledge_by_id(item_id)
            
            # Log memory access if found in permanent memory
            if item and self.enable_visualization and self.memory_visualizer:
                self.memory_visualizer.log_memory_access(
                    item_id=item_id,
                    item_type="permanent",
                    reason="Direct retrieval by ID"
                )
        
        # If item found and decompression requested
        if item and decompress and 'compression' in item:
            # Log decompression start if visualization is enabled
            if self.enable_visualization and self.memory_visualizer:
                self.memory_visualizer.log_analysis_step(
                    "decompression_start",
                    {
                        "item_id": item_id,
                        "compressed_size": len(item.get('content', '')),
                        "compression_info": item.get('compression', {})
                    }
                )
            
            # Decompress the item
            item = self.memory_compressor.decompress_item(item)
            
            # Track decompression
            if self.enable_analytics:
                self.token_usage["retrievals"] += 1
                
            # Log decompression complete if visualization is enabled
            if self.enable_visualization and self.memory_visualizer:
                self.memory_visualizer.log_analysis_step(
                    "decompression_complete",
                    {
                        "item_id": item_id,
                        "decompressed_size": len(item.get('content', '')),
                        "original_restored": True
                    }
                )
        
        # Log retrieval result
        if self.enable_visualization and self.memory_visualizer:
            if item:
                result_message = f"Successfully retrieved item {item_id}"
            else:
                result_message = f"Failed to retrieve item {item_id} - not found"
                
            self.memory_visualizer.end_operation(summary=result_message)
        
        # Track execution time
        if self.enable_analytics and item:
            self.operation_times["retrieval"].append(time.time() - start_time)
            
        return item
    
    def analyze_and_extract_knowledge(self) -> List[Dict[str, Any]]:
        """
        Analyze temporary memory and extract knowledge for permanent storage.
        
        Returns:
            List of extracted knowledge entries
        """
        # Start visualization tracking if enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.start_operation(
                "extract_knowledge", 
                query="Analyzing temporary memory to extract knowledge"
            )
        
        # Use the dual memory's built-in analysis
        knowledge_entries = self.dual_memory.analyze_temporary_memory()
        
        # Log initial extraction if visualization is enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.log_analysis_step(
                "initial_extraction",
                {"extracted_entries": len(knowledge_entries)}
            )
        
        # Apply relevance scoring to determine which entries are worth keeping
        scored_entries = []
        for entry in knowledge_entries:
            # Score based on content quality (not query-based)
            # Use a generic "extract_knowledge" query to guide scoring
            score = self.relevance_scorer.score_item(
                item=entry,
                query="extract valuable knowledge",
                context={"weights": {
                    "semantic_similarity": 0.1,  # Less important for extraction
                    "recency": 0.2,              # Recent knowledge is more valuable
                    "usage_count": 0.1,          # Not yet used
                    "success_rate": 0.1,         # Not yet applied
                    "complexity_match": 0.5      # Focus on information density
                }}
            )
            
            # Add the score
            entry['knowledge_value'] = score
            
            # Log individual scoring if visualization is enabled
            if self.enable_visualization and self.memory_visualizer:
                self.memory_visualizer.log_analysis_step(
                    "knowledge_scoring",
                    {
                        "item_id": entry.get('id', 'unknown'),
                        "knowledge_value": score,
                        "content_preview": entry.get('content', '')[:100] + "..." if len(entry.get('content', '')) > 100 else entry.get('content', '')
                    }
                )
            
            # Only keep entries with sufficient value
            if score > 0.4:  # Threshold for knowledge extraction
                scored_entries.append(entry)
        
        # Sort by knowledge value
        scored_entries.sort(key=lambda x: x.get('knowledge_value', 0), reverse=True)
        
        # Log final results if visualization is enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.log_analysis_step(
                "knowledge_filtering",
                {
                    "initial_count": len(knowledge_entries),
                    "filtered_count": len(scored_entries),
                    "threshold": 0.4,
                    "rejected_count": len(knowledge_entries) - len(scored_entries)
                }
            )
            
            summary = f"Extracted {len(scored_entries)} valuable knowledge entries from temporary memory"
            self.memory_visualizer.end_operation(summary=summary)
        
        return scored_entries
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """
        Get optimization statistics and analytics.
        
        Returns:
            Dictionary with optimization statistics
        """
        # Get compression stats
        compression_stats = self.memory_compressor.get_compression_stats()
        
        # Calculate average operation times
        avg_times = {}
        for op, times in self.operation_times.items():
            if times:
                avg_times[f"avg_{op}_time_ms"] = sum(times) / len(times) * 1000
            else:
                avg_times[f"avg_{op}_time_ms"] = 0
        
        # Combine all stats
        stats = {
            "token_usage": self.token_usage,
            "compression": compression_stats,
            "performance": avg_times,
            "search_engine": {
                "cache_hit_rate": self.search_engine.cache_hits / max(self.search_engine.total_searches, 1),
                "total_searches": self.search_engine.total_searches
            }
        }
        
        return stats
    
    def get_recent_memory_operations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent memory operations for visualization.
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of recent memory operations
        """
        if not self.enable_visualization or not self.memory_visualizer:
            return []
            
        return self.memory_visualizer.get_operation_history(limit=limit)
    
    def get_memory_operation_report(self, operation_id: Optional[int] = None) -> str:
        """
        Get a detailed report for a specific memory operation.
        
        Args:
            operation_id: ID of the operation to report, or None for most recent
            
        Returns:
            Formatted report text
        """
        if not self.enable_visualization or not self.memory_visualizer:
            return "Memory visualization is not enabled."
            
        return self.memory_visualizer.generate_operation_report(operation_id)
    
    def set_auto_compression(self, enabled: bool, threshold: Optional[int] = None) -> None:
        """
        Configure automatic compression settings.
        
        Args:
            enabled: Whether to enable auto-compression
            threshold: Optional new character threshold for compression
        """
        self.auto_compress = enabled
        if threshold is not None:
            self.compression_threshold = threshold
            
    def clear_search_cache(self) -> None:
        """Clear the search engine's result cache."""
        self.search_engine.clear_cache()
        
    def optimize_all_permanent_memory(self) -> Dict[str, Any]:
        """
        Apply optimization to all items in permanent memory.
        
        Returns:
            Statistics about the optimization process
        """
        start_time = time.time()
        
        # Start visualization tracking if enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.start_operation(
                "optimize_all", 
                query="Optimizing all permanent memory"
            )
        
        # Get all knowledge entries
        entries = self.dual_memory.permanent_memory.get_all_knowledge()
        
        # Log initial state if visualization is enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.log_analysis_step(
                "optimization_start",
                {
                    "total_entries": len(entries),
                    "compression_threshold": self.compression_threshold
                }
            )
        
        # Track stats
        total_entries = len(entries)
        compressed_entries = 0
        original_size = 0
        compressed_size = 0
        
        # Process each entry
        for entry in entries:
            # Skip already compressed entries
            if 'compression' in entry:
                continue
                
            # Check if entry is large enough to compress
            content = entry.get('content', '')
            original_size += len(content)
            
            if len(content) > self.compression_threshold:
                # Log compression start if visualization is enabled
                if self.enable_visualization and self.memory_visualizer:
                    self.memory_visualizer.log_analysis_step(
                        "compressing_entry",
                        {
                            "item_id": entry.get('id', 'unknown'),
                            "content_size": len(content)
                        }
                    )
                
                # Compress the entry
                compressed = self.memory_compressor.compress_item(entry)
                compressed_size += len(compressed.get('content', ''))
                compressed_entries += 1
                
                # Update the entry in permanent memory
                self.dual_memory.permanent_memory.delete_entry(entry.get('id'))
                self.dual_memory.permanent_memory.add_knowledge(compressed)
                
                # Log compression results if visualization is enabled
                if self.enable_visualization and self.memory_visualizer:
                    compression_ratio = compressed.get('compression', {}).get('compression_ratio', 1.0)
                    self.memory_visualizer.log_analysis_step(
                        "entry_compressed",
                        {
                            "item_id": entry.get('id', 'unknown'),
                            "original_size": len(content),
                            "compressed_size": len(compressed.get('content', '')),
                            "compression_ratio": compression_ratio
                        }
                    )
            else:
                compressed_size += len(content)
        
        # Calculate savings
        elapsed_time = time.time() - start_time
        tokens_saved = (original_size - compressed_size) / self.chars_per_token
        
        # Update global stats
        if self.enable_analytics:
            self.token_usage["compressions"] += compressed_entries
            self.token_usage["estimated_tokens_saved"] += tokens_saved
            
        # Log final results if visualization is enabled
        if self.enable_visualization and self.memory_visualizer:
            self.memory_visualizer.log_analysis_step(
                "optimization_complete",
                {
                    "total_entries": total_entries,
                    "compressed_entries": compressed_entries,
                    "original_size": original_size,
                    "compressed_size": compressed_size,
                    "compression_ratio": compressed_size / original_size if original_size > 0 else 1.0,
                    "tokens_saved": int(tokens_saved),
                    "elapsed_time": elapsed_time
                }
            )
            
            summary = f"Optimized permanent memory: compressed {compressed_entries} entries, saved {int(tokens_saved)} tokens"
            self.memory_visualizer.end_operation(summary=summary)
        
        return {
            "total_entries": total_entries,
            "compressed_entries": compressed_entries,
            "original_size_chars": original_size,
            "compressed_size_chars": compressed_size,
            "chars_saved": original_size - compressed_size,
            "estimated_tokens_saved": tokens_saved,
            "compression_ratio": compressed_size / original_size if original_size > 0 else 1.0,
            "elapsed_time_seconds": elapsed_time
        }
    
    def save_memory_state(self, file_path: str) -> bool:
        """
        Save the optimized memory state to disk.
        
        Args:
            file_path: Path to save the memory state
            
        Returns:
            True if successful, False otherwise
        """
        # Save using dual memory's built-in save function
        return self.dual_memory.save_memory(file_path)
    
    def load_memory_state(self, file_path: str) -> bool:
        """
        Load the optimized memory state from disk.
        
        Args:
            file_path: Path to load the memory state from
            
        Returns:
            True if successful, False otherwise
        """
        # Load using dual memory's built-in load function
        return self.dual_memory.load_memory(file_path) 