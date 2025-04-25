"""
Utility to check API connectivity with Anthropic API.
"""

import sys
from rich.console import Console
from anthropic import Anthropic

from src.utils.config import config

console = Console()

def check_anthropic_api():
    """
    Check connection to Anthropic API.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    console.print("[bold cyan]Checking Anthropic API connection...[/bold cyan]")
    
    if not config.ANTHROPIC_API_KEY:
        console.print("[bold red]Error: ANTHROPIC_API_KEY is not set in .env file[/bold red]")
        return False
    
    try:
        client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
        # Make a simple API call to verify connectivity
        response = client.messages.create(
            model=config.MODEL,
            max_tokens=10,
            temperature=0,
            messages=[
                {"role": "user", "content": "Hello, are you working?"}
            ]
        )
        
        console.print(f"[bold green]Successfully connected to Anthropic API using model: {config.MODEL}[/bold green]")
        console.print(f"Response preview: {response.content[0].text[:50]}...")
        return True
    
    except Exception as e:
        console.print(f"[bold red]Error connecting to Anthropic API: {str(e)}[/bold red]")
        return False

if __name__ == "__main__":
    success = check_anthropic_api()
    sys.exit(0 if success else 1) 