"""
Memory Adapter for DualMemorySystem

This module provides an adapter that allows the Laravel Agent to use the 
visual DualMemorySystem with Rich UI while maintaining compatibility.
"""

from typing import Dict, List, Any, Optional
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage

from src.memory.dual_memory import DualMemorySystem
from src.memory.temporary_memory import TemporaryMemory
from src.memory.permanent_memory import PermanentMemory
from src.cli.memory_ui import memory_ui, MemoryUI

class ChatHistoryAdapter:
    """
    Adapter to make the dual memory chat history compatible with the Langchain format
    expected by the CLI's memory display function.
    """
    def __init__(self, memory):
        self.memory = memory
    
    @property
    def messages(self) -> List[BaseMessage]:
        """
        Convert DualMemory messages to Langchain messages
        """
        try:
            if not self.memory or not hasattr(self.memory, 'temporary_memory'):
                return []
                
            langchain_messages = []
            for msg in self.memory.temporary_memory.get_messages():
                role = msg.get('role', '')
                if role == 'user':
                    langchain_messages.append(HumanMessage(content=msg.get('content', '')))
                elif role == 'assistant':
                    langchain_messages.append(AIMessage(content=msg.get('content', '')))
                elif role == 'system':
                    langchain_messages.append(SystemMessage(content=msg.get('content', '')))
                    
            return langchain_messages
        except Exception as e:
            print(f"Error accessing messages in ChatHistoryAdapter: {str(e)}")
            return []

class MessageContainer:
    """
    Simple container class for messages that provides the expected interface.
    
    This class wraps a list of message objects (HumanMessage, AIMessage, etc.) and provides
    a 'messages' attribute that returns the list directly. This is necessary because some
    parts of the system expect chat_history to be an object with a 'messages' attribute,
    while others expect it to be a direct list of messages.
    
    The primary purpose is to maintain compatibility with code that accesses chat history
    through the '.messages' attribute pattern while still allowing direct iteration and
    access to the underlying message list.
    
    Attributes:
        _messages: The underlying list of message objects
    """
    def __init__(self, messages):
        """
        Initialize the container with a list of messages.
        
        Args:
            messages: A list of message objects (HumanMessage, AIMessage, etc.)
        """
        self._messages = messages
    
    @property
    def messages(self):
        """
        Return the contained messages list.
        
        This property is accessed by code expecting the chat_history.messages pattern.
        
        Returns:
            The list of message objects
        """
        return self._messages
    
    def __len__(self):
        """
        Get the number of messages in the container.
        
        Returns:
            The number of messages
        """
        return len(self._messages)

class DualMemoryAdapter:
    """
    Adapter that makes DualMemorySystem compatible with the Laravel Agent memory interface.
    
    This adapter wraps the visual DualMemorySystem to provide the same interface
    as LaravelAgentMemory, allowing it to be used by the agent without major changes.
    """
    
    def __init__(self, memory_path: str = "memory/agent"):
        """
        Initialize the dual memory adapter.
        
        Args:
            memory_path: Path to store memory files
        """
        try:
            # Create necessary components
            temporary_memory = TemporaryMemory()
            permanent_memory = PermanentMemory()
            ui = memory_ui
            
            # Initialize the dual memory system with proper components
            self.dual_memory = DualMemorySystem(
                temporary_memory=temporary_memory,
                permanent_memory=permanent_memory,
                ui=ui
            )
            self.memory_path = memory_path
            
            # Create chat history adapter for CLI compatibility
            self._chat_history_adapter = ChatHistoryAdapter(self.dual_memory)
            
            # Initialize the chat_history attribute as a property
            self._initialize_chat_history()
            
        except Exception as e:
            print(f"Error initializing DualMemoryAdapter: {str(e)}")
            # Create empty fallback objects to prevent attribute errors
            self.dual_memory = None
            self.memory_path = memory_path
            self._chat_history_adapter = None
            self._messages = []
            self._message_container = MessageContainer([])
    
    def _initialize_chat_history(self):
        """
        Initialize the chat_history attribute with the current messages
        from the dual memory system in Langchain format.
        """
        try:
            self._messages = []
            if self.dual_memory and hasattr(self.dual_memory, 'temporary_memory'):
                messages = self.dual_memory.temporary_memory.get_messages()
                for msg in messages:
                    if msg.get("role") == "user":
                        self._messages.append(HumanMessage(content=msg.get("content", "")))
                    elif msg.get("role") == "assistant":
                        self._messages.append(AIMessage(content=msg.get("content", "")))
                    elif msg.get("role") == "system":
                        self._messages.append(SystemMessage(content=msg.get("content", "")))
            
            # Create a container object that has a messages property
            self._message_container = MessageContainer(self._messages)
        except Exception as e:
            print(f"Error initializing chat history: {str(e)}")
            self._messages = []
            self._message_container = MessageContainer([])
        
    @property
    def chat_history_adapter(self):
        """
        Return a chat history adapter compatible with the CLI memory display
        """
        return self._chat_history_adapter
    
    @property
    def chat_history(self):
        """
        Return a container object with a messages attribute for compatibility with CLI display.
        This ensures code that expects chat_history.messages will work.
        """
        return self._message_container
        
    def add_user_message(self, message: str):
        """Add a user message to memory."""
        try:
            if self.dual_memory:
                self.dual_memory.add_message({
                    "role": "user",
                    "content": message,
                    "type": "message"
                })
                # Update the chat_history property
                self._messages.append(HumanMessage(content=message))
        except Exception as e:
            print(f"Error adding user message: {str(e)}")
        
    def add_ai_message(self, message: str):
        """Add an AI message to memory."""
        try:
            if self.dual_memory:
                self.dual_memory.add_message({
                    "role": "assistant",
                    "content": message,
                    "type": "message"
                })
                # Update the chat_history property
                self._messages.append(AIMessage(content=message))
        except Exception as e:
            print(f"Error adding AI message: {str(e)}")
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """
        Get all memory variables for use in prompt context.
        
        Returns:
            Dict containing chat_history and other memory variables
        """
        try:
            # Return the already converted Langchain message format
            return {
                "chat_history": self._messages,
                "chat_summary": self._get_chat_summary(),
                "project_context": {}  # Empty for now, could be populated from permanent memory
            }
        except Exception as e:
            print(f"Error getting memory variables: {str(e)}")
            return {
                "chat_history": [],
                "chat_summary": "Error retrieving chat summary",
                "project_context": {}
            }
    
    def _get_chat_summary(self) -> str:
        """Get a simple summary of the conversation."""
        try:
            if self.dual_memory and hasattr(self.dual_memory, 'temporary_memory'):
                messages = self.dual_memory.temporary_memory.get_messages()
                return f"Conversation with {len(messages)} messages"
            return "No conversation"
        except Exception as e:
            print(f"Error getting chat summary: {str(e)}")
            return "Error retrieving chat summary"
    
    def save(self, path: str = None):
        """
        Save memory to a file.
        
        Args:
            path: Path to save memory to, uses default if None or empty
        """
        # Ensure directory exists
        import os
        
        try:
            # If path is empty or None, use default path
            if not path:
                # Create a properly formed default path
                path = os.path.join(self.memory_path, "memory.json")
                
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            
            # Save using dual memory system
            if self.dual_memory and hasattr(self.dual_memory, 'save_memory'):
                if self.dual_memory.save_memory(path):
                    print(f"Memory saved to {path}")
            else:
                print("Unable to save memory: dual memory system not initialized")
        except Exception as e:
            print(f"Failed to save memory: {str(e)}")
        
    @classmethod
    def load(cls, path: str = None) -> "DualMemoryAdapter":
        """
        Class method to load memory from a file.
        
        Args:
            path: Path to load memory from, uses default if None or empty
            
        Returns:
            DualMemoryAdapter with loaded memory
        """
        import os
        
        # Create a new adapter instance
        adapter = cls()
        
        try:
            if not path:
                # Use default path if none provided
                path = os.path.join(adapter.memory_path, "memory.json")
                
            if not os.path.exists(path):
                print(f"Memory file not found: {path}")
                return adapter
            
            if adapter.dual_memory and hasattr(adapter.dual_memory, 'load_memory'):
                adapter.dual_memory.load_memory(path)
                # Reinitialize chat_history with loaded content
                adapter._initialize_chat_history()
                print(f"Memory loaded from {path}")
            else:
                print("Unable to load memory: dual memory system not initialized")
        except Exception as e:
            print(f"Error loading memory: {str(e)}")
        
        return adapter
    
    def clear(self):
        """Clear temporary memory."""
        try:
            if self.dual_memory and hasattr(self.dual_memory, 'clear_temporary_memory'):
                self.dual_memory.clear_temporary_memory()
                # Reset chat_history as well
                self._messages = []
                self._message_container = MessageContainer([])
        except Exception as e:
            print(f"Error clearing memory: {str(e)}")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation."""
        try:
            if self.dual_memory and hasattr(self.dual_memory, 'get_conversation_summary'):
                return self.dual_memory.get_conversation_summary()
            return {"summary": "No conversation summary available", "message_count": 0}
        except Exception as e:
            print(f"Error getting conversation summary: {str(e)}")
            return {"summary": "Error retrieving conversation summary", "message_count": 0} 