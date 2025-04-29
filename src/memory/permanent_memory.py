"""
Permanent Memory System

This module provides a long-term memory system for storing and retrieving knowledge extracted
from conversations.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import uuid


class PermanentMemory:
    """
    A memory system for long-term knowledge storage.
    
    Permanent Memory stores extracted knowledge and insights beyond the scope of
    temporary memory, providing:
    - Categorized knowledge storage
    - Vector search across knowledge entries
    - Persistence between conversations
    """
    
    def __init__(self, storage_path: str = "memory/permanent"):
        """
        Initialize permanent memory system.
        
        Args:
            storage_path: Directory path for storing memory files (defaults to "memory/permanent")
        """
        self.storage_path = storage_path
        self._knowledge_entries = []
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Categories for organizing knowledge
        self.categories = [
            "concept",         # Abstract ideas or principles
            "fact",            # Verifiable pieces of information
            "personal",        # User-specific information
            "procedure",       # Step-by-step processes
            "preference",      # User preferences and opinions
            "reference",       # External sources and citations
        ]
    
    def add_knowledge(self, knowledge: Union[Dict[str, Any], List[Dict[str, Any]]]) -> None:
        """
        Add knowledge entries to permanent memory.
        
        Args:
            knowledge: Dictionary or list of dictionaries with knowledge entries
        """
        if isinstance(knowledge, dict):
            knowledge = [knowledge]
            
        for entry in knowledge:
            # Validate entry has required fields
            if not isinstance(entry, dict) or 'content' not in entry:
                raise ValueError("Knowledge entry must be a dictionary with 'content' key")
            
            # Create a copy to avoid reference issues
            entry_copy = entry.copy()
            
            # Set defaults for optional fields
            if 'id' not in entry_copy:
                entry_copy['id'] = str(uuid.uuid4())
                
            if 'timestamp' not in entry_copy:
                entry_copy['timestamp'] = datetime.now().isoformat()
                
            if 'category' not in entry_copy:
                entry_copy['category'] = "fact"  # Default category
            
            # Add source field if not present
            if 'source' not in entry_copy:
                entry_copy['source'] = "unknown"
                
            # Add relevance if not present (default to medium)
            if 'relevance' not in entry_copy:
                entry_copy['relevance'] = 0.5
                
            # Add to knowledge entries
            self._knowledge_entries.append(entry_copy)
    
    def get_all_knowledge(self) -> List[Dict[str, Any]]:
        """
        Get all knowledge entries.
        
        Returns:
            List of all knowledge entries
        """
        return self._knowledge_entries
    
    def get_knowledge_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get knowledge entries by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of knowledge entries in the specified category
        """
        if category not in self.categories:
            raise ValueError(f"Invalid category: {category}. Must be one of {self.categories}")
            
        return [entry for entry in self._knowledge_entries if entry.get('category') == category]
    
    def get_knowledge_by_id(self, knowledge_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific knowledge entry by ID.
        
        Args:
            knowledge_id: ID of the knowledge entry to retrieve
            
        Returns:
            The knowledge entry dictionary if found, None otherwise
        """
        for entry in self._knowledge_entries:
            if entry.get('id') == knowledge_id:
                return entry
        
        return None
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search knowledge entries for the given query.
        
        Args:
            query: Search query string
            top_k: Maximum number of results to return
            
        Returns:
            List of knowledge entries that match the query
        """
        # For this simple implementation, use substring matching
        query = query.lower()
        results = []
        
        for entry in self._knowledge_entries:
            content = entry.get('content', '').lower()
            
            # Check if query is in content
            if query in content:
                # Calculate basic relevance score based on match position and length
                position = content.find(query)
                length_ratio = len(query) / max(len(content), 1)
                
                # Simple relevance formula: higher is better
                # Normalize position to 0.0-1.0
                relevance = 0.5 + (1.0 - position / max(len(content), 1)) * 0.25 + length_ratio * 0.25
                
                # Include original relevance if present
                original_relevance = entry.get('relevance', 0.5)
                combined_relevance = (relevance + original_relevance) / 2
                
                # Add result with relevance score
                result = entry.copy()
                result['search_relevance'] = combined_relevance
                results.append(result)
        
        # Sort by relevance (highest first)
        results.sort(key=lambda x: x.get('search_relevance', 0), reverse=True)
        
        # Return top_k results
        return results[:top_k]
    
    def save(self, filename: str = "memory.json") -> str:
        """
        Save memory to a file.
        
        Args:
            filename: Name of the file to save to
            
        Returns:
            Full path to the saved file
        """
        filepath = os.path.join(self.storage_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump({
                'knowledge_entries': self._knowledge_entries,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'entry_count': len(self._knowledge_entries)
                }
            }, f, indent=2)
            
        return filepath
    
    def load(self, filename: str = "memory.json") -> bool:
        """
        Load memory from a file.
        
        Args:
            filename: Name of the file to load from
            
        Returns:
            True if successful, False otherwise
        """
        filepath = os.path.join(self.storage_path, filename)
        
        if not os.path.exists(filepath):
            return False
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            if 'knowledge_entries' in data:
                self._knowledge_entries = data['knowledge_entries']
                return True
                
        except (json.JSONDecodeError, IOError):
            return False
            
        return False
    
    def clear(self) -> None:
        """Clear all knowledge entries."""
        self._knowledge_entries = []
        
    def delete_entry(self, entry_id: str) -> bool:
        """
        Delete a knowledge entry by ID.
        
        Args:
            entry_id: ID of the entry to delete
            
        Returns:
            True if entry was found and deleted, False otherwise
        """
        for i, entry in enumerate(self._knowledge_entries):
            if entry.get('id') == entry_id:
                del self._knowledge_entries[i]
                return True
                
        return False
        
    def __len__(self) -> int:
        """
        Get number of knowledge entries in memory.
        
        Returns:
            Number of knowledge entries
        """
        return len(self._knowledge_entries) 