"""
Temporary Memory System

This module provides temporary (working) memory for storing recent conversation context.
"""

import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime


class TemporaryMemory:
    """
    A memory system for storing recent conversation messages.
    
    Temporary Memory stores the most recent messages in a conversation context,
    providing:
    - Message storage with timestamps
    - Search functionality for finding relevant messages
    - Clear boundaries on what constitutes "recent" context
    """
    
    def __init__(self, max_messages: int = 50):
        """
        Initialize temporary memory system.
        
        Args:
            max_messages: Maximum number of messages to store (defaults to 50)
        """
        self._messages = []
        self.max_messages = max_messages
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """
        Add a message to memory.
        
        Args:
            message: Message dictionary containing at least 'role' and 'content'
        """
        # Validate message has required fields
        if not isinstance(message, dict) or not all(key in message for key in ['role', 'content']):
            raise ValueError("Message must be a dictionary with 'role' and 'content' keys")
        
        # Create a copy to avoid reference issues
        message_copy = message.copy()
        
        # Add timestamp and ID if not present
        if 'timestamp' not in message_copy:
            message_copy['timestamp'] = datetime.now().isoformat()
        
        if 'id' not in message_copy:
            message_copy['id'] = str(uuid.uuid4())
        
        # Add to messages list, maintaining max size
        self._messages.append(message_copy)
        
        # Remove oldest messages if we exceed max_messages
        if len(self._messages) > self.max_messages:
            self._messages = self._messages[-self.max_messages:]
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages in memory.
        
        Returns:
            List of message dictionaries
        """
        return self._messages
    
    def get_message_by_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific message by ID.
        
        Args:
            message_id: ID of the message to retrieve
            
        Returns:
            The message dictionary if found, None otherwise
        """
        for message in self._messages:
            if message.get('id') == message_id:
                return message
        
        return None
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search messages for the given query.
        
        Args:
            query: Search query string
            
        Returns:
            List of message dictionaries that match the query
        """
        # For this simple implementation, we'll do case-insensitive substring search
        query = query.lower()
        results = []
        
        for message in self._messages:
            content = message.get('content', '').lower()
            
            # Check if query is in content
            if query in content:
                # Calculate basic relevance score based on match position and length
                # Earlier matches and higher percentage matches are more relevant
                position = content.find(query)
                length_ratio = len(query) / max(len(content), 1)
                
                # Simple relevance formula: higher is better
                # Normalize to range 0.0-1.0
                relevance = 0.5 + (1.0 - position / max(len(content), 1)) * 0.25 + length_ratio * 0.25
                
                # Add result with relevance score
                result = message.copy()
                result['relevance'] = relevance
                results.append(result)
        
        # Sort by relevance (highest first)
        results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        return results
    
    def clear(self) -> None:
        """Clear all messages from memory."""
        self._messages = []
    
    def get_user_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages with role 'user'.
        
        Returns:
            List of user message dictionaries
        """
        return [m for m in self._messages if m.get('role') == 'user']
    
    def get_assistant_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages with role 'assistant'.
        
        Returns:
            List of assistant message dictionaries
        """
        return [m for m in self._messages if m.get('role') == 'assistant']
        
    def get_last_n_messages(self, n: int) -> List[Dict[str, Any]]:
        """
        Get the last N messages.
        
        Args:
            n: Number of messages to retrieve
            
        Returns:
            List of the most recent n message dictionaries
        """
        return self._messages[-n:] if n > 0 else []
    
    def __len__(self) -> int:
        """
        Get number of messages in memory.
        
        Returns:
            Number of messages
        """
        return len(self._messages) 