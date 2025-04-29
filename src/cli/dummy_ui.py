"""
Dummy UI implementation that implements the same interface as MemoryUI but doesn't display anything.
Used for testing, non-interactive environments, or when the rich library isn't available.
"""

from typing import Dict, List, Any, Optional, Union


class DummyUI:
    """
    A no-op implementation of the memory UI interface.
    All methods accept the same parameters but do nothing.
    """
    
    def __init__(self):
        """Initialize the dummy UI."""
        pass
        
    def show_memory_state(self, temporary_messages: int, permanent_entries: int, categories: List[str]):
        """No-op implementation of show_memory_state."""
        pass
        
    def memory_thinking(self, task: str):
        """No-op implementation of memory_thinking."""
        pass
        
    def show_memory_usage(self, operation: str, memory_type: str):
        """No-op implementation of show_memory_usage."""
        pass
        
    def analyzing_temporary_memory(self, with_progress: bool = False):
        """No-op implementation of analyzing_temporary_memory."""
        pass
        
    def show_storing_knowledge(self, entry_count: int, knowledge_entries: List[Dict[str, Any]]):
        """No-op implementation of show_storing_knowledge."""
        pass
        
    def show_code_snippet(self, code: str, language: str = "php"):
        """No-op implementation of show_code_snippet."""
        pass
        
    def memory_saved(self, path: str):
        """No-op implementation of memory_saved."""
        pass
        
    def memory_loaded(self, path: str, temporary_entries: int, permanent_entries: int):
        """No-op implementation of memory_loaded."""
        pass
        
    def show_memory_completion(self):
        """No-op implementation of show_memory_completion."""
        pass
        
    def show_search_results(self, entries: List[Any], query: str):
        """No-op implementation of show_search_results."""
        pass
        
    def conversation_summary(self, data: Dict[str, Any]):
        """No-op implementation of conversation_summary."""
        pass
        
    def show_memory_transition(self, from_memory: str, to_memory: str, reason: str):
        """No-op implementation of show_memory_transition."""
        pass
        
    def error(self, message: str):
        """No-op implementation of error."""
        pass


# Create a global instance for easy access
dummy_ui = DummyUI() 