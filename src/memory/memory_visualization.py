"""
Memory Visualization and Transparency

This module provides tools to visualize and track how the agent accesses and analyzes
memory, making the internal memory operations transparent to users.
"""

from typing import Dict, List, Any, Optional, Tuple, Union, Callable
import json
import time
from datetime import datetime
import os
import threading

class MemoryVisualization:
    """
    A component for tracking and visualizing memory operations.
    
    This class provides functionality to:
    1. Log and track memory operations (search, retrieval, compression)
    2. Store operation details for later analysis
    3. Generate reports and statistics on memory usage
    4. Support the memory dashboard UI
    """
    
    def __init__(self, enable_logging: bool = True, max_operations: int = 1000):
        """
        Initialize the memory visualization system.
        
        Args:
            enable_logging: Whether to enable operation logging
            max_operations: Maximum number of operations to store in history
        """
        self.enable_logging = enable_logging
        self.max_operations = max_operations
        self.operations = []
        self.operation_counter = 0
        self.lock = threading.Lock()
        
        # Performance tracking
        self.performance_stats = {
            "search_times_ms": [],
            "retrieval_times_ms": [],
            "compression_times_ms": [],
        }
        
        # Usage statistics
        self.usage_stats = {
            "search_count": 0,
            "retrieval_count": 0,
            "compression_count": 0,
            "token_count": 0,
            "compressed_token_count": 0,
        }
        
        # Create log directory if it doesn't exist and logging is enabled
        if self.enable_logging:
            os.makedirs("logs", exist_ok=True)
            
        # Initialize session
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def log_operation(self, 
                     operation_type: str, 
                     query: Optional[str] = None,
                     params: Optional[Dict[str, Any]] = None,
                     results: Optional[Any] = None,
                     duration_ms: Optional[float] = None,
                     summary: Optional[str] = None) -> int:
        """
        Log a memory operation with details.
        
        Args:
            operation_type: Type of operation (search, retrieval, compression, etc.)
            query: The query or key used for the operation
            params: Parameters used for the operation
            results: Results of the operation
            duration_ms: Duration of the operation in milliseconds
            summary: Short summary of the operation
            
        Returns:
            Operation ID
        """
        if not self.enable_logging:
            return -1
            
        with self.lock:
            self.operation_counter += 1
            operation_id = self.operation_counter
            
            # Create operation record
            operation = {
                "operation_id": operation_id,
                "operation_type": operation_type,
                "timestamp": time.time(),
                "query": query or "",
                "params": params or {},
                "summary": summary or "",
                "duration_ms": duration_ms
            }
            
            # Store a copy of results if provided (might be large)
            if results is not None:
                # Store a simplified version or summary of results to avoid storing too much data
                if operation_type == "search":
                    # For search results, store count and top items
                    if isinstance(results, list):
                        result_summary = {
                            "count": len(results),
                            "top_items": results[:3] if len(results) > 0 else []
                        }
                    else:
                        result_summary = {"data": str(results)[:200]}
                    operation["results"] = result_summary
                elif operation_type == "compression":
                    # For compression, store before/after sizes
                    if isinstance(results, dict) and "original" in results and "compressed" in results:
                        operation["results"] = {
                            "original_size": len(str(results["original"])),
                            "compressed_size": len(str(results["compressed"])),
                            "compression_ratio": len(str(results["compressed"])) / max(1, len(str(results["original"])))
                        }
                    else:
                        operation["results"] = {"data": str(results)[:200]}
                else:
                    # For other operations, store a string preview
                    operation["results"] = {"data": str(results)[:200]}
            
            # Add to operations list, maintain max size
            self.operations.append(operation)
            if len(self.operations) > self.max_operations:
                self.operations = self.operations[-self.max_operations:]
                
            # Update statistics
            self._update_stats(operation_type, duration_ms)
                
            return operation_id
            
    def _update_stats(self, operation_type: str, duration_ms: Optional[float] = None):
        """Update performance statistics based on operation type."""
        if operation_type == "search":
            self.usage_stats["search_count"] += 1
            if duration_ms is not None:
                self.performance_stats["search_times_ms"].append(duration_ms)
                # Keep only last 100 measurements
                if len(self.performance_stats["search_times_ms"]) > 100:
                    self.performance_stats["search_times_ms"] = self.performance_stats["search_times_ms"][-100:]
        elif operation_type == "retrieval":
            self.usage_stats["retrieval_count"] += 1
            if duration_ms is not None:
                self.performance_stats["retrieval_times_ms"].append(duration_ms)
                if len(self.performance_stats["retrieval_times_ms"]) > 100:
                    self.performance_stats["retrieval_times_ms"] = self.performance_stats["retrieval_times_ms"][-100:]
        elif operation_type == "compression":
            self.usage_stats["compression_count"] += 1
            if duration_ms is not None:
                self.performance_stats["compression_times_ms"].append(duration_ms)
                if len(self.performance_stats["compression_times_ms"]) > 100:
                    self.performance_stats["compression_times_ms"] = self.performance_stats["compression_times_ms"][-100:]
    
    def get_recent_operations(self, limit: int = 10, operation_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recent memory operations, optionally filtered by type.
        
        Args:
            limit: Maximum number of operations to return
            operation_type: Optional filter for operation type
            
        Returns:
            List of recent operations
        """
        with self.lock:
            if operation_type:
                filtered_ops = [op for op in self.operations if op["operation_type"] == operation_type]
            else:
                filtered_ops = self.operations.copy()
                
            # Return the most recent operations first
            return sorted(filtered_ops, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_operation_details(self, operation_id: int) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific operation by ID.
        
        Args:
            operation_id: ID of the operation to retrieve
            
        Returns:
            Operation details or None if not found
        """
        with self.lock:
            for op in self.operations:
                if op["operation_id"] == operation_id:
                    return op.copy()
            return None
    
    def get_operation_report(self, operation_id: int) -> str:
        """
        Generate a human-readable report for a specific operation.
        
        Args:
            operation_id: ID of the operation to report on
            
        Returns:
            Formatted report string
        """
        operation = self.get_operation_details(operation_id)
        if not operation:
            return f"Operation {operation_id} not found"
            
        # Build the report text
        report = f"Operation #{operation['operation_id']}: {operation['operation_type'].upper()}\n"
        report += f"Timestamp: {datetime.fromtimestamp(operation['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if operation.get("duration_ms"):
            report += f"Duration: {operation['duration_ms']:.2f}ms\n"
            
        if operation.get("query"):
            report += f"\nQuery: {operation['query']}\n"
            
        if operation.get("params"):
            report += "\nParameters:\n"
            for k, v in operation["params"].items():
                report += f"  - {k}: {v}\n"
                
        if operation.get("summary"):
            report += f"\nSummary: {operation['summary']}\n"
            
        if operation.get("results"):
            report += "\nResults:\n"
            results = operation["results"]
            
            if isinstance(results, dict):
                if "count" in results:
                    report += f"  - Found {results['count']} items\n"
                    
                if "top_items" in results and results["top_items"]:
                    report += "  - Top matches:\n"
                    for idx, item in enumerate(results["top_items"]):
                        preview = str(item)[:100] + "..." if len(str(item)) > 100 else str(item)
                        report += f"    {idx+1}. {preview}\n"
                        
                if "original_size" in results:
                    report += f"  - Original size: {results['original_size']} chars\n"
                    report += f"  - Compressed size: {results['compressed_size']} chars\n"
                    report += f"  - Compression ratio: {results['compression_ratio']:.2f}\n"
                    
                if "data" in results:
                    report += f"  - Data: {results['data']}\n"
            else:
                report += f"  {str(results)[:500]}\n"
                
        return report
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about memory operations.
        
        Returns:
            Dictionary of statistics
        """
        with self.lock:
            # Calculate averages for performance metrics
            avg_search_time = sum(self.performance_stats["search_times_ms"]) / max(1, len(self.performance_stats["search_times_ms"]))
            avg_retrieval_time = sum(self.performance_stats["retrieval_times_ms"]) / max(1, len(self.performance_stats["retrieval_times_ms"]))
            avg_compression_time = sum(self.performance_stats["compression_times_ms"]) / max(1, len(self.performance_stats["compression_times_ms"]))
            
            # Estimate tokens saved with compression
            tokens_saved = self.usage_stats["token_count"] - self.usage_stats["compressed_token_count"]
            
            # Compile all statistics
            stats = {
                "token_usage": {
                    "searches": self.usage_stats["search_count"],
                    "retrievals": self.usage_stats["retrieval_count"],
                    "compressions": self.usage_stats["compression_count"],
                    "total_tokens": self.usage_stats["token_count"],
                    "compressed_tokens": self.usage_stats["compressed_token_count"],
                    "estimated_tokens_saved": tokens_saved
                },
                "performance": {
                    "avg_search_time_ms": avg_search_time,
                    "avg_retrieval_time_ms": avg_retrieval_time,
                    "avg_compression_time_ms": avg_compression_time
                },
                "operations": {
                    "total": len(self.operations),
                    "by_type": self._count_operations_by_type()
                }
            }
            
            return stats
            
    def _count_operations_by_type(self) -> Dict[str, int]:
        """Count operations by type."""
        type_counts = {}
        for op in self.operations:
            op_type = op["operation_type"]
            type_counts[op_type] = type_counts.get(op_type, 0) + 1
        return type_counts
    
    def update_token_usage(self, original_tokens: int, compressed_tokens: Optional[int] = None):
        """
        Update token usage statistics.
        
        Args:
            original_tokens: Number of tokens in original content
            compressed_tokens: Number of tokens after compression (if applicable)
        """
        if not self.enable_logging:
            return
            
        with self.lock:
            self.usage_stats["token_count"] += original_tokens
            if compressed_tokens is not None:
                self.usage_stats["compressed_token_count"] += compressed_tokens
                
    def clear_data(self):
        """Clear all stored operations and reset statistics."""
        with self.lock:
            self.operations = []
            self.operation_counter = 0
            
            # Reset performance tracking
            self.performance_stats = {
                "search_times_ms": [],
                "retrieval_times_ms": [],
                "compression_times_ms": [],
            }
            
            # Reset usage statistics
            self.usage_stats = {
                "search_count": 0,
                "retrieval_count": 0,
                "compression_count": 0,
                "token_count": 0,
                "compressed_token_count": 0,
            }
    
    def _generate_preview(self, content: str, max_length: int = 100) -> str:
        """
        Generate a preview of content text.
        
        Args:
            content: The content to preview
            max_length: Maximum preview length
            
        Returns:
            Content preview
        """
        if len(content) <= max_length:
            return content
            
        return content[:max_length] + "..."
    
    def _log_event(self, message: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an event to the execution trace.
        
        Args:
            message: Event message
            data: Optional event data
        """
        if not self.operations:
            return
            
        event = {
            "timestamp": time.time(),
            "message": message,
            "data": data or {}
        }
        
        self.operations[-1]["execution_trace"].append(event)
        
        # Also print to console for immediate feedback
        print(f"[Memory] {message}")
    
    def _save_log_file(self) -> None:
        """Save the current operation to a log file."""
        if not self.enable_logging or not self.operations:
            return
            
        # Create a filename based on operation type and ID
        op_type = self.operations[-1]["operation_type"]
        op_id = self.operations[-1]["operation_id"]
        timestamp = datetime.fromtimestamp(self.operations[-1]["timestamp"]).strftime("%Y%m%d_%H%M%S")
        
        filename = f"logs/memory_{op_type}_{op_id}_{timestamp}.json"
        
        # Write operation to file
        with open(filename, 'w') as f:
            json.dump(self.operations[-1], f, indent=2)
    
    def get_operation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent memory operations history.
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of recent operations
        """
        # Return most recent operations first
        return list(reversed(self.operations[-limit:]))
    
    def get_operation_by_id(self, operation_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific operation by ID.
        
        Args:
            operation_id: ID of the operation to retrieve
            
        Returns:
            Operation if found, None otherwise
        """
        for op in self.operations:
            if op["operation_id"] == operation_id:
                return op
                
        return None
    
    def generate_operation_report(self, operation_id: Optional[int] = None) -> str:
        """
        Generate a human-readable report for a memory operation.
        
        Args:
            operation_id: ID of operation to report, or None for most recent
            
        Returns:
            Formatted report text
        """
        operation = None
        
        if operation_id is not None:
            operation = self.get_operation_by_id(operation_id)
        elif self.operations:
            operation = self.operations[-1]
            
        if not operation:
            return "No operation found."
            
        # Build the report
        report = []
        report.append(f"Memory Operation Report: {operation['operation_type'].upper()}")
        report.append(f"ID: {operation['operation_id']}")
        
        if operation['query']:
            report.append(f"Query: \"{operation['query']}\"")
            
        report.append(f"Duration: {operation['duration_ms']:.2f}ms")
        
        # Add memory access information
        if operation['accessed_items']:
            report.append("\nMemory Items Accessed:")
            for i, item in enumerate(operation['accessed_items']):
                report.append(f"  {i+1}. {item['item_type']} item {item['item_id']}")
                report.append(f"     Reason: {item['reason']}")
        
        # Add search results
        if operation['result_items']:
            report.append("\nTop Search Results:")
            for i, result in enumerate(operation['result_items'][:3]):  # Show top 3
                report.append(f"  {i+1}. ID: {result['item_id']} (Score: {result['relevance_score']:.2f}, Confidence: {result['confidence']})")
                report.append(f"     Preview: {result['content_preview']}")
                
                # Add score explanation if available
                if 'score_details' in result and result['score_details']:
                    report.append("     Scoring factors:")
                    factors = result['score_details'].get('factor_scores', {})
                    for factor, score in factors.items():
                        report.append(f"       - {factor}: {score:.2f}")
        
        # Add summary if available
        if 'summary' in operation and operation['summary']:
            report.append(f"\nSummary: {operation['summary']}")
            
        return "\n".join(report) 