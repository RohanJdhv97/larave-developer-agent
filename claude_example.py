import os
import sys
import argparse
import json
import requests
from typing import Dict, List, Optional, Union, Any
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Rich console for better output
console = Console()

class ClaudeLaravelAssistant:
    """
    A wrapper for Claude AI focused specifically on Laravel development.
    This assistant provides specialized help for Laravel, Filament, and related technologies.
    """
    
    def __init__(self):
        """Initialize the Claude Laravel Assistant with API key and configurations."""
        # Get API key from environment variable
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            console.print("[bold red]Error:[/bold red] ANTHROPIC_API_KEY not found in environment variables.")
            console.print("Please set your ANTHROPIC_API_KEY in a .env file or as an environment variable.")
            sys.exit(1)
            
        # Claude API endpoint
        self.api_url = "https://api.anthropic.com/v1/messages"
        
        # Default model - Claude 3 Opus for best performance, but can be configured
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Laravel-specific knowledge base and context
        self.laravel_context = """
        You are an expert Laravel developer with deep knowledge of:
        - Laravel framework and ecosystem
        - FilamentPHP admin panel builder
        - PestPHP testing framework
        - PHP 8.x features and best practices
        - Modern web development patterns
        
        Follow these guidelines when providing assistance:
        - Write concise, technical responses with accurate Laravel examples
        - Follow Laravel best practices and conventions
        - Use PHP 8.2+ features when appropriate
        - Follow PSR-12 coding standards
        - Use strict typing with declare(strict_types=1)
        - Utilize Laravel's built-in features and helpers
        - Follow SOLID principles and object-oriented programming
        - Implement proper error handling, validation, and security measures
        """
    
    def _send_message_to_claude(self, user_message: str) -> Dict[str, Any]:
        """
        Send a message to Claude API and get the response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The response from Claude API
        """
        # Per Anthropic documentation, the API key should be in x-api-key header
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Build messages array from conversation history
        messages = []
        for msg in self.conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        # Prepare the request data according to current Claude API standards
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4000,
            "system": self.laravel_context
        }
        
        try:
            console.print(f"Sending request to: {self.api_url}")
            console.print(f"Using model: {self.model}")
            
            response = requests.post(self.api_url, headers=headers, json=data)
            
            # Print detailed response information for debugging
            console.print(f"Response status code: {response.status_code}")
            
            # If we get an error, try to extract the error details
            if response.status_code != 200:
                try:
                    error_details = response.json()
                    console.print(f"Error details: {json.dumps(error_details, indent=2)}")
                except:
                    console.print(f"Response text: {response.text}")
                return None
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error:[/bold red] Failed to communicate with Claude API: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                console.print(f"Response status code: {e.response.status_code}")
                try:
                    error_details = e.response.json()
                    console.print(f"Error details: {json.dumps(error_details, indent=2)}")
                except:
                    console.print(f"Response text: {e.response.text}")
            return None
    
    def _update_conversation_history(self, user_message: str, assistant_response: str):
        """Update the conversation history with the latest exchange."""
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_response})
        
        # Keep conversation history to a reasonable size (last 10 messages)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def handle_laravel_query(self, query: str):
        """
        Process a Laravel-related query and display the response.
        
        Args:
            query: The user's Laravel-related question
        """
        # Enhance the query with Laravel-specific context if needed
        enhanced_query = f"{query}"
        
        console.print("\n[bold cyan]Sending your Laravel query to Claude...[/bold cyan]")
        response = self._send_message_to_claude(enhanced_query)
        
        if not response:
            console.print("[bold red]Error:[/bold red] No response received from Claude API.")
            return
            
        # Extract the assistant's response
        try:
            response_text = response.get("content", [])[0].get("text", "")
            
            # Update conversation history
            self._update_conversation_history(query, response_text)
            
            # Display the response as formatted markdown
            console.print("\n[bold green]Claude's Response:[/bold green]")
            console.print(Panel(Markdown(response_text), border_style="green"))
        except (KeyError, IndexError) as e:
            console.print(f"[bold red]Error:[/bold red] Failed to parse Claude response: {str(e)}")
            console.print(f"Response: {response}")
    
    def interactive_session(self):
        """Start an interactive session with the Laravel Assistant."""
        console.print(Panel.fit(
            "[bold purple]Laravel Assistant powered by Claude[/bold purple]\n"
            "Ask any questions related to Laravel, Filament, or PHP development.\n"
            "Type 'exit' or 'quit' to end the session.",
            title="Welcome",
            border_style="purple"
        ))
        
        while True:
            user_input = Prompt.ask("\n[bold blue]Your Laravel question[/bold blue]")
            
            if user_input.lower() in ["exit", "quit"]:
                console.print("[bold]Thank you for using Laravel Assistant. Goodbye![/bold]")
                break
                
            self.handle_laravel_query(user_input)

def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(description="Laravel Assistant powered by Claude")
    parser.add_argument("--query", "-q", help="Single query mode: ask a question and exit")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start an interactive session")
    args = parser.parse_args()
    
    # Create the assistant
    assistant = ClaudeLaravelAssistant()
    
    if args.query:
        # Single query mode
        assistant.handle_laravel_query(args.query)
    elif args.interactive or not sys.argv[1:]:
        # Interactive mode (default if no arguments provided)
        assistant.interactive_session()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
