"""
Memory components for the Laravel Developer Agent.

This module implements various memory components using LangChain's memory modules
to help the agent retain context across interactions.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.memory import BaseMemory
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_anthropic import ChatAnthropic
import os
import json
import datetime

from src.utils.config import config

# Create a simple chat history class, since ChatMessageHistory may not be available
class SimpleChatMessageHistory(BaseModel):
    """A simple implementation of chat message history."""
    messages: List[BaseMessage] = Field(default_factory=list)
    
    def add_user_message(self, message: str) -> None:
        """Add a user message to the history."""
        self.messages.append(HumanMessage(content=message))
        
    def add_ai_message(self, message: str) -> None:
        """Add an AI message to the history."""
        self.messages.append(AIMessage(content=message))
        
    def clear(self) -> None:
        """Clear the message history."""
        self.messages = []

class LaravelAgentMemory(BaseModel):
    """
    Unified memory manager for the Laravel Developer Agent.
    
    This class manages different types of memory components:
    - Conversation buffer for recent interactions
    - Conversation summary for long-term context
    - Project context for Laravel project details
    """
    
    buffer_memory: ConversationBufferMemory = Field(default_factory=lambda: ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    ))
    
    summary_memory: ConversationSummaryMemory = Field(default=None)
    
    project_context: Dict[str, Any] = Field(default_factory=dict)
    
    # Add our own chat history as a backup
    chat_history: SimpleChatMessageHistory = Field(default_factory=SimpleChatMessageHistory)
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Initialize summary memory with the model
        if self.summary_memory is None:
            llm = ChatAnthropic(
                model=config.MODEL,
                temperature=0.3,  # Lower temperature for summaries
                max_tokens=1000,
                anthropic_api_key=config.ANTHROPIC_API_KEY
            )
            self.summary_memory = ConversationSummaryMemory(
                llm=llm,
                memory_key="chat_summary",
                return_messages=True
            )
    
    def add_user_message(self, message: str):
        """Add a user message to both buffer and summary memories."""
        # Use try/except in case buffer_memory.chat_memory doesn't work as expected
        try:
            self.buffer_memory.chat_memory.add_user_message(message)
        except (AttributeError, TypeError):
            pass  # In case the chat_memory doesn't have this method
            
        try:
            self.summary_memory.chat_memory.add_user_message(message)
        except (AttributeError, TypeError):
            pass
            
        # Always add to our backup history
        self.chat_history.add_user_message(message)
    
    def add_ai_message(self, message: str):
        """Add an AI message to both buffer and summary memories."""
        try:
            self.buffer_memory.chat_memory.add_ai_message(message)
        except (AttributeError, TypeError):
            pass
            
        try:
            self.summary_memory.chat_memory.add_ai_message(message)
        except (AttributeError, TypeError):
            pass
            
        # Always add to our backup history
        self.chat_history.add_ai_message(message)
    
    def get_buffer_history(self) -> List[BaseMessage]:
        """Get the recent conversation history from buffer memory."""
        try:
            return self.buffer_memory.chat_memory.messages
        except (AttributeError, TypeError):
            # Return our backup history if buffer memory fails
            return self.chat_history.messages
    
    def get_summary(self) -> str:
        """Get the conversation summary for long-term context."""
        try:
            return self.summary_memory.predict_new_summary(
                self.get_buffer_history(),
                ""  # Previous summary is tracked internally
            )
        except (AttributeError, TypeError):
            # If summary prediction fails, return a simple summary
            return f"Chat history with {len(self.chat_history.messages)} messages"
    
    def clear_buffer(self):
        """Clear the buffer memory while preserving the summary."""
        try:
            self.buffer_memory.chat_memory.clear()
        except (AttributeError, TypeError):
            pass
            
        # Always clear our backup history
        self.chat_history.clear()
    
    def save_project_context(self, key: str, value: Any):
        """Save information about the Laravel project being worked on."""
        self.project_context[key] = value
    
    def get_project_context(self, key: str) -> Optional[Any]:
        """Retrieve information about the Laravel project."""
        return self.project_context.get(key)
    
    def get_all_project_context(self) -> Dict[str, Any]:
        """Get all project context information."""
        return self.project_context
    
    def clear_project_context(self):
        """Clear all project context information."""
        self.project_context.clear()
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """
        Get all memory variables for use in prompt context.
        
        Returns:
            Dict containing chat_history, chat_summary, and project_context
        """
        return {
            "chat_history": self.get_buffer_history(),
            "chat_summary": self.get_summary(),
            "project_context": self.project_context
        }
    
    def save(self, path: str):
        """
        Save the memory state to disk.
        
        Args:
            path: Path where to save the memory
        """
        # Serialize chat history to a list of dicts
        chat_history_data = []
        for message in self.chat_history.messages:
            # Convert each message to a dict representation
            message_data = {
                "type": "human" if hasattr(message, "type") and message.type == "human" else "ai",
                "content": message.content
            }
            chat_history_data.append(message_data)
            
        # Prepare the data to save
        memory_data = {
            "chat_history": chat_history_data,
            "project_context": self.project_context,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        
        # Save to file
        with open(path, "w") as f:
            json.dump(memory_data, f, indent=2)
            
        print(f"Memory saved to {path}")
    
    @classmethod
    def load(cls, path: str) -> "LaravelAgentMemory":
        """
        Load memory state from disk.
        
        Args:
            path: Path to load memory from
            
        Returns:
            LaravelAgentMemory: An instance with the loaded memory
        """
        # Check if file exists
        if not os.path.exists(path):
            print(f"Memory file {path} not found. Starting with fresh memory.")
            return cls()
            
        try:
            # Load data from file
            with open(path, "r") as f:
                memory_data = json.load(f)
                
            print(f"DEBUG: Loaded memory file with keys: {list(memory_data.keys())}")
            
            # Create a new instance
            instance = cls()
            
            # Load project context
            if "project_context" in memory_data:
                instance.project_context = memory_data["project_context"]
                print(f"DEBUG: Loaded project context: {instance.project_context}")
                
            # Load chat history
            if "chat_history" in memory_data:
                chat_history = memory_data["chat_history"]
                print(f"DEBUG: Found {len(chat_history)} messages in chat history")
                
                for i, message_data in enumerate(chat_history):
                    msg_type = message_data.get("type", "unknown")
                    content = message_data.get("content", "")
                    
                    print(f"DEBUG: Loading message {i+1} - Type: {msg_type}, Content: {content[:30]}...")
                    
                    if msg_type == "human":
                        instance.add_user_message(content)
                    else:
                        instance.add_ai_message(content)
            
            # Verify loading
            print(f"DEBUG: After loading, chat history has {len(instance.chat_history.messages)} messages")
                        
            print(f"Memory loaded from {path} with {len(memory_data.get('chat_history', []))} messages")
            return instance
            
        except Exception as e:
            print(f"Error loading memory: {str(e)}")
            import traceback
            traceback.print_exc()
            return cls() 