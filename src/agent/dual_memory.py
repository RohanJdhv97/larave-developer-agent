"""
Dual Memory System for the Laravel Developer Agent.

This module implements a sophisticated dual memory system with:
1. Temporary memory for capturing current conversation context
2. Permanent memory for storing refined, high-quality knowledge
"""

from typing import Dict, List, Any, Optional, Union, Tuple
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_anthropic import ChatAnthropic
import os
import json
import datetime
import uuid
import re
from pathlib import Path

from src.utils.config import config
from src.agent.memory import SimpleChatMessageHistory, LaravelAgentMemory
try:
    from src.cli.memory_ui import memory_ui
except ImportError:
    # Create a dummy UI if the real one is not available
    class DummyUI:
        def __getattr__(self, name):
            return lambda *args, **kwargs: None
    memory_ui = DummyUI()

class TemporaryMemory(BaseModel):
    """
    Temporary memory for capturing current conversation context.
    
    This class expands on the existing LaravelAgentMemory to capture additional
    information about the current session, including:
    - Complete conversation history
    - Intermediate reasoning steps and solution attempts
    - Code snippets and implementations
    - Error correction sequences
    """
    
    # Unique identifier for this session
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Base memory system using LaravelAgentMemory
    base_memory: LaravelAgentMemory = Field(default_factory=LaravelAgentMemory)
    
    # Additional context information about the session
    session_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Track solutions attempted in this conversation
    solution_attempts: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Track code snippets generated in this conversation
    code_snippets: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Track errors and corrections
    error_corrections: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Track the quality and relevance of interactions
    interaction_metrics: Dict[str, Any] = Field(default_factory=lambda: {
        "successful_solutions": 0,
        "failed_attempts": 0,
        "clarification_requests": 0,
        "corrections_applied": 0
    })
    
    def add_user_message(self, message: str):
        """Add a user message to memory."""
        self.base_memory.add_user_message(message)
        
        # Update session metadata
        self.session_metadata["last_user_message_time"] = datetime.datetime.now().isoformat()
        
        # Track clarification requests
        if self._is_clarification_request(message):
            self.interaction_metrics["clarification_requests"] += 1
    
    def add_ai_message(self, message: str):
        """Add an AI message to memory."""
        self.base_memory.add_ai_message(message)
        
        # Update session metadata
        self.session_metadata["last_ai_message_time"] = datetime.datetime.now().isoformat()
        
        # Extract code snippets from the message
        code_blocks = self._extract_code_blocks(message)
        if code_blocks:
            for code in code_blocks:
                self._add_code_snippet(code)
    
    def _extract_code_blocks(self, message: str) -> List[str]:
        """Extract code blocks from a message."""
        # Look for markdown code blocks: ```lang ... ```
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', message, re.DOTALL)
        return code_blocks
    
    def _is_clarification_request(self, message: str) -> bool:
        """Check if a message is a clarification request."""
        # Simple heuristic: check for question marks and clarification keywords
        has_question_mark = '?' in message
        clarification_keywords = ['what do you mean', 'clarify', 'explain', 'don\'t understand', 'confused']
        has_keywords = any(keyword in message.lower() for keyword in clarification_keywords)
        return has_question_mark and has_keywords
    
    def _add_code_snippet(self, code: str):
        """Add a code snippet to memory."""
        snippet = {
            "code": code,
            "language": self._detect_language(code),
            "timestamp": datetime.datetime.now().isoformat(),
            "context": self._get_recent_context()
        }
        self.code_snippets.append(snippet)
    
    def _detect_language(self, code: str) -> str:
        """Detect the programming language of a code snippet."""
        # Simple heuristic detection
        if "<?php" in code or "namespace App" in code:
            return "php"
        elif "<template" in code and "<script" in code:
            return "vue"
        elif "function" in code and "return" in code and "const" in code:
            return "javascript"
        elif "import React" in code or "export default" in code:
            return "javascript-react"
        elif "<x-" in code or "@section" in code or "@extends" in code:
            return "blade"
        else:
            return "unknown"
    
    def _get_recent_context(self) -> List[Dict[str, str]]:
        """Get the most recent conversation context."""
        messages = self.base_memory.chat_history.messages[-3:] if len(self.base_memory.chat_history.messages) > 0 else []
        context = []
        
        for msg in messages:
            msg_type = "user" if isinstance(msg, HumanMessage) else "ai"
            context.append({
                "type": msg_type,
                "content": msg.content[:200] + ("..." if len(msg.content) > 200 else "")
            })
            
        return context
    
    def record_solution_attempt(self, problem: str, solution: str, successful: bool = False):
        """
        Record an attempted solution to a problem.
        
        Args:
            problem: Description of the problem being solved
            solution: The solution that was attempted
            successful: Whether the solution was successful
        """
        attempt = {
            "problem": problem,
            "solution": solution,
            "successful": successful,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.solution_attempts.append(attempt)
        
        # Update metrics
        if successful:
            self.interaction_metrics["successful_solutions"] += 1
        else:
            self.interaction_metrics["failed_attempts"] += 1
    
    def record_error_correction(self, error: str, correction: str):
        """
        Record an error and its correction.
        
        Args:
            error: Description of the error
            correction: How the error was corrected
        """
        correction_record = {
            "error": error,
            "correction": correction,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.error_corrections.append(correction_record)
        self.interaction_metrics["corrections_applied"] += 1
    
    def get_conversation_history(self) -> List[BaseMessage]:
        """Get the full conversation history."""
        return self.base_memory.chat_history.messages
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """
        Get all memory variables for use in prompt context.
        
        Returns:
            Dict containing chat_history, chat_summary, project_context, and session data
        """
        # Get base memory variables
        memory_vars = self.base_memory.get_memory_variables()
        
        # Add session-specific data
        memory_vars.update({
            "session_id": self.session_id,
            "session_metadata": self.session_metadata,
            "interaction_metrics": self.interaction_metrics
        })
        
        return memory_vars
    
    def clear(self):
        """Clear temporary memory."""
        self.base_memory.clear_buffer()
        self.solution_attempts = []
        self.code_snippets = []
        self.error_corrections = []
        self.interaction_metrics = {
            "successful_solutions": 0,
            "failed_attempts": 0,
            "clarification_requests": 0,
            "corrections_applied": 0
        }
    
    def save(self, path: str):
        """
        Save temporary memory to disk.
        
        Args:
            path: Directory path where to save the memory
        """
        # Create the session file path
        session_file = os.path.join(path, f"session_{self.session_id}.json")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(session_file)), exist_ok=True)
        
        # Prepare serializable data
        memory_data = {
            "session_id": self.session_id,
            "session_metadata": self.session_metadata,
            "solution_attempts": self.solution_attempts,
            "code_snippets": self.code_snippets,
            "error_corrections": self.error_corrections,
            "interaction_metrics": self.interaction_metrics,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Add chat history
        chat_history_data = []
        for message in self.base_memory.chat_history.messages:
            message_data = {
                "type": "human" if isinstance(message, HumanMessage) else "ai",
                "content": message.content
            }
            chat_history_data.append(message_data)
        
        memory_data["chat_history"] = chat_history_data
        
        # Save to file
        with open(session_file, "w") as f:
            json.dump(memory_data, f, indent=2)
            
        print(f"Temporary memory saved to {session_file}")
        
        # Also save the base memory
        base_memory_path = os.path.join(path, f"base_memory_{self.session_id}.json")
        self.base_memory.save(base_memory_path)
    
    @classmethod
    def load(cls, session_file: str) -> "TemporaryMemory":
        """
        Load temporary memory from disk.
        
        Args:
            session_file: Path to the session file
            
        Returns:
            TemporaryMemory: An instance with the loaded memory
        """
        if not os.path.exists(session_file):
            print(f"Session file {session_file} not found. Starting with fresh memory.")
            return cls()
            
        try:
            # Load data from session file
            with open(session_file, "r") as f:
                memory_data = json.load(f)
                
            # Create a new instance
            instance = cls(session_id=memory_data.get("session_id", str(uuid.uuid4())))
            
            # Load session metadata
            if "session_metadata" in memory_data:
                instance.session_metadata = memory_data["session_metadata"]
                
            # Load other components
            if "solution_attempts" in memory_data:
                instance.solution_attempts = memory_data["solution_attempts"]
                
            if "code_snippets" in memory_data:
                instance.code_snippets = memory_data["code_snippets"]
                
            if "error_corrections" in memory_data:
                instance.error_corrections = memory_data["error_corrections"]
                
            if "interaction_metrics" in memory_data:
                instance.interaction_metrics = memory_data["interaction_metrics"]
                
            # Load chat history
            if "chat_history" in memory_data:
                chat_history = memory_data["chat_history"]
                
                for message_data in chat_history:
                    msg_type = message_data.get("type", "unknown")
                    content = message_data.get("content", "")
                    
                    if msg_type == "human":
                        instance.add_user_message(content)
                    else:
                        instance.add_ai_message(content)
            
            print(f"Temporary memory loaded from {session_file}")
            return instance
            
        except Exception as e:
            print(f"Error loading temporary memory: {str(e)}")
            import traceback
            traceback.print_exc()
            return cls()


class KnowledgeEntry(BaseModel):
    """Model representing an entry in the permanent knowledge repository."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    source_type: str  # e.g., "conversation", "manual", "documentation"
    source_reference: Optional[str] = None  # e.g., session ID, documentation URL
    category: str  # Primary category
    subcategory: Optional[str] = None  # Optional subcategory
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)  # Additional metadata
    code_snippets: List[Dict[str, Any]] = Field(default_factory=list)
    related_entries: List[str] = Field(default_factory=list)  # IDs of related entries
    quality_score: float = 0.0  # Score representing the quality (0.0 to 1.0)
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    version: str = "1.0"  # Version of this knowledge entry


class PermanentMemory(BaseModel):
    """
    Permanent memory for storing refined, high-quality knowledge.
    
    This class implements a sophisticated repository for storing valuable
    knowledge extracted from conversations and other sources, organized
    by category and tagged for efficient retrieval.
    """
    
    # Dictionary of knowledge entries by ID
    entries: Dict[str, KnowledgeEntry] = Field(default_factory=dict)
    
    # Category hierarchy
    categories: Dict[str, List[str]] = Field(default_factory=dict)
    
    # Tag index for efficient retrieval
    tag_index: Dict[str, List[str]] = Field(default_factory=dict)
    
    # Storage path
    storage_path: str = Field(default="memory/permanent")
    
    def add_entry(self, title: str, content: str, category: str, 
                 source_type: str, tags: List[str] = None,
                 subcategory: Optional[str] = None,
                 source_reference: Optional[str] = None,
                 code_snippets: List[Dict[str, Any]] = None,
                 related_entries: List[str] = None,
                 quality_score: float = 0.5,
                 metadata: Dict[str, Any] = None) -> str:
        """
        Add a new knowledge entry to permanent memory.
        
        Args:
            title: Title of the knowledge entry
            content: Main content of the entry
            category: Primary category (e.g., "laravel", "filament", "testing")
            source_type: How this knowledge was acquired (e.g., "conversation", "documentation")
            tags: List of tags for easier searching
            subcategory: Optional subcategory for more detailed organization
            source_reference: Reference to source (e.g., session ID, documentation URL)
            code_snippets: List of code snippet objects
            related_entries: IDs of related knowledge entries
            quality_score: Score representing the quality (0.0 to 1.0)
            metadata: Additional metadata for the entry
            
        Returns:
            str: ID of the new knowledge entry
        """
        entry_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        entry = KnowledgeEntry(
            id=entry_id,
            title=title,
            content=content,
            source_type=source_type,
            source_reference=source_reference,
            category=category,
            subcategory=subcategory,
            tags=tags or [],
            metadata=metadata or {},
            code_snippets=code_snippets or [],
            related_entries=related_entries or [],
            quality_score=quality_score,
            created_at=now,
            updated_at=now
        )
        
        # Add to entries dictionary
        self.entries[entry_id] = entry
        
        # Update category hierarchy
        if category not in self.categories:
            self.categories[category] = []
        if subcategory and subcategory not in self.categories[category]:
            self.categories[category].append(subcategory)
        
        # Update tag index
        for tag in tags or []:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            self.tag_index[tag].append(entry_id)
        
        return entry_id
    
    def update_entry(self, entry_id: str, **kwargs) -> bool:
        """
        Update an existing knowledge entry.
        
        Args:
            entry_id: ID of the entry to update
            **kwargs: Fields to update
            
        Returns:
            bool: Whether the update was successful
        """
        if entry_id not in self.entries:
            return False
            
        entry = self.entries[entry_id]
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        
        # Always update the updated_at timestamp
        entry.updated_at = datetime.datetime.now().isoformat()
        
        # Special handling for tags (update tag index)
        if "tags" in kwargs:
            # Remove entry ID from old tags
            for tag in entry.tags:
                if tag in self.tag_index and entry_id in self.tag_index[tag]:
                    self.tag_index[tag].remove(entry_id)
            
            # Add entry ID to new tags
            for tag in kwargs["tags"]:
                if tag not in self.tag_index:
                    self.tag_index[tag] = []
                if entry_id not in self.tag_index[tag]:
                    self.tag_index[tag].append(entry_id)
        
        # Special handling for category/subcategory
        if "category" in kwargs or "subcategory" in kwargs:
            new_category = kwargs.get("category", entry.category)
            new_subcategory = kwargs.get("subcategory", entry.subcategory)
            
            # Update category hierarchy
            if new_category not in self.categories:
                self.categories[new_category] = []
            if new_subcategory and new_subcategory not in self.categories[new_category]:
                self.categories[new_category].append(new_subcategory)
        
        return True
    
    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """
        Get a knowledge entry by ID.
        
        Args:
            entry_id: ID of the entry to retrieve
            
        Returns:
            Optional[KnowledgeEntry]: The knowledge entry if found, None otherwise
        """
        return self.entries.get(entry_id)
    
    def delete_entry(self, entry_id: str) -> bool:
        """
        Delete a knowledge entry.
        
        Args:
            entry_id: ID of the entry to delete
            
        Returns:
            bool: Whether the deletion was successful
        """
        if entry_id not in self.entries:
            return False
            
        entry = self.entries[entry_id]
        
        # Remove from tag index
        for tag in entry.tags:
            if tag in self.tag_index and entry_id in self.tag_index[tag]:
                self.tag_index[tag].remove(entry_id)
        
        # Remove from entries dictionary
        del self.entries[entry_id]
        
        return True
    
    def search_by_tags(self, tags: List[str], match_all: bool = False) -> List[KnowledgeEntry]:
        """
        Search for knowledge entries by tags.
        
        Args:
            tags: List of tags to search for
            match_all: Whether all tags must match (AND) or any tag (OR)
            
        Returns:
            List[KnowledgeEntry]: List of matching knowledge entries
        """
        if not tags:
            return []
            
        # Get entry IDs for each tag
        tag_entry_ids = [self.tag_index.get(tag, []) for tag in tags]
        
        if not tag_entry_ids:
            return []
            
        # Combine based on match_all flag
        if match_all:
            # Set intersection of all tag entry IDs
            entry_ids = set(tag_entry_ids[0])
            for ids in tag_entry_ids[1:]:
                entry_ids &= set(ids)
        else:
            # Set union of all tag entry IDs
            entry_ids = set()
            for ids in tag_entry_ids:
                entry_ids |= set(ids)
        
        # Get entries for the matching IDs
        return [self.entries[entry_id] for entry_id in entry_ids if entry_id in self.entries]
    
    def search_by_category(self, category: str, subcategory: Optional[str] = None) -> List[KnowledgeEntry]:
        """
        Search for knowledge entries by category and optionally subcategory.
        
        Args:
            category: Category to search for
            subcategory: Optional subcategory to filter by
            
        Returns:
            List[KnowledgeEntry]: List of matching knowledge entries
        """
        results = []
        
        for entry in self.entries.values():
            if entry.category == category:
                if subcategory is None or entry.subcategory == subcategory:
                    results.append(entry)
                    
        return results
    
    def search_by_text(self, query: str) -> List[Tuple[KnowledgeEntry, float]]:
        """
        Search for knowledge entries by text content.
        
        Args:
            query: Text to search for
            
        Returns:
            List[Tuple[KnowledgeEntry, float]]: List of entries with relevance scores
        """
        # Simple text search implementation
        query = query.lower()
        results = []
        
        for entry in self.entries.values():
            score = 0.0
            
            # Check title (higher weight)
            if query in entry.title.lower():
                score += 0.5
                
            # Check content
            if query in entry.content.lower():
                score += 0.3
                
            # Check tags
            for tag in entry.tags:
                if query in tag.lower():
                    score += 0.2
                    break
            
            if score > 0:
                results.append((entry, score))
                
        # Sort by relevance score (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def get_related_entries(self, entry_id: str) -> List[KnowledgeEntry]:
        """
        Get entries related to a specific entry.
        
        Args:
            entry_id: ID of the entry to find related entries for
            
        Returns:
            List[KnowledgeEntry]: List of related knowledge entries
        """
        entry = self.get_entry(entry_id)
        if not entry:
            return []
            
        related_entries = []
        for related_id in entry.related_entries:
            related_entry = self.get_entry(related_id)
            if related_entry:
                related_entries.append(related_entry)
                
        return related_entries
    
    def add_relationship(self, source_id: str, target_id: str) -> bool:
        """
        Create a relationship between two knowledge entries.
        
        Args:
            source_id: ID of the source entry
            target_id: ID of the target entry
            
        Returns:
            bool: Whether the relationship was created successfully
        """
        if source_id not in self.entries or target_id not in self.entries:
            return False
            
        # Add relationship in both directions
        source_entry = self.entries[source_id]
        target_entry = self.entries[target_id]
        
        if target_id not in source_entry.related_entries:
            source_entry.related_entries.append(target_id)
            
        if source_id not in target_entry.related_entries:
            target_entry.related_entries.append(source_id)
            
        return True
    
    def remove_relationship(self, source_id: str, target_id: str) -> bool:
        """
        Remove a relationship between two knowledge entries.
        
        Args:
            source_id: ID of the source entry
            target_id: ID of the target entry
            
        Returns:
            bool: Whether the relationship was removed successfully
        """
        if source_id not in self.entries or target_id not in self.entries:
            return False
            
        # Remove relationship in both directions
        source_entry = self.entries[source_id]
        target_entry = self.entries[target_id]
        
        if target_id in source_entry.related_entries:
            source_entry.related_entries.remove(target_id)
            
        if source_id in target_entry.related_entries:
            target_entry.related_entries.remove(source_id)
            
        return True
    
    def get_categories(self) -> Dict[str, List[str]]:
        """
        Get the category hierarchy.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping categories to subcategories
        """
        return self.categories
    
    def get_all_tags(self) -> List[str]:
        """
        Get all tags in the knowledge base.
        
        Returns:
            List[str]: List of all tags
        """
        return list(self.tag_index.keys())
    
    def get_entries_by_source(self, source_type: str, source_reference: Optional[str] = None) -> List[KnowledgeEntry]:
        """
        Get entries by source type and optionally source reference.
        
        Args:
            source_type: Type of source (e.g., "conversation", "documentation")
            source_reference: Optional specific source reference
            
        Returns:
            List[KnowledgeEntry]: List of matching knowledge entries
        """
        results = []
        
        for entry in self.entries.values():
            if entry.source_type == source_type:
                if source_reference is None or entry.source_reference == source_reference:
                    results.append(entry)
                    
        return results
    
    def save(self, path: Optional[str] = None):
        """
        Save the permanent memory to disk.
        
        Args:
            path: Directory path where to save the memory (defaults to self.storage_path)
        """
        storage_path = path or self.storage_path
        
        # Ensure directory exists
        os.makedirs(storage_path, exist_ok=True)
        
        # Save entries
        entries_file = os.path.join(storage_path, "entries.json")
        entries_data = {}
        
        for entry_id, entry in self.entries.items():
            entries_data[entry_id] = entry.dict()
            
        with open(entries_file, "w") as f:
            json.dump(entries_data, f, indent=2)
            
        # Save category hierarchy
        categories_file = os.path.join(storage_path, "categories.json")
        with open(categories_file, "w") as f:
            json.dump(self.categories, f, indent=2)
            
        # Save tag index
        tag_index_file = os.path.join(storage_path, "tag_index.json")
        with open(tag_index_file, "w") as f:
            json.dump(self.tag_index, f, indent=2)
            
        print(f"Permanent memory saved to {storage_path}")
    
    @classmethod
    def load(cls, path: Optional[str] = None) -> "PermanentMemory":
        """
        Load permanent memory from disk.
        
        Args:
            path: Directory path to load the memory from
            
        Returns:
            PermanentMemory: An instance with the loaded memory
        """
        storage_path = path or "memory/permanent"
        
        if not os.path.exists(storage_path):
            print(f"Storage path {storage_path} not found. Starting with fresh memory.")
            return cls(storage_path=storage_path)
            
        try:
            # Create a new instance
            instance = cls(storage_path=storage_path)
            
            # Load entries
            entries_file = os.path.join(storage_path, "entries.json")
            if os.path.exists(entries_file):
                with open(entries_file, "r") as f:
                    entries_data = json.load(f)
                    
                for entry_id, entry_data in entries_data.items():
                    instance.entries[entry_id] = KnowledgeEntry(**entry_data)
            
            # Load category hierarchy
            categories_file = os.path.join(storage_path, "categories.json")
            if os.path.exists(categories_file):
                with open(categories_file, "r") as f:
                    instance.categories = json.load(f)
            
            # Load tag index
            tag_index_file = os.path.join(storage_path, "tag_index.json")
            if os.path.exists(tag_index_file):
                with open(tag_index_file, "r") as f:
                    instance.tag_index = json.load(f)
            
            print(f"Permanent memory loaded from {storage_path} with {len(instance.entries)} entries")
            return instance
            
        except Exception as e:
            print(f"Error loading permanent memory: {str(e)}")
            import traceback
            traceback.print_exc()
            return cls(storage_path=storage_path)


class MemoryAnalyzer(BaseModel):
    """
    Memory analyzer for extracting high-value information from temporary memory.
    
    This class implements sophisticated analysis mechanisms to identify valuable
    knowledge from conversations and other temporary memory, for preservation
    in the permanent memory repository.
    """
    
    # LLM for analysis
    llm: Any = None
    
    # Threshold for quality score
    quality_threshold: float = 0.7
    
    # Categories for knowledge classification
    default_categories: List[str] = Field(default_factory=lambda: [
        "laravel", "filament", "testing", "integration", "database", "frontend", "deployment"
    ])
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Initialize the LLM if not provided
        if self.llm is None:
            self.llm = ChatAnthropic(
                model=config.MODEL,
                temperature=0.3,  # Lower temperature for more consistent analysis
                max_tokens=2000,
                anthropic_api_key=config.ANTHROPIC_API_KEY
            )
    
    def analyze_temporary_memory(self, temp_memory: TemporaryMemory) -> List[Dict[str, Any]]:
        """
        Analyze temporary memory and extract valuable knowledge entries.
        
        Args:
            temp_memory: The temporary memory to analyze
            
        Returns:
            List[Dict[str, Any]]: List of extracted knowledge entries ready for permanent storage
        """
        extracted_knowledge = []
        
        # Analyze successful solution attempts
        successful_solutions = [attempt for attempt in temp_memory.solution_attempts 
                               if attempt.get("successful", False)]
        
        for solution in successful_solutions:
            knowledge = self._analyze_solution(solution, temp_memory)
            if knowledge:
                extracted_knowledge.append(knowledge)
        
        # Analyze code snippets
        for snippet in temp_memory.code_snippets:
            knowledge = self._analyze_code_snippet(snippet, temp_memory)
            if knowledge and knowledge["quality_score"] >= self.quality_threshold:
                extracted_knowledge.append(knowledge)
        
        # Analyze error corrections for valuable learning
        for correction in temp_memory.error_corrections:
            knowledge = self._analyze_error_correction(correction, temp_memory)
            if knowledge and knowledge["quality_score"] >= self.quality_threshold:
                extracted_knowledge.append(knowledge)
        
        # Analyze full conversation for conceptual knowledge
        conversation_knowledge = self._analyze_conversation(temp_memory)
        if conversation_knowledge:
            extracted_knowledge.extend(conversation_knowledge)
        
        return extracted_knowledge
    
    def _analyze_solution(self, solution: Dict[str, Any], temp_memory: TemporaryMemory) -> Optional[Dict[str, Any]]:
        """
        Analyze a successful solution for valuable knowledge.
        
        Args:
            solution: The solution attempt data
            temp_memory: The temporary memory for context
            
        Returns:
            Optional[Dict[str, Any]]: Knowledge entry data if valuable, None otherwise
        """
        # Skip if solution quality is low
        if not solution.get("successful", False):
            return None
        
        problem = solution.get("problem", "")
        solution_text = solution.get("solution", "")
        
        # Skip if either is empty
        if not problem or not solution_text:
            return None
        
        # Analyze the solution with LLM
        prompt = f"""
        Analyze this Laravel/PHP solution and extract its knowledge value:
        
        PROBLEM:
        {problem}
        
        SOLUTION:
        {solution_text}
        
        Evaluate the solution for:
        1. Reusability across different scenarios
        2. Demonstration of best practices
        3. Technical accuracy and efficiency
        4. Conceptual value for understanding Laravel/PHP
        
        Then determine:
        - A descriptive title for this knowledge
        - The primary category (laravel, filament, testing, database, etc.)
        - Any subcategory that applies
        - Relevant tags for searchability
        - A quality score (0.0 to 1.0) representing how valuable this knowledge is
        
        Format your response in JSON:
        {{
            "title": "Clear descriptive title",
            "content": "Refined, generalized version of the solution",
            "category": "primary_category",
            "subcategory": "subcategory",
            "tags": ["tag1", "tag2", "tag3"],
            "quality_score": 0.X,
            "include": true/false
        }}
        
        Only include high-quality, reusable knowledge (quality_score >= 0.7).
        Set "include" to false if this solution doesn't meet that threshold.
        """
        
        try:
            response = self.llm.invoke(prompt).content
            
            # Extract JSON
            json_match = re.search(r'({.*})', response, re.DOTALL)
            if not json_match:
                return None
                
            analysis = json.loads(json_match.group(1))
            
            # Check if worth including
            if not analysis.get("include", False) or analysis.get("quality_score", 0) < self.quality_threshold:
                return None
            
            # Create knowledge entry data
            knowledge = {
                "title": analysis.get("title", "Untitled Solution"),
                "content": analysis.get("content", solution_text),
                "category": analysis.get("category", "laravel"),
                "subcategory": analysis.get("subcategory"),
                "tags": analysis.get("tags", []),
                "quality_score": analysis.get("quality_score", 0.5),
                "source_type": "conversation",
                "source_reference": temp_memory.session_id,
                "metadata": {
                    "original_problem": problem,
                    "original_solution": solution_text,
                    "timestamp": solution.get("timestamp")
                }
            }
            
            return knowledge
            
        except Exception as e:
            print(f"Error analyzing solution: {str(e)}")
            return None
    
    def _analyze_code_snippet(self, snippet: Dict[str, Any], temp_memory: TemporaryMemory) -> Optional[Dict[str, Any]]:
        """
        Analyze a code snippet for valuable knowledge.
        
        Args:
            snippet: The code snippet data
            temp_memory: The temporary memory for context
            
        Returns:
            Optional[Dict[str, Any]]: Knowledge entry data if valuable, None otherwise
        """
        code = snippet.get("code", "")
        language = snippet.get("language", "unknown")
        context = snippet.get("context", [])
        
        # Skip if code is too short
        if len(code) < 30:
            return None
        
        # Convert context to text
        context_text = ""
        for ctx in context:
            context_text += f"{ctx.get('type', 'unknown')}: {ctx.get('content', '')}\n"
        
        # Analyze the code with LLM
        prompt = f"""
        Analyze this {language} code snippet in the context of Laravel/PHP development:
        
        CODE:
        ```{language}
        {code}
        ```
        
        CONTEXT:
        {context_text}
        
        Evaluate the code for:
        1. Reusability as a pattern or solution
        2. Demonstration of best practices
        3. Technical accuracy and efficiency
        4. Educational value
        
        Then determine:
        - A descriptive title for this code snippet
        - The primary category (laravel, filament, testing, database, etc.)
        - Any subcategory that applies
        - Relevant tags for searchability
        - A quality score (0.0 to 1.0) representing how valuable this code is
        
        Format your response in JSON:
        {{
            "title": "Clear descriptive title",
            "content": "Refined, commented version of the code with explanation",
            "category": "primary_category",
            "subcategory": "subcategory",
            "tags": ["tag1", "tag2", "tag3"],
            "quality_score": 0.X,
            "include": true/false
        }}
        
        Only include high-quality, reusable code (quality_score >= 0.7).
        Set "include" to false if this code doesn't meet that threshold.
        """
        
        try:
            response = self.llm.invoke(prompt).content
            
            # Extract JSON
            json_match = re.search(r'({.*})', response, re.DOTALL)
            if not json_match:
                return None
                
            analysis = json.loads(json_match.group(1))
            
            # Check if worth including
            if not analysis.get("include", False) or analysis.get("quality_score", 0) < self.quality_threshold:
                return None
            
            # Create knowledge entry data
            knowledge = {
                "title": analysis.get("title", f"Code Snippet: {language}"),
                "content": analysis.get("content", code),
                "category": analysis.get("category", "laravel"),
                "subcategory": analysis.get("subcategory"),
                "tags": analysis.get("tags", []),
                "quality_score": analysis.get("quality_score", 0.5),
                "source_type": "conversation",
                "source_reference": temp_memory.session_id,
                "code_snippets": [{
                    "code": code,
                    "language": language,
                    "context": context_text
                }],
                "metadata": {
                    "original_code": code,
                    "language": language,
                    "timestamp": snippet.get("timestamp")
                }
            }
            
            return knowledge
            
        except Exception as e:
            print(f"Error analyzing code snippet: {str(e)}")
            return None
    
    def _analyze_error_correction(self, correction: Dict[str, Any], temp_memory: TemporaryMemory) -> Optional[Dict[str, Any]]:
        """
        Analyze an error correction for valuable knowledge.
        
        Args:
            correction: The error correction data
            temp_memory: The temporary memory for context
            
        Returns:
            Optional[Dict[str, Any]]: Knowledge entry data if valuable, None otherwise
        """
        error = correction.get("error", "")
        correction_text = correction.get("correction", "")
        
        # Skip if either is empty
        if not error or not correction_text:
            return None
        
        # Analyze the correction with LLM
        prompt = f"""
        Analyze this error and correction in Laravel/PHP development:
        
        ERROR:
        {error}
        
        CORRECTION:
        {correction_text}
        
        Evaluate this error-correction pair for:
        1. Common mistake pattern that others might make
        2. Educational value in understanding Laravel/PHP
        3. Clarity of the correction approach
        4. Root cause insights
        
        Then determine:
        - A descriptive title for this error-correction pair
        - The primary category (laravel, filament, testing, database, etc.)
        - Any subcategory that applies
        - Relevant tags for searchability
        - A quality score (0.0 to 1.0) representing how valuable this knowledge is
        
        Format your response in JSON:
        {{
            "title": "Clear descriptive title",
            "content": "Explanation of the error, its causes, and how to fix it",
            "category": "primary_category",
            "subcategory": "subcategory",
            "tags": ["tag1", "tag2", "tag3"],
            "quality_score": 0.X,
            "include": true/false
        }}
        
        Only include high-quality, educational error corrections (quality_score >= 0.7).
        Set "include" to false if this error-correction doesn't meet that threshold.
        """
        
        try:
            response = self.llm.invoke(prompt).content
            
            # Extract JSON
            json_match = re.search(r'({.*})', response, re.DOTALL)
            if not json_match:
                return None
                
            analysis = json.loads(json_match.group(1))
            
            # Check if worth including
            if not analysis.get("include", False) or analysis.get("quality_score", 0) < self.quality_threshold:
                return None
            
            # Create knowledge entry data
            knowledge = {
                "title": analysis.get("title", "Error Correction"),
                "content": analysis.get("content", f"Error: {error}\n\nCorrection: {correction_text}"),
                "category": analysis.get("category", "laravel"),
                "subcategory": analysis.get("subcategory"),
                "tags": analysis.get("tags", []),
                "quality_score": analysis.get("quality_score", 0.5),
                "source_type": "error_correction",
                "source_reference": temp_memory.session_id,
                "metadata": {
                    "original_error": error,
                    "original_correction": correction_text,
                    "timestamp": correction.get("timestamp")
                }
            }
            
            return knowledge
            
        except Exception as e:
            print(f"Error analyzing error correction: {str(e)}")
            return None
    
    def _analyze_conversation(self, temp_memory: TemporaryMemory) -> List[Dict[str, Any]]:
        """
        Analyze the full conversation for conceptual knowledge.
        
        Args:
            temp_memory: The temporary memory with conversation history
            
        Returns:
            List[Dict[str, Any]]: List of extracted knowledge entries
        """
        messages = temp_memory.get_conversation_history()
        
        # Skip if conversation is too short
        if len(messages) < 4:  # Need at least 2 exchanges
            return []
        
        # Format conversation for analysis
        conversation_text = ""
        for i, msg in enumerate(messages):
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            # Truncate very long messages for the prompt
            content = msg.content[:1000] + ("..." if len(msg.content) > 1000 else "")
            conversation_text += f"{role}: {content}\n\n"
        
        # Analyze with LLM
        prompt = f"""
        Analyze this conversation about Laravel/PHP development and extract 1-3 valuable knowledge concepts:
        
        CONVERSATION:
        {conversation_text}
        
        Extract up to 3 distinct, valuable knowledge concepts from this conversation. 
        These should be generalizable lessons, patterns, or insights that would be useful 
        to remember for future Laravel/PHP development scenarios.
        
        For each concept, determine:
        - A descriptive title
        - A concise explanation of the concept
        - The primary category (laravel, filament, testing, database, etc.)
        - Any subcategory that applies
        - Relevant tags for searchability
        - A quality score (0.0 to 1.0) representing how valuable this knowledge is
        
        Format your response as an array of JSON objects:
        [
            {{
                "title": "Clear descriptive title for concept 1",
                "content": "Explanation of concept 1",
                "category": "primary_category",
                "subcategory": "subcategory",
                "tags": ["tag1", "tag2", "tag3"],
                "quality_score": 0.X,
                "include": true/false
            }},
            // ... additional concepts if found
        ]
        
        Only include high-quality concepts (quality_score >= 0.7).
        Set "include" to false for concepts that don't meet that threshold.
        If you don't find any valuable concepts, return an empty array.
        """
        
        try:
            response = self.llm.invoke(prompt).content
            
            # Extract JSON array
            json_match = re.search(r'(\[.*\])', response, re.DOTALL)
            if not json_match:
                return []
                
            concepts = json.loads(json_match.group(1))
            
            # Filter and convert to knowledge entries
            knowledge_entries = []
            for concept in concepts:
                # Skip if not worth including
                if not concept.get("include", False) or concept.get("quality_score", 0) < self.quality_threshold:
                    continue
                
                knowledge = {
                    "title": concept.get("title", "Untitled Concept"),
                    "content": concept.get("content", ""),
                    "category": concept.get("category", "laravel"),
                    "subcategory": concept.get("subcategory"),
                    "tags": concept.get("tags", []),
                    "quality_score": concept.get("quality_score", 0.5),
                    "source_type": "conversation_concept",
                    "source_reference": temp_memory.session_id,
                    "metadata": {
                        "conversation_length": len(messages),
                        "extraction_timestamp": datetime.datetime.now().isoformat()
                    }
                }
                
                knowledge_entries.append(knowledge)
            
            return knowledge_entries
            
        except Exception as e:
            print(f"Error analyzing conversation: {str(e)}")
            return []


class DualMemorySystem(BaseModel):
    """
    Dual Memory System integrating temporary and permanent memory.
    
    This class provides a unified interface for the dual memory system,
    managing both temporary session memory and permanent knowledge repository.
    """
    
    temporary_memory: TemporaryMemory = Field(default_factory=TemporaryMemory)
    permanent_memory: PermanentMemory = Field(default_factory=PermanentMemory)
    memory_analyzer: MemoryAnalyzer = Field(default_factory=MemoryAnalyzer)
    
    # Base storage path
    base_storage_path: str = Field(default="memory")
    
    # Auto-analyze frequency (number of messages)
    auto_analyze_frequency: int = 10
    message_counter: int = 0
    
    # Show visualization in CLI
    show_ui: bool = True
    
    def add_user_message(self, message: str):
        """Add a user message to temporary memory."""
        if self.show_ui:
            memory_ui.show_memory_usage("user message", "temporary")
            
        self.temporary_memory.add_user_message(message)
        self.message_counter += 1
        
        # Check if it's time for auto-analysis
        if self.message_counter >= self.auto_analyze_frequency:
            if self.show_ui:
                memory_ui.show_memory_transition(
                    "Temporary Memory", 
                    "Permanent Memory", 
                    f"Auto-analysis triggered after {self.auto_analyze_frequency} messages"
                )
            self.analyze_and_store()
            self.message_counter = 0
    
    def add_ai_message(self, message: str):
        """Add an AI message to temporary memory."""
        if self.show_ui:
            memory_ui.show_memory_usage("AI response", "temporary")
            
        self.temporary_memory.add_ai_message(message)
        self.message_counter += 1
    
    def record_solution_attempt(self, problem: str, solution: str, successful: bool = False):
        """Record a solution attempt in temporary memory."""
        if self.show_ui:
            status = "successful" if successful else "attempted"
            memory_ui.console.print(f"[bold blue]Recording {status} solution in temporary memory[/bold blue]")
            
        self.temporary_memory.record_solution_attempt(problem, solution, successful)
        
        # If successful, consider immediate analysis
        if successful:
            if self.show_ui:
                memory_ui.show_memory_transition(
                    "Temporary Memory", 
                    "Permanent Memory", 
                    "Successful solution identified for preservation"
                )
            self.analyze_solution(problem, solution)
    
    def record_error_correction(self, error: str, correction: str):
        """Record an error correction in temporary memory."""
        if self.show_ui:
            memory_ui.console.print(f"[bold blue]Recording error correction in temporary memory[/bold blue]")
            
        self.temporary_memory.record_error_correction(error, correction)
    
    def analyze_solution(self, problem: str, solution: str):
        """
        Analyze a single solution and store if valuable.
        
        Args:
            problem: Description of the problem
            solution: The solution that was applied
        """
        if self.show_ui:
            with memory_ui.console.status("[bold blue]Analyzing solution for knowledge value...[/bold blue]") as status:
                solution_data = {
                    "problem": problem,
                    "solution": solution,
                    "successful": True,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                
                knowledge = self.memory_analyzer._analyze_solution(solution_data, self.temporary_memory)
        else:
            solution_data = {
                "problem": problem,
                "solution": solution,
                "successful": True,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            knowledge = self.memory_analyzer._analyze_solution(solution_data, self.temporary_memory)
        
        if knowledge and knowledge.get("quality_score", 0) >= self.memory_analyzer.quality_threshold:
            # Add to permanent memory
            entry_id = self.permanent_memory.add_entry(
                title=knowledge.get("title", "Untitled Solution"),
                content=knowledge.get("content", solution),
                category=knowledge.get("category", "laravel"),
                subcategory=knowledge.get("subcategory"),
                source_type=knowledge.get("source_type", "conversation"),
                source_reference=knowledge.get("source_reference", self.temporary_memory.session_id),
                tags=knowledge.get("tags", []),
                quality_score=knowledge.get("quality_score", 0.5),
                metadata=knowledge.get("metadata", {})
            )
            
            if self.show_ui:
                memory_ui.console.print(f"[bold green]Added valuable solution to permanent memory:[/bold green] {knowledge.get('title')}")
                memory_ui.console.print(f"[dim]Quality score: {knowledge.get('quality_score', 0.5):.2f}[/dim]")
    
    def analyze_and_store(self):
        """
        Analyze temporary memory and store valuable knowledge in permanent memory.
        """
        if self.show_ui:
            memory_ui.analyzing_temporary_memory(with_progress=True)
        else:
            print("Analyzing temporary memory for valuable knowledge...")
        
        # Extract knowledge entries
        knowledge_entries = self.memory_analyzer.analyze_temporary_memory(self.temporary_memory)
        
        # Store in permanent memory
        stored_count = 0
        for knowledge in knowledge_entries:
            entry_id = self.permanent_memory.add_entry(
                title=knowledge.get("title", "Untitled Entry"),
                content=knowledge.get("content", ""),
                category=knowledge.get("category", "laravel"),
                subcategory=knowledge.get("subcategory"),
                source_type=knowledge.get("source_type", "conversation"),
                source_reference=knowledge.get("source_reference", self.temporary_memory.session_id),
                tags=knowledge.get("tags", []),
                code_snippets=knowledge.get("code_snippets", []),
                quality_score=knowledge.get("quality_score", 0.5),
                metadata=knowledge.get("metadata", {})
            )
            
            stored_count += 1
        
        if self.show_ui:
            memory_ui.show_storing_knowledge(stored_count, knowledge_entries)
            memory_ui.show_memory_completion()
        else:
            print(f"Stored {stored_count} valuable knowledge entries in permanent memory.")
    
    def search_knowledge(self, query: str, categories: List[str] = None, tags: List[str] = None) -> List[KnowledgeEntry]:
        """
        Search the permanent memory for relevant knowledge.
        
        Args:
            query: Text search query
            categories: Optional list of categories to filter by
            tags: Optional list of tags to filter by
            
        Returns:
            List[KnowledgeEntry]: List of relevant knowledge entries
        """
        if self.show_ui:
            with memory_ui.console.status(f"[bold green]Searching permanent memory: '{query}'[/bold green]") as status:
                # Start with text search
                search_results = self.permanent_memory.search_by_text(query)
                entries = [entry for entry, score in search_results]
                
                # Filter by categories if provided
                if categories:
                    entries = [entry for entry in entries if entry.category in categories]
                
                # Filter by tags if provided
                if tags:
                    tag_entries = self.permanent_memory.search_by_tags(tags, match_all=False)
                    # Get intersection
                    entries = [entry for entry in entries if entry in tag_entries]
            
            # Display search results
            memory_ui.show_search_results(entries, query)
        else:
            # Start with text search
            search_results = self.permanent_memory.search_by_text(query)
            entries = [entry for entry, score in search_results]
            
            # Filter by categories if provided
            if categories:
                entries = [entry for entry in entries if entry.category in categories]
            
            # Filter by tags if provided
            if tags:
                tag_entries = self.permanent_memory.search_by_tags(tags, match_all=False)
                # Get intersection
                entries = [entry for entry in entries if entry in tag_entries]
        
        return entries
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """
        Get memory variables for use in prompt context.
        
        Returns:
            Dict containing temporary memory variables and permanent memory stats
        """
        # Get temporary memory variables
        memory_vars = self.temporary_memory.get_memory_variables()
        
        # Add permanent memory stats
        memory_vars.update({
            "permanent_memory_stats": {
                "entry_count": len(self.permanent_memory.entries),
                "categories": list(self.permanent_memory.categories.keys()),
                "tag_count": len(self.permanent_memory.tag_index)
            }
        })
        
        if self.show_ui:
            memory_ui.memory_thinking("Accessing memory variables")
            # Show memory state
            temp_msg_count = len(self.temporary_memory.get_conversation_history())
            perm_entry_count = len(self.permanent_memory.entries)
            categories = list(self.permanent_memory.categories.keys())
            memory_ui.show_memory_state(temp_msg_count, perm_entry_count, categories)
        
        return memory_vars
    
    def clear_temporary_memory(self):
        """Clear temporary memory while preserving permanent memory."""
        if self.show_ui:
            memory_ui.console.print("[bold yellow]Clearing temporary memory[/bold yellow]")
            
        self.temporary_memory.clear()
        self.message_counter = 0
        
        if self.show_ui:
            memory_ui.console.print("[bold green]Temporary memory cleared[/bold green]")
    
    def save(self):
        """Save both temporary and permanent memory to disk."""
        # Create storage paths
        temp_path = os.path.join(self.base_storage_path, "temporary")
        perm_path = os.path.join(self.base_storage_path, "permanent")
        
        # Ensure directories exist
        os.makedirs(temp_path, exist_ok=True)
        os.makedirs(perm_path, exist_ok=True)
        
        if self.show_ui:
            with memory_ui.console.status("[bold blue]Saving memory system to disk...[/bold blue]") as status:
                # Save temporary memory
                self.temporary_memory.save(temp_path)
                
                # Save permanent memory
                self.permanent_memory.save(perm_path)
                
                # Save system metadata
                metadata = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "message_counter": self.message_counter,
                    "auto_analyze_frequency": self.auto_analyze_frequency,
                    "current_session_id": self.temporary_memory.session_id
                }
                
                metadata_file = os.path.join(self.base_storage_path, "dual_memory_metadata.json")
                with open(metadata_file, "w") as f:
                    json.dump(metadata, f, indent=2)
        else:
            # Save temporary memory
            self.temporary_memory.save(temp_path)
            
            # Save permanent memory
            self.permanent_memory.save(perm_path)
            
            # Save system metadata
            metadata = {
                "timestamp": datetime.datetime.now().isoformat(),
                "message_counter": self.message_counter,
                "auto_analyze_frequency": self.auto_analyze_frequency,
                "current_session_id": self.temporary_memory.session_id
            }
            
            metadata_file = os.path.join(self.base_storage_path, "dual_memory_metadata.json")
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)
        
        if self.show_ui:
            memory_ui.memory_saved(self.base_storage_path)
        else:
            print(f"Dual memory system saved to {self.base_storage_path}")
    
    @classmethod
    def load(cls, base_path: str = "memory", show_ui: bool = True) -> "DualMemorySystem":
        """
        Load dual memory system from disk.
        
        Args:
            base_path: Base directory path where the memory is stored
            show_ui: Whether to show the UI
            
        Returns:
            DualMemorySystem: An instance with the loaded memory
        """
        # Create storage paths
        temp_path = os.path.join(base_path, "temporary")
        perm_path = os.path.join(base_path, "permanent")
        
        if show_ui:
            with memory_ui.console.status(f"[bold blue]Loading memory system from {base_path}...[/bold blue]") as status:
                try:
                    # Create a new instance
                    instance = cls(base_storage_path=base_path, show_ui=show_ui)
                    
                    # Load permanent memory
                    instance.permanent_memory = PermanentMemory.load(perm_path)
                    
                    # Load system metadata to get current session
                    metadata_file = os.path.join(base_path, "dual_memory_metadata.json")
                    current_session_id = None
                    
                    if os.path.exists(metadata_file):
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                            
                        current_session_id = metadata.get("current_session_id")
                        instance.message_counter = metadata.get("message_counter", 0)
                        instance.auto_analyze_frequency = metadata.get("auto_analyze_frequency", 10)
                    
                    # Load temporary memory if session ID available
                    if current_session_id:
                        session_file = os.path.join(temp_path, f"session_{current_session_id}.json")
                        if os.path.exists(session_file):
                            instance.temporary_memory = TemporaryMemory.load(session_file)
                    
                    temp_entries = len(instance.temporary_memory.get_conversation_history())
                    perm_entries = len(instance.permanent_memory.entries)
                    
                    memory_ui.memory_loaded(base_path, temp_entries, perm_entries)
                    return instance
                    
                except Exception as e:
                    memory_ui.error(f"Error loading dual memory system: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    return cls(base_storage_path=base_path, show_ui=show_ui)
        else:
            try:
                # Create a new instance
                instance = cls(base_storage_path=base_path, show_ui=show_ui)
                
                # Load permanent memory
                instance.permanent_memory = PermanentMemory.load(perm_path)
                
                # Load system metadata to get current session
                metadata_file = os.path.join(base_path, "dual_memory_metadata.json")
                current_session_id = None
                
                if os.path.exists(metadata_file):
                    with open(metadata_file, "r") as f:
                        metadata = json.load(f)
                        
                    current_session_id = metadata.get("current_session_id")
                    instance.message_counter = metadata.get("message_counter", 0)
                    instance.auto_analyze_frequency = metadata.get("auto_analyze_frequency", 10)
                
                # Load temporary memory if session ID available
                if current_session_id:
                    session_file = os.path.join(temp_path, f"session_{current_session_id}.json")
                    if os.path.exists(session_file):
                        instance.temporary_memory = TemporaryMemory.load(session_file)
                
                print(f"Dual memory system loaded from {base_path}")
                return instance
                
            except Exception as e:
                print(f"Error loading dual memory system: {str(e)}")
                import traceback
                traceback.print_exc()
                return cls(base_storage_path=base_path, show_ui=show_ui)
    
    def show_conversation_summary(self):
        """Show a summary of the current conversation."""
        if self.show_ui:
            # Calculate some additional metrics
            total_messages = len(self.temporary_memory.get_conversation_history())
            code_snippets = len(self.temporary_memory.code_snippets)
            
            # Update metrics for display
            metrics = self.temporary_memory.interaction_metrics.copy()
            metrics["total_messages"] = total_messages
            metrics["code_snippets"] = code_snippets
            
            memory_ui.conversation_summary({"interaction_metrics": metrics})
