from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.utils.config import config

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