import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Optional, Dict, List, Any, Callable
import threading
import time
import json
from datetime import datetime

class MemoryDashboard:
    """
    A graphical user interface component that displays memory operations in real-time.
    
    This dashboard provides visibility into:
    - Recent memory operations (search, retrieval, compression)
    - Memory access patterns
    - Details of current memory operation
    - Visualization of relevance scoring
    """
    
    def __init__(
        self, 
        parent: Optional[tk.Tk] = None,
        memory_system = None,
        refresh_interval: int = 1000,  # milliseconds
        max_operations: int = 10
    ):
        """
        Initialize the memory dashboard.
        
        Args:
            parent: Parent Tkinter window
            memory_system: Reference to OptimizedMemorySystem instance
            refresh_interval: How often to refresh the display (ms)
            max_operations: Maximum number of operations to display
        """
        self.parent = parent or tk.Tk()
        self.memory_system = memory_system
        self.refresh_interval = refresh_interval
        self.max_operations = max_operations
        
        # Initialize Tkinter frame if we're in the main thread
        self.initialized = False
        self.should_stop = False
        
        # If called from a different thread, defer initialization
        if threading.current_thread() is threading.main_thread():
            self._initialize_ui()
        
    def _initialize_ui(self):
        """Set up the UI components."""
        if self.initialized:
            return
            
        self.initialized = True
        self.parent.title("Memory Operations Dashboard")
        self.parent.geometry("900x700")
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.parent, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#f5f5f5')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        
        # Header with title
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame, 
            text="Memory Operations Monitor", 
            style='Title.TLabel'
        )
        title_label.pack(side=tk.LEFT)
        
        # Memory operations section
        op_frame = ttk.LabelFrame(main_frame, text="Recent Memory Operations", padding=10)
        op_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Operations list
        columns = ('time', 'operation', 'query', 'summary')
        self.operations_tree = ttk.Treeview(op_frame, columns=columns, show='headings')
        
        # Configure columns
        self.operations_tree.heading('time', text='Time')
        self.operations_tree.heading('operation', text='Operation')
        self.operations_tree.heading('query', text='Query')
        self.operations_tree.heading('summary', text='Summary')
        
        self.operations_tree.column('time', width=80)
        self.operations_tree.column('operation', width=100)
        self.operations_tree.column('query', width=250)
        self.operations_tree.column('summary', width=350)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(op_frame, orient=tk.VERTICAL, command=self.operations_tree.yview)
        self.operations_tree.configure(yscroll=scrollbar.set)
        
        # Pack tree and scrollbar
        self.operations_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add selection event
        self.operations_tree.bind('<<TreeviewSelect>>', self.on_operation_selected)
        
        # Operation details section
        details_frame = ttk.LabelFrame(main_frame, text="Operation Details", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Details text area
        self.details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, height=15)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.config(state=tk.DISABLED)
        
        # Stats section
        stats_frame = ttk.LabelFrame(main_frame, text="Memory System Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=5)
        
        # Stats text area
        self.stats_text = scrolledtext.ScrolledText(stats_frame, wrap=tk.WORD, height=6)
        self.stats_text.pack(fill=tk.BOTH)
        self.stats_text.config(state=tk.DISABLED)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_check = ttk.Checkbutton(
            control_frame, 
            text="Auto-refresh", 
            variable=self.auto_refresh_var
        )
        auto_refresh_check.pack(side=tk.LEFT)
        
        refresh_button = ttk.Button(
            control_frame, 
            text="Refresh Now", 
            command=self.refresh_dashboard
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        close_button = ttk.Button(
            control_frame, 
            text="Close", 
            command=self.close
        )
        close_button.pack(side=tk.RIGHT)
        
        # Start the refresh timer
        if self.auto_refresh_var.get():
            self.refresh_timer()
            
        # Empty placeholder data
        self.update_operations([])
        self.update_stats({})
        
    def show(self):
        """Display the dashboard."""
        if not self.initialized:
            self._initialize_ui()
            
        self.parent.deiconify()  # Show window
        
    def close(self):
        """Close the dashboard."""
        self.should_stop = True
        self.parent.withdraw()  # Hide window
        
    def destroy(self):
        """Completely destroy the window."""
        self.should_stop = True
        if self.initialized:
            self.parent.destroy()
            
    def refresh_timer(self):
        """Timer function for auto-refreshing the dashboard."""
        if self.should_stop:
            return
            
        if self.auto_refresh_var.get():
            self.refresh_dashboard()
            
        # Schedule next refresh
        self.parent.after(self.refresh_interval, self.refresh_timer)
        
    def refresh_dashboard(self):
        """Refresh the dashboard data."""
        if not self.memory_system:
            return
            
        # Get recent operations
        operations = self.memory_system.get_recent_memory_operations(limit=self.max_operations)
        self.update_operations(operations)
        
        # Get system stats
        stats = self.memory_system.get_optimization_stats()
        self.update_stats(stats)
        
    def update_operations(self, operations: List[Dict[str, Any]]):
        """
        Update the operations list display.
        
        Args:
            operations: List of operation data
        """
        # Clear existing items
        for i in self.operations_tree.get_children():
            self.operations_tree.delete(i)
            
        # Add new items (in reverse order - newest first)
        for op in reversed(operations):
            # Format time
            timestamp = op.get('timestamp', 0)
            if isinstance(timestamp, (int, float)):
                time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
            else:
                time_str = str(timestamp)
                
            # Insert into tree
            self.operations_tree.insert(
                '', 
                'end', 
                values=(
                    time_str,
                    op.get('operation_type', 'unknown'),
                    op.get('query', '')[:50] + ('...' if len(op.get('query', '')) > 50 else ''),
                    op.get('summary', '')[:50] + ('...' if len(op.get('summary', '')) > 50 else '')
                ),
                tags=(str(op.get('operation_id', 0)),)
            )
            
    def update_stats(self, stats: Dict[str, Any]):
        """
        Update the statistics display.
        
        Args:
            stats: Dictionary of system statistics
        """
        # Format the stats into readable text
        if not stats:
            stats_text = "No statistics available"
        else:
            stats_text = "Memory System Statistics:\n\n"
            
            # Token usage
            token_usage = stats.get('token_usage', {})
            stats_text += f"Searches: {token_usage.get('searches', 0)} | "
            stats_text += f"Compressions: {token_usage.get('compressions', 0)} | "
            stats_text += f"Retrievals: {token_usage.get('retrievals', 0)} | "
            stats_text += f"Estimated Tokens Saved: {int(token_usage.get('estimated_tokens_saved', 0))}\n\n"
            
            # Performance
            perf = stats.get('performance', {})
            stats_text += "Average Times (ms):\n"
            stats_text += f"Search: {perf.get('avg_search_time_ms', 0):.2f} | "
            stats_text += f"Retrieval: {perf.get('avg_retrieval_time_ms', 0):.2f} | "
            stats_text += f"Compression: {perf.get('avg_compression_time_ms', 0):.2f}\n\n"
            
            # Search engine
            search = stats.get('search_engine', {})
            stats_text += f"Cache Hit Rate: {search.get('cache_hit_rate', 0)*100:.1f}% | "
            stats_text += f"Total Searches: {search.get('total_searches', 0)}"
        
        # Update the text widget
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', stats_text)
        self.stats_text.config(state=tk.DISABLED)
        
    def on_operation_selected(self, event):
        """Handle selection of an operation from the list."""
        selection = self.operations_tree.selection()
        if not selection or not self.memory_system:
            return
            
        # Get operation ID from the selected item's tags
        item = self.operations_tree.item(selection[0])
        tags = item.get('tags', [])
        if not tags:
            return
            
        try:
            operation_id = int(tags[0])
        except (ValueError, IndexError):
            return
            
        # Get the detailed report
        report = self.memory_system.get_memory_operation_report(operation_id)
        
        # Update the details display
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert('1.0', report)
        self.details_text.config(state=tk.DISABLED)
        
    def start_standalone(self):
        """Run the dashboard as a standalone window."""
        if not self.initialized:
            self._initialize_ui()
        
        try:
            self.parent.mainloop()
        except KeyboardInterrupt:
            self.destroy()


# Optional commandline starter for testing
if __name__ == "__main__":
    import sys
    import os
    
    # Add parent directory to path to allow imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from src.memory.optimized_memory import OptimizedMemorySystem
    
    # Create a memory system for testing
    memory_system = OptimizedMemorySystem(enable_visualization=True)
    
    # Add some sample data
    memory_system.add_message({
        "id": "msg1",
        "role": "user",
        "content": "What is the capital of France?"
    })
    
    memory_system.add_message({
        "id": "msg2",
        "role": "assistant",
        "content": "The capital of France is Paris."
    })
    
    # Do a search
    memory_system.search_memory("capital city", max_results=3)
    
    # Store some knowledge
    memory_system.store_knowledge([
        {
            "id": "k1",
            "content": "Paris is the capital and most populous city of France.",
            "source": "conversation"
        }
    ])
    
    # Create and show dashboard
    dashboard = MemoryDashboard(memory_system=memory_system)
    dashboard.start_standalone() 