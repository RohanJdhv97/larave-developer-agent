"""
Dual Memory System

This module provides a dual memory system that integrates both temporary and permanent memory,
with visual feedback through the UI component.
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime

from src.cli.memory_ui import MemoryUI, memory_ui
from src.memory.temporary_memory import TemporaryMemory
from src.memory.permanent_memory import PermanentMemory


class DualMemorySystem:
    """
    A memory system that combines temporary and permanent memory with visual feedback.
    
    The DualMemorySystem integrates temporary memory for recent conversation context
    and permanent memory for long-term knowledge storage. It provides:
    - Visual feedback through a UI component
    - Seamless transitions between memory types
    - Analytics on memory usage and operations
    - Persistence through save/load functionality
    """
    
    def __init__(
        self, 
        temporary_memory: Optional[TemporaryMemory] = None,
        permanent_memory: Optional[PermanentMemory] = None,
        ui: Optional[MemoryUI] = None
    ):
        """
        Initialize the dual memory system.
        
        Args:
            temporary_memory: Optional TemporaryMemory instance
            permanent_memory: Optional PermanentMemory instance
            ui: Optional MemoryUI instance for visual feedback
        """
        # Initialize memories
        self.temporary_memory = temporary_memory or TemporaryMemory()
        self.permanent_memory = permanent_memory or PermanentMemory()
        
        # UI component for visual feedback
        self.ui = ui or memory_ui
        
        # Session analytics
        self.session_start = datetime.now().isoformat()
        self.messages_count = 0
        self.knowledge_entries_count = 0
        self.memory_transitions = 0
        self.searches_performed = 0
        
        # Initial UI update
        self._update_memory_state_display()
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """
        Add a message to temporary memory with visual feedback.
        
        Args:
            message: The message to add (must contain 'role' and 'content' keys)
        """
        # Show user interface notification
        self.ui.show_memory_usage("Adding message", "temporary")
        
        # Add to temporary memory
        self.temporary_memory.add_message(message)
        
        # Update analytics
        self.messages_count += 1
        
        # Update UI
        self._update_memory_state_display()
    
    def analyze_temporary_memory(self) -> List[Dict[str, Any]]:
        """
        Analyze temporary memory to extract knowledge, with visual progress indication.
        
        Returns:
            List of extracted knowledge entries
        """
        # Start analysis with progress indicator
        progress = self.ui.analyzing_temporary_memory(with_progress=True)
        task_id = None
        
        try:
            if progress:
                # Add a task to the progress bar
                task_id = progress.add_task("Analyzing conversations...", total=100)
            
            # Extract knowledge from messages
            messages = self.temporary_memory.get_messages()
            
            # Simulate progress updates
            if progress and task_id is not None:
                progress.update(task_id, completed=30, description="Identifying key concepts...")
                
            # Extract knowledge from messages
            knowledge_entries = self._extract_knowledge_from_messages(messages)
            
            if progress and task_id is not None:
                progress.update(task_id, completed=70, description="Categorizing knowledge...")
                
            # Final progress update
            if progress and task_id is not None:
                progress.update(task_id, completed=100, description="Finalizing analysis...")
                
            return knowledge_entries
            
        finally:
            # Always complete the progress indicator
            self.ui.show_memory_completion()
    
    def _extract_knowledge_from_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract knowledge entries from messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            List of knowledge entries extracted from messages
        """
        # This is a simplified implementation - in a real system, this would
        # use a more sophisticated analysis of the conversation
        
        knowledge_entries = []
        
        # For this example, we'll consider user messages with at least 20 chars as knowledge
        for message in messages:
            if message.get("role") == "user" and len(message.get("content", "")) >= 20:
                # Extract content and create timestamp
                content = message.get("content", "")
                timestamp = message.get("timestamp", datetime.now().isoformat())
                
                # Simple category determination based on content keywords
                category = "general"
                if any(term in content.lower() for term in ["code", "function", "class", "programming"]):
                    category = "code"
                elif any(term in content.lower() for term in ["question", "how", "what", "why"]):
                    category = "question"
                elif any(term in content.lower() for term in ["fact", "remember", "important"]):
                    category = "fact"
                
                # Create knowledge entry
                entry = {
                    "content": content,
                    "category": category,
                    "source": "user_message",
                    "timestamp": timestamp
                }
                
                knowledge_entries.append(entry)
        
        return knowledge_entries
    
    def store_in_permanent_memory(self, entries: List[Dict[str, Any]]) -> None:
        """
        Store knowledge entries in permanent memory with visual feedback.
        
        Args:
            entries: List of knowledge entries to store
        """
        # Show transition from temporary to permanent memory
        self.ui.show_memory_transition(
            "Temporary Memory", 
            "Permanent Memory",
            "Storing important knowledge for long-term recall"
        )
        
        # Add each entry to permanent memory
        for entry in entries:
            self.permanent_memory.add_entry(entry)
        
        # Update analytics
        self.knowledge_entries_count += len(entries)
        self.memory_transitions += 1
        
        # Show what was stored
        self.ui.show_storing_knowledge(len(entries), entries)
        
        # Update UI state
        self._update_memory_state_display()
    
    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        """
        Search across both temporary and permanent memory.
        
        Args:
            query: The search query string
            
        Returns:
            List of search results from both memory types
        """
        # Show thinking indication
        self.ui.memory_thinking(f"Searching memory for: '{query}'")
        
        # Search in both memory types
        temp_results = self.temporary_memory.search(query)
        
        # Handle different permanent memory implementations
        if hasattr(self.permanent_memory, 'search'):
            perm_results = self.permanent_memory.search(query)
        else:
            # Default to empty list if search method doesn't exist
            perm_results = []
        
        # Mark results with their source
        for result in temp_results:
            result["source"] = "temporary_memory"
        
        for result in perm_results:
            result["source"] = "permanent_memory"
        
        # Combine and sort by relevance
        all_results = temp_results + perm_results
        all_results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        
        # Update analytics
        self.searches_performed += 1
        
        # Show results
        self.ui.show_search_results(all_results, query)
        
        return all_results
    
    def save_memory(self, file_path: str) -> bool:
        """
        Save the current memory state to a file.
        
        Args:
            file_path: Path to save the memory state
            
        Returns:
            True if save was successful, False otherwise
        """
        # Check for empty or None path
        if not file_path:
            self.ui.error("Failed to save memory: Empty file path")
            return False
            
        # Get temporary memory messages
        temp_messages = self.temporary_memory.get_messages()
        
        # Different permanent memory implementations may have different methods
        if hasattr(self.permanent_memory, 'get_entries'):
            perm_entries = self.permanent_memory.get_entries()
        elif hasattr(self.permanent_memory, 'get_all_knowledge'):
            perm_entries = self.permanent_memory.get_all_knowledge()
        else:
            perm_entries = []
        
        # Prepare memory state
        memory_state = {
            "temporary_memory": temp_messages,
            "permanent_memory": perm_entries,
            "analytics": {
                "session_start": self.session_start,
                "messages_count": self.messages_count,
                "knowledge_entries_count": self.knowledge_entries_count,
                "memory_transitions": self.memory_transitions,
                "searches_performed": self.searches_performed
            }
        }
        
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(os.path.abspath(file_path))
            # Create directory structure even if empty directory name
            os.makedirs(directory, exist_ok=True)
            
            # Write to file
            with open(file_path, 'w') as f:
                json.dump(memory_state, f, indent=2)
            
            # Show success notification
            self.ui.memory_saved(file_path)
            return True
            
        except Exception as e:
            # Show error
            self.ui.error(f"Failed to save memory: {str(e)}")
            return False
    
    def load_memory(self, file_path: str) -> bool:
        """
        Load memory state from a file.
        
        Args:
            file_path: Path to load the memory state from
            
        Returns:
            True if load was successful, False otherwise
        """
        try:
            # Read from file
            with open(file_path, 'r') as f:
                memory_state = json.load(f)
            
            # Restore temporary memory
            temp_messages = memory_state.get("temporary_memory", [])
            self.temporary_memory.clear()
            for message in temp_messages:
                self.temporary_memory.add_message(message)
            
            # Restore permanent memory - handle different implementations
            perm_entries = memory_state.get("permanent_memory", [])
            
            # Different permanent memory implementations use different methods
            if hasattr(self.permanent_memory, 'clear'):
                self.permanent_memory.clear()
            
            # Add entries using the appropriate method
            if hasattr(self.permanent_memory, 'add_entry'):
                for entry in perm_entries:
                    self.permanent_memory.add_entry(entry)
            elif hasattr(self.permanent_memory, 'add_knowledge'):
                self.permanent_memory.add_knowledge(perm_entries)
            
            # Restore analytics
            analytics = memory_state.get("analytics", {})
            self.session_start = analytics.get("session_start", self.session_start)
            self.messages_count = analytics.get("messages_count", 0)
            self.knowledge_entries_count = analytics.get("knowledge_entries_count", 0)
            self.memory_transitions = analytics.get("memory_transitions", 0)
            self.searches_performed = analytics.get("searches_performed", 0)
            
            # Show success notification
            self.ui.memory_loaded(
                file_path, 
                len(temp_messages), 
                len(perm_entries)
            )
            
            # Update UI
            self._update_memory_state_display()
            return True
            
        except Exception as e:
            # Show error
            self.ui.error(f"Failed to load memory: {str(e)}")
            return False
    
    def _update_memory_state_display(self) -> None:
        """Update the memory state display in the UI."""
        try:
            # Only call show_memory_state on self as we now can traverse the memory reference
            if hasattr(self.ui, 'show_memory_state'):
                self.ui.show_memory_state(self)
        except Exception as e:
            # Fail gracefully for UI issues
            print(f"Error updating memory display: {str(e)}")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of conversation and memory statistics.
        
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            "session_start": self.session_start,
            "messages_count": self.messages_count,
            "knowledge_entries_count": self.knowledge_entries_count,
            "memory_transitions": self.memory_transitions,
            "searches_performed": self.searches_performed,
            "temporary_memory_count": len(self.temporary_memory.get_messages()),
            "permanent_memory_count": len(self.permanent_memory.get_entries())
        }
        
        # Display summary in UI
        self.ui.conversation_summary(summary)
        
        return summary
    
    def clear_temporary_memory(self) -> None:
        """Clear temporary memory and update UI."""
        self.temporary_memory.clear()
        self.ui.memory_thinking("Temporary memory cleared")
        self._update_memory_state_display()
    
    def clear_permanent_memory(self) -> None:
        """Clear permanent memory and update UI."""
        self.permanent_memory.clear()
        self.ui.memory_thinking("Permanent memory cleared")
        self._update_memory_state_display() 