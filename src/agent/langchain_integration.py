from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.utils.config import config
from src.agent.memory import LaravelAgentMemory
from src.agent.memory_adapter import DualMemoryAdapter
from src.agent.project_context import LaravelProjectContext
from src.agent.knowledge_base import load_knowledge_base

def create_anthropic_client():
    """
    Create and return an instance of the Anthropic chat model.
    
    Returns:
        ChatAnthropic: An instance of the Anthropic chat model
    """
    return ChatAnthropic(
        model=config.MODEL,
        temperature=config.TEMPERATURE,
        max_tokens=config.MAX_TOKENS,
        anthropic_api_key=config.ANTHROPIC_API_KEY
    )

def create_laravel_agent_prompt():
    """
    Create a prompt template for the Laravel Developer Agent.
    
    Returns:
        ChatPromptTemplate: A template for Laravel Developer Agent prompts
    """
    template = """You are an expert Laravel developer with deep knowledge of:
    - Laravel framework and ecosystem
    - FilamentPHP admin panel builder
    - PestPHP testing framework
    - PHP 8.x features and best practices
    - Modern web development patterns

    Provide your expertise to help with the following Laravel development task:
    
    {query}
    
    Follow these guidelines in your response:
    - Write concise, technical responses with accurate Laravel examples
    - Follow Laravel best practices and conventions
    - Use PHP 8.2+ features where appropriate
    - Follow PSR-12 coding standards
    - Use strict typing with declare(strict_types=1)
    - Utilize Laravel's built-in features and helpers
    - Follow SOLID principles and object-oriented programming
    - Implement proper error handling, validation, and security measures
    """
    
    return ChatPromptTemplate.from_template(template)

def create_laravel_chain():
    """
    Create a simple LangChain chain for the Laravel Developer Agent.
    
    This is maintained for backward compatibility, but new code should
    use the LangGraph workflow instead.
    
    Returns:
        Chain: A LangChain chain for Laravel development assistance
    """
    # Create model, prompt, and output parser
    model = create_anthropic_client()
    prompt = create_laravel_agent_prompt()
    output_parser = StrOutputParser()
    
    # Create and return the chain
    chain = (
        {"query": RunnablePassthrough()} 
        | prompt 
        | model 
        | output_parser
    )
    
    return chain

def test_laravel_chain(query: str):
    """
    Test the Laravel Developer Agent chain with a query.
    
    Args:
        query: The query to test with
        
    Returns:
        str: The response from the chain
    """
    chain = create_laravel_chain()
    return chain.invoke(query)

class LaravelDeveloperAgent:
    """
    Main agent class for Laravel development assistance.
    
    This class provides a unified interface to the agent's capabilities,
    managing memory, project context, and knowledge retrieval.
    """
    
    def __init__(self, use_visual_memory: bool = True):
        """
        Initialize the Laravel Developer Agent.
        
        Args:
            use_visual_memory: Whether to use the visual memory system with Rich UI
        """
        # Use either the visual dual memory system or the standard memory
        if use_visual_memory:
            self.memory = DualMemoryAdapter()
            print("Using visual dual memory system with Rich UI")
        else:
            self.memory = LaravelAgentMemory()
            print("Using standard memory system")
            
        self.project_context = LaravelProjectContext()
        self.knowledge_base = load_knowledge_base()
    
    def query(self, user_query: str) -> str:
        """
        Process a user query using the LangGraph workflow.
        
        Args:
            user_query: The user's Laravel development query
            
        Returns:
            str: The agent's response
        """
        # Temporarily use only the simple chain until we fix the workflow issue
        print("Using simple chain mode as a fallback")
        return self.query_simple(user_query)
    
    def query_simple(self, user_query: str) -> str:
        """
        Process a user query using the simple LangChain chain.
        
        This method is provided for backward compatibility and simpler queries
        that don't require the full reasoning workflow.
        
        Args:
            user_query: The user's Laravel development query
            
        Returns:
            str: The agent's response
        """
        # Use the simpler LangChain chain
        response = test_laravel_chain(user_query)
        
        # Update memory with the interaction
        self.memory.add_user_message(user_query)
        self.memory.add_ai_message(response)
        
        return response
    
    def get_memory_variables(self):
        """Get all memory variables for use in prompt context."""
        return self.memory.get_memory_variables()
    
    def get_project_context_summary(self):
        """Get a summary of the project context."""
        return self.project_context.get_context_summary()
    
    def update_project_context(self, **kwargs):
        """Update the project context with new information."""
        self.project_context.update_project_info(**kwargs)
    
    def save_state(self, memory_path="memory.json", context_path="project_context.json"):
        """
        Save the agent's state to disk.
        
        Args:
            memory_path: Path to save memory to
            context_path: Path to save project context to
        """
        self.memory.save(memory_path)
        self.project_context.save(context_path)
    
    def load_state(self, memory_path="memory.json", context_path="project_context.json"):
        """
        Load the agent's state from disk.
        
        Args:
            memory_path: Path to load memory from
            context_path: Path to load project context from
        """
        # TODO: Implement memory loading when available
        self.project_context = LaravelProjectContext.load(context_path) 