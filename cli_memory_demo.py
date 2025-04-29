"""
CLI Memory Visualization Demo

This script demonstrates the CLI-based memory visualization features
that are available in the current implementation.
"""

from src.cli.memory_ui import MemoryUI
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
import time

def main():
    print("Initializing CLI Memory Visualization...")
    
    # Create console and memory UI
    console = Console()
    memory_ui = MemoryUI(console=console)
    
    # Create mock memory state
    mock_memory = {
        "chat_history": {
            "messages": [
                {"type": "human", "content": "What is Laravel?"},
                {"type": "ai", "content": "Laravel is a PHP framework..."}
            ]
        },
        "dual_memory": {
            "temporary_memory": {
                "get_messages": lambda: [
                    {"role": "user", "content": "What is Laravel?"},
                    {"role": "assistant", "content": "Laravel is a PHP framework..."}
                ]
            },
            "permanent_memory": {
                "get_count": lambda: 3
            }
        }
    }
    
    # Show memory state
    print("\n=== Memory State ===")
    memory_ui.show_memory_state(mock_memory)
    
    # Show memory thinking
    print("\n=== Memory Thinking ===")
    memory_ui.memory_thinking("Processing user query about Laravel features")
    
    # Show memory usage
    print("\n=== Memory Usage ===")
    memory_ui.show_memory_usage("search", "temporary")
    memory_ui.show_memory_usage("retrieval", "permanent")
    
    # Show analyzing memory
    print("\n=== Memory Analysis ===")
    progress = memory_ui.analyzing_temporary_memory()
    if progress:
        try:
            task = progress.add_task("Analyzing conversation history", total=100)
            for i in range(101):
                progress.update(task, completed=i)
                time.sleep(0.02)
            progress.stop()
        except Exception as e:
            print(f"Error with progress bar: {e}")
    
    # Show code snippet - fixed implementation
    print("\n=== Code Snippet ===")
    code = """
    Route::get('/users', [UserController::class, 'index'])
        ->name('users.index');
    
    Route::get('/users/{user}', [UserController::class, 'show'])
        ->name('users.show');
    """
    # Directly use console instead of memory_ui for code snippet
    syntax = Syntax(code, "php", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="Laravel Routes Example"))
    
    # Show memory saving/loading
    print("\n=== Memory Persistence ===")
    memory_ui.memory_saved("memory.json")
    memory_ui.memory_loaded("memory.json", 2, 3)
    
    # Show search results
    print("\n=== Search Results ===")
    search_results = [
        {"id": "1", "content": "Laravel is a PHP framework", "relevance": 0.95},
        {"id": "2", "content": "Laravel features include MVC architecture", "relevance": 0.85}
    ]
    memory_ui.show_search_results(search_results, "Laravel features")
    
    # Show memory transition
    print("\n=== Memory Transition ===")
    memory_ui.show_memory_transition("temporary", "permanent", "High knowledge value")
    
    # Show error
    print("\n=== Error Handling ===")
    memory_ui.error("Failed to compress memory due to formatting error")

if __name__ == "__main__":
    main() 