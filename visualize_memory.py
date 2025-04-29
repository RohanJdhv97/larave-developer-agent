"""
Memory Visualization Demo

This script demonstrates the MemoryVisualization class features directly.
"""

from src.memory.memory_visualization import MemoryVisualization
import time

def main():
    print("Creating Memory Visualization module...")
    
    # Initialize the visualization system
    visualizer = MemoryVisualization(enable_logging=True)
    
    # Log some example operations
    print("Logging sample operations...")
    
    # Example search operation
    search_op_id = visualizer.log_operation(
        operation_type="search",
        query="Laravel features",
        params={"max_results": 5},
        results=["MVC architecture", "Eloquent ORM", "Blade templating"],
        duration_ms=45.7,
        summary="Searched for Laravel features"
    )
    
    # Example retrieval operation
    retrieval_op_id = visualizer.log_operation(
        operation_type="retrieval",
        query="message_123",
        params={"decompress": True},
        results={"content": "Laravel is a web application framework with expressive, elegant syntax."},
        duration_ms=12.3,
        summary="Retrieved message from memory"
    )
    
    # Example compression operation
    compression_op_id = visualizer.log_operation(
        operation_type="compression",
        params={"threshold": 1000},
        results={
            "original": "Laravel is a web application framework with expressive, elegant syntax. " * 10,
            "compressed": "Laravel is a web application framework with expressive, elegant syntax. [repeated 10x]"
        },
        duration_ms=22.5,
        summary="Compressed redundant content"
    )
    
    # Generate and display reports
    print("\n--- SEARCH OPERATION REPORT ---")
    print(visualizer.get_operation_report(search_op_id))
    
    print("\n--- RETRIEVAL OPERATION REPORT ---")
    print(visualizer.get_operation_report(retrieval_op_id))
    
    print("\n--- COMPRESSION OPERATION REPORT ---")
    print(visualizer.get_operation_report(compression_op_id))
    
    # Display statistics
    print("\n--- MEMORY STATISTICS ---")
    stats = visualizer.get_statistics()
    print(f"Total operations: {stats['operations']['total']}")
    print(f"Operations by type: {stats['operations']['by_type']}")
    print(f"Average search time: {stats['performance']['avg_search_time_ms']:.2f}ms")
    print(f"Average retrieval time: {stats['performance']['avg_retrieval_time_ms']:.2f}ms")
    print(f"Average compression time: {stats['performance']['avg_compression_time_ms']:.2f}ms")
    
    # Get recent operations
    print("\n--- RECENT OPERATIONS ---")
    recent_ops = visualizer.get_recent_operations(limit=5)
    for op in recent_ops:
        print(f"ID: {op['operation_id']} | Type: {op['operation_type']} | Summary: {op['summary']}")

if __name__ == "__main__":
    main() 