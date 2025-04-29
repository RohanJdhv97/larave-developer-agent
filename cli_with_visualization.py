"""
Enhanced CLI with Memory Visualization and Token Cost Tracking

This script extends the original CLI with additional features:
- Memory utilization visualization
- Token usage tracking with dollar cost estimates
- Memory extraction and reuse statistics
- Permanent memory utilization reporting

Run this instead of the regular 'python -m src.cli.main interactive' command.
"""

import os
import sys
import time
import json
import atexit
from typing import Optional, Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table
from rich.status import Status
from rich import print as rprint

from src.agent.langchain_integration import LaravelDeveloperAgent, create_anthropic_client
from src.utils.config import config
from src.memory.memory_visualization import MemoryVisualization
from src.cli.memory_ui import MemoryUI

# Constants
MEMORY_FILE = "agent_memory.json"
PROJECT_CONTEXT_FILE = "project_context.json"
TOKEN_COST_PER_1K = 0.03  # $0.03 per 1K tokens for Claude 3 Sonnet

# Initialize console and UI components
console = Console()
memory_ui = MemoryUI(console=console)
memory_visualizer = MemoryVisualization(enable_logging=True)

# Initialize empty agent
agent = None

def initialize_agent(use_visual_memory: bool = True):
    """Initialize the agent with memory visualization enabled."""
    global agent
    if agent is None:
        with Status("[bold blue]Initializing Laravel Developer Agent...[/bold blue]", spinner="dots12") as status:
            # Initialize with the visual memory system
            agent = LaravelDeveloperAgent(use_visual_memory=use_visual_memory)
            
            # Try to load saved memory if it exists
            if os.path.exists(MEMORY_FILE):
                try:
                    status.update("[bold blue]Loading conversation history...[/bold blue]")
                    agent.memory = agent.memory.__class__.load(MEMORY_FILE)
                    console.print(f"[bold green]Loaded previous conversation history[/bold green]")
                except Exception as e:
                    console.print(f"[bold yellow]Could not load previous memory: {str(e)}[/bold yellow]")

def save_memory_on_exit():
    """Save agent memory when the program exits."""
    global agent
    if agent is not None:
        try:
            with Status("[bold blue]Saving conversation memory...[/bold blue]", spinner="dots") as status:
                agent.save_state(memory_path=MEMORY_FILE, context_path=PROJECT_CONTEXT_FILE)
                console.print(f"[bold green]Saved conversation memory to {MEMORY_FILE}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error saving memory: {str(e)}[/bold red]")

# Register the exit handler
atexit.register(save_memory_on_exit)

def display_usage_and_memory_stats(query: str, response: str, duration_ms: float):
    """
    Display usage statistics, token costs, and memory visualization data.
    
    Args:
        query: The user's query
        response: The agent's response
        duration_ms: Time taken to process the query in milliseconds
    """
    # Estimate token usage (very rough calculation)
    # Claude 3 Sonnet uses cl100k tokenizer with ~0.7 tokens per word
    words_in_query = len(query.split())
    words_in_response = len(response.split())
    
    prompt_tokens = int(words_in_query * 1.3)  # Add buffer for system instructions
    completion_tokens = int(words_in_response * 1.3)
    total_tokens = prompt_tokens + completion_tokens
    
    # Calculate cost
    cost = (total_tokens / 1000) * TOKEN_COST_PER_1K
    
    # Get memory statistics
    stats = memory_visualizer.get_statistics()
    operations_by_type = stats.get('operations', {}).get('by_type', {})
    search_count = operations_by_type.get('search', 0)
    retrieval_count = operations_by_type.get('retrieval', 0)
    
    # Check if permanent memory was used
    permanent_used = "No"
    if retrieval_count > 0:
        permanent_used = "Yes"
    
    # Format the duration
    duration_str = f"{duration_ms:.2f}" if duration_ms is not None else "N/A"
    
    # Create memory stats panel
    memory_stats = [
        f"🔢 [bold cyan]Token Usage:[/bold cyan]",
        f"   • Prompt Tokens: [bold]{prompt_tokens}[/bold]",
        f"   • Completion Tokens: [bold]{completion_tokens}[/bold]",
        f"   • Total Tokens: [bold]{total_tokens}[/bold]",
        f"   • Estimated Cost: [bold]${cost:.6f}[/bold]",
        f"",
        f"🧠 [bold magenta]Memory Usage:[/bold magenta]",
        f"   • Memory Searches: [bold]{search_count}[/bold]",
        f"   • Memory Retrievals: [bold]{retrieval_count}[/bold]",
        f"   • Permanent Memory Used: [bold]{permanent_used}[/bold]",
        f"",
        f"⏱️ [bold yellow]Performance:[/bold yellow]",
        f"   • Query Processing Time: [bold]{duration_str}ms[/bold]",
    ]
    
    # Display the memory stats panel
    console.print("\n")
    console.print(Panel("\n".join(memory_stats), 
                         title="[bold green]Memory & Token Usage Report[/bold green]", 
                         border_style="green"))

def process_query(query: str) -> tuple:
    """
    Process a user query through the agent with measurements.
    
    Args:
        query: The user query
        
    Returns:
        Tuple of (response text, duration in ms)
    """
    start_time = time.time()
    response = agent.query_simple(query)
    duration_ms = (time.time() - start_time) * 1000
    return response, duration_ms

def interactive_with_visualization():
    """Run interactive mode with memory visualization."""
    # Initialize agent
    initialize_agent(use_visual_memory=True)
    
    console.print(Panel.fit(
        "[bold purple]Laravel Developer Agent with Memory Visualization[/bold purple]\n\n"
        "Your AI assistant for Laravel, FilamentPHP, and PestPHP development.\n\n"
        "[bold cyan]Features:[/bold cyan]\n"
        "• PSR-12 compliant code generation\n"
        "• PHP 8.2+ features and best practices\n"
        "• SOLID principles implementation\n"
        "• Laravel ecosystem expertise\n"
        "• Database schema design\n"
        "• [bold green]Memory visualization and token tracking[/bold green]\n\n"
        "[bold yellow]Commands:[/bold yellow]\n"
        "• Type your Laravel questions directly\n"
        "• Type 'exit' or 'quit' to end the session\n"
        "• Type '!simple' to toggle between memory and simple mode\n"
        "• Type '!stats' to show detailed memory statistics",
        title="Welcome",
        subtitle=f"Using {config.MODEL} | Temperature: {config.TEMPERATURE}",
        border_style="purple"
    ))
    
    # Default to memory mode
    use_simple_mode = False
    console.print(f"\n[bold blue]Starting in Memory Mode[/bold blue] - Type '!simple' to toggle modes")
    
    while True:
        # Show the current mode and memory state
        mode_indicator = "[Simple Mode]" if use_simple_mode else "[Memory Mode]"
        user_input = Prompt.ask(f"\n[bold blue]{mode_indicator} Your Laravel question[/bold blue]")
        
        # Handle special commands
        if user_input.lower() in ["exit", "quit"]:
            # Save memory before exiting
            try:
                with Status("[bold blue]Saving conversation memory...[/bold blue]", spinner="dots") as status:
                    agent.save_state(memory_path=MEMORY_FILE, context_path=PROJECT_CONTEXT_FILE)
                    console.print(f"[bold green]Conversation saved to {MEMORY_FILE}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error saving conversation: {str(e)}[/bold red]")
                
            console.print("[bold]Thank you for using Laravel Developer Agent. Goodbye![/bold]")
            break
            
        elif user_input.lower() == "!simple":
            use_simple_mode = not use_simple_mode
            console.print(f"[bold cyan]Switched to {'simple' if use_simple_mode else 'memory'} mode[/bold cyan]")
            continue
            
        elif user_input.lower() == "!stats":
            # Show detailed memory statistics
            stats = memory_visualizer.get_statistics()
            console.print(Panel(json.dumps(stats, indent=2), title="Detailed Memory Statistics", border_style="cyan"))
            continue
            
        # Log the operation start
        operation_id = memory_visualizer.log_operation(
            operation_type="query",
            query=user_input,
            params={"mode": "simple" if use_simple_mode else "memory"},
            summary=f"User query: {user_input[:50]}..."
        )
        
        try:
            # Show memory thinking animation
            memory_ui.memory_thinking("Processing your query...")
            memory_ui.show_memory_usage("search", "temporary")
            
            # Process the query with timing measurement
            response, duration_ms = process_query(user_input)
            
            # Show memory access indicators
            memory_ui.show_memory_usage("retrieval", "permanent")
            
            # Display the response
            console.print(Panel(Markdown(response), title="Laravel Agent Response", border_style="green"))
            
            # Update operation with results and duration
            memory_visualizer.log_operation(
                operation_type="response",
                query=user_input,
                results={"response_length": len(response)},
                duration_ms=duration_ms,
                summary=f"Response generated ({len(response)} chars)"
            )
            
            # Show usage and memory stats - directly passing duration instead of operation id
            display_usage_and_memory_stats(user_input, response, duration_ms)
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            console.print(f"[bold yellow]Traceback:[/bold yellow]")
            import traceback
            console.print(traceback.format_exc())

if __name__ == "__main__":
    interactive_with_visualization() 