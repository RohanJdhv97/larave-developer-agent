import typer
import asyncio
import os
import atexit
import json
import time
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.status import Status
from rich import print as rprint

from src.agent.langchain_integration import test_laravel_chain, LaravelDeveloperAgent, create_anthropic_client
from src.utils.config import config
from src.agent.memory import LaravelAgentMemory

# Initialize typer app and rich console
app = typer.Typer(
    help="Laravel Developer Agent - AI assistant for Laravel development",
    add_completion=False
)
console = Console()

# This will be initialized during command execution
agent = None

# Default memory file path
MEMORY_FILE = "agent_memory.json"
PROJECT_CONTEXT_FILE = "project_context.json"

# Define processing stages for loading animations
PROCESSING_STAGES = [
    "Analyzing your request...",
    "Retrieving Laravel knowledge...",
    "Applying SOLID principles...",
    "Checking PSR-12 standards...",
    "Considering PHP 8.2+ features...",
    "Evaluating best practices...",
    "Crafting a detailed response...",
]

def initialize_agent():
    """Initialize the agent with memory loaded from disk if available."""
    global agent
    if agent is None:
        with Status("[bold blue]Initializing Laravel Developer Agent...[/bold blue]", spinner="dots12") as status:
            agent = LaravelDeveloperAgent()
            
            # Try to load saved memory if it exists
            if os.path.exists(MEMORY_FILE):
                try:
                    # Load memory directly instead of using load_state
                    status.update("[bold blue]Loading conversation history...[/bold blue]")
                    agent.memory = LaravelAgentMemory.load(MEMORY_FILE)
                    console.print(f"[bold green]Loaded previous conversation history with {len(agent.memory.chat_history.messages)} messages[/bold green]")
                except Exception as e:
                    console.print(f"[bold yellow]Could not load previous memory: {str(e)}[/bold yellow]")

# Save memory when the program exits
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

def animated_processing(query_text: str) -> None:
    """Display an animated processing indicator with stages."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.fields[status]}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[bold blue]Processing your Laravel query...", total=len(PROCESSING_STAGES), status="")
        
        # Show different processing stages
        for stage in PROCESSING_STAGES:
            progress.update(task, advance=1, status=stage)
            # Random delay between 0.5 and 1.5 seconds to simulate processing
            time.sleep(0.5 + (len(query_text) % 10) / 10)

@app.command()
def query(
    query_text: str = typer.Argument(..., help="The Laravel development query to process"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    simple: bool = typer.Option(False, "--simple", "-s", help="Use simple mode without the full reasoning workflow")
):
    """
    Process a single Laravel development query and display the result.
    """
    # Initialize agent with memory
    global agent
    initialize_agent()
        
    if verbose:
        console.print("[bold cyan]Processing query...[/bold cyan]")
        console.print(f"Model: {config.MODEL}")
        console.print(f"Temperature: {config.TEMPERATURE}")
    
    try:
        # Show animated processing indicator
        animated_processing(query_text)
        
        if simple:
            with Status("[bold magenta]Generating response with simple chain...[/bold magenta]", spinner="aesthetic") as status:
                # Use the simple chain for compatibility
                response = test_laravel_chain(query_text)
        else:
            with Status("[bold magenta]Generating comprehensive response...[/bold magenta]", spinner="point") as status:
                # Use the simple chain for now
                response = agent.query_simple(query_text)
        
        console.print(Panel(Markdown(response), title="Laravel Agent Response", border_style="green"))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@app.command()
def interactive(
    no_workflow: bool = typer.Option(False, "--no-workflow", help="Disable the workflow mode and use simple chain only")
):
    """
    Start an interactive session with the Laravel Developer Agent.
    """
    # Initialize agent with memory
    global agent
    initialize_agent()
        
    console.print(Panel.fit(
        "[bold purple]Laravel Developer Agent[/bold purple]\n\n"
        "Your AI assistant for Laravel, FilamentPHP, and PestPHP development.\n\n"
        "[bold cyan]Features:[/bold cyan]\n"
        "• PSR-12 compliant code generation\n"
        "• PHP 8.2+ features and best practices\n"
        "• SOLID principles implementation\n"
        "• Laravel ecosystem expertise\n"
        "• Database schema design\n\n"
        "[bold yellow]Commands:[/bold yellow]\n"
        "• Type your Laravel questions directly\n"
        "• Type 'exit' or 'quit' to end the session\n"
        "• Type '!help' to see all available commands",
        title="Welcome",
        subtitle=f"Using {config.MODEL} | Temperature: {config.TEMPERATURE}",
        border_style="purple"
    ))
    
    # Keep track of whether to use simple mode
    use_simple_mode = no_workflow
    
    # Show initial mode
    mode_name = "Simple Mode" if use_simple_mode else "Memory Mode"
    console.print(f"\n[bold blue]Starting in {mode_name}[/bold blue] - Type '!simple' to toggle modes")
    
    while True:
        # Show the current mode
        mode_indicator = "[Simple Mode]" if use_simple_mode else "[Memory Mode]"
        user_input = Prompt.ask(f"\n[bold blue]{mode_indicator} Your Laravel question[/bold blue]")
        
        # Handle special commands
        if user_input.lower() in ["exit", "quit"]:
            # Save memory before exiting
            try:
                # Save memory directly
                with Status("[bold blue]Saving conversation memory...[/bold blue]", spinner="dots") as status:
                    agent.memory.save(MEMORY_FILE)
                    console.print(f"[bold green]Conversation saved to {MEMORY_FILE}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error saving conversation: {str(e)}[/bold red]")
                
            console.print("[bold]Thank you for using Laravel Developer Agent. Goodbye![/bold]")
            break
        elif user_input.lower() == "!simple":
            use_simple_mode = not use_simple_mode
            console.print(f"[bold cyan]Switched to {'simple' if use_simple_mode else 'memory'} mode[/bold cyan]")
            continue
        elif user_input.lower() == "!context":
            with Status("[bold blue]Retrieving project context...[/bold blue]", spinner="moon") as status:
                show_project_context()
            continue
        elif user_input.lower() == "!memory":
            # Display the memory contents from agent.memory.chat_history directly
            with Status("[bold blue]Loading conversation history...[/bold blue]", spinner="clock") as status:
                try:
                    direct_history = agent.memory.chat_history.messages
                    if not direct_history:
                        console.print(Panel("No conversation history found.", title="Memory Contents", border_style="yellow"))
                    else:
                        # Create a table for the conversation
                        table = Table(title=f"Conversation History ({len(direct_history)} messages)")
                        table.add_column("Turn", style="dim")
                        table.add_column("Role", style="cyan")
                        table.add_column("Message", style="white")
                        
                        # Add conversation turns to the table
                        for i, msg in enumerate(direct_history):
                            # Determine the role based on message type
                            msg_type = type(msg).__name__
                            
                            if "Human" in msg_type:
                                role = "[bold blue]User"
                            elif "AI" in msg_type:
                                role = "[bold green]Agent"
                            else:
                                role = f"[bold yellow]{msg_type}"
                                
                            # Get the content
                            content = msg.content if hasattr(msg, 'content') else str(msg)
                            
                            # Add to the table
                            table.add_row(str(i+1), role, content)
                        
                        console.print(table)
                except Exception as e:
                    console.print(f"[bold red]Error displaying memory:[/bold red] {str(e)}")
            continue
        elif user_input.lower() == "!debug":
            try:
                # Run the debug_memory function
                console.print("[bold yellow]Running memory diagnostics...[/bold yellow]")
                with Status("[bold blue]Analyzing memory structure...[/bold blue]", spinner="pong") as status:
                    memory_vars = agent.get_memory_variables()
                    direct_history = agent.memory.chat_history.messages
                    
                    console.print(f"Memory variables keys: {list(memory_vars.keys())}")
                    console.print(f"Direct history length: {len(direct_history)}")
                    
                    # Show details of direct history
                    console.print("\n[bold]Direct Chat History[/bold]")
                    for i, msg in enumerate(direct_history):
                        console.print(f"Message {i+1}: {type(msg).__name__} - {str(msg)[:100]}...")
            except Exception as e:
                console.print(f"[bold red]Error during debug:[/bold red] {str(e)}")
            continue
        elif user_input.lower() == "!save":
            try:
                with Status("[bold blue]Saving agent memory state...[/bold blue]", spinner="bouncingBar") as status:
                    agent.memory.save(MEMORY_FILE)
                    console.print(f"[bold green]Agent memory saved to {MEMORY_FILE}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error saving memory: {str(e)}[/bold red]")
            continue
        elif user_input.lower() == "!load":
            try:
                with Status("[bold blue]Loading agent memory state...[/bold blue]", spinner="smiley") as status:
                    agent.memory = LaravelAgentMemory.load(MEMORY_FILE)
                    console.print(f"[bold green]Agent memory loaded from {MEMORY_FILE} with {len(agent.memory.chat_history.messages)} messages[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error loading memory: {str(e)}[/bold red]")
            continue
        elif user_input.lower() == "!reset":
            if Prompt.ask("[bold yellow]Reset all memory? This cannot be undone. (y/n)[/bold yellow]").lower() == 'y':
                # Create a fresh memory instance
                with Status("[bold red]Resetting agent memory...[/bold red]", spinner="runner") as status:
                    agent.memory = LaravelAgentMemory()
                    console.print("[bold red]Memory reset complete. All conversation history cleared.[/bold red]")
            continue
        elif user_input.lower() == "!help":
            show_help()
            continue
            
        try:
            # Show animated processing indicator
            animated_processing(user_input)
            
            if use_simple_mode:
                with Status("[bold magenta]Generating response using simple mode...[/bold magenta]", spinner="aesthetic") as status:
                    response = agent.query_simple(user_input)
            else:
                with Status("[bold magenta]Generating response with memory integration...[/bold magenta]", spinner="point") as status:
                    # For now, always use the simple chain to avoid workflow issues
                    response = agent.query_simple(user_input)
                
            console.print(Panel(Markdown(response), title="Laravel Agent Response", border_style="green"))
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

@app.command()
def show_context():
    """
    Display the current project context stored in the agent's memory.
    """
    # Initialize agent with memory
    global agent
    initialize_agent()
    show_project_context()

@app.command()
def show_memory():
    """
    Display the conversation history from the agent's memory.
    """
    # Initialize agent with memory
    global agent
    initialize_agent()
    show_memory_history()

def show_project_context():
    """Helper function to display project context in a formatted way."""
    global agent
    context = agent.get_project_context_summary()
    console.print(Panel(context, title="Project Context", border_style="blue"))

def show_memory_history():
    """Helper function to display conversation history from memory."""
    # Access the direct chat history from the agent's memory
    global agent
    try:
        console.print("[bold yellow]DEBUG: Accessing chat history[/bold yellow]")
        
        # Get direct chat history - this is more reliable than memory_vars
        direct_history = agent.memory.chat_history.messages
        console.print(f"[bold yellow]DEBUG: Found {len(direct_history)} messages in memory[/bold yellow]")
        
        # Get memory variables for comparison
        memory_vars = agent.get_memory_variables()
        chat_history = memory_vars.get('chat_history', [])
        console.print(f"[bold yellow]DEBUG: memory_vars has {len(chat_history)} messages[/bold yellow]")
        
        if not direct_history:
            console.print(Panel("No conversation history found.", title="Memory Contents", border_style="yellow"))
            return
        
        # Create a table for the conversation
        table = Table(title="Conversation History")
        table.add_column("Turn", style="dim")
        table.add_column("Role", style="cyan")
        table.add_column("Message", style="white")
        
        # Add conversation turns to the table
        for i, msg in enumerate(direct_history):
            # Determine the role based on message type
            msg_type = type(msg).__name__
            console.print(f"[bold yellow]DEBUG: Message {i+1} type: {msg_type}[/bold yellow]")
            
            if "Human" in msg_type:
                role = "[bold blue]User"
            elif "AI" in msg_type:
                role = "[bold green]Agent"
            else:
                role = f"[bold yellow]{msg_type}"
                
            # Get the content
            content = msg.content if hasattr(msg, 'content') else str(msg)
            
            # Add to the table
            table.add_row(str(i+1), role, content)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error displaying memory:[/bold red] {str(e)}")
        import traceback
        console.print(traceback.format_exc())
        console.print(Panel("Failed to retrieve conversation history.", title="Memory Contents", border_style="red"))

def show_help():
    """Display help information for interactive mode."""
    console.print(Panel.fit(
        "[bold purple]Laravel Developer Agent - Interactive Mode Help[/bold purple]\n"
        "This agent helps with Laravel, FilamentPHP, and PestPHP development tasks.",
        title="About",
        border_style="purple"
    ))
    
    table = Table(title="Available Commands", border_style="blue")
    table.add_column("Command", style="cyan", justify="left")
    table.add_column("Description", style="white")
    table.add_column("Example", style="green", justify="left")
    
    commands = [
        ("exit, quit", "Exit the interactive session and save conversation history", "exit"),
        ("!simple", "Toggle between simple mode (faster) and memory mode (more context-aware)", "!simple"),
        ("!context", "Display the current project context and configuration", "!context"),
        ("!memory", "Show the full conversation history stored in memory", "!memory"),
        ("!debug", "Display technical debug information about the memory system", "!debug"),
        ("!save", "Manually save the agent's memory and context to disk", "!save"),
        ("!load", "Load the agent's previously saved state from disk", "!load"),
        ("!reset", "Reset all memory and start a fresh conversation", "!reset"),
        ("!help", "Show this help message with available commands", "!help")
    ]
    
    for cmd, desc, example in commands:
        table.add_row(f"[bold]{cmd}[/bold]", desc, example)
    
    console.print(table)
    
    # Add a usage guide panel
    console.print(Panel(
        "To ask a question: Simply type your Laravel query and press Enter\n\n"
        "[bold]Example queries:[/bold]\n"
        "- How do I create a migration for a users table?\n"
        "- Generate a Filament resource for a Product model\n"
        "- Write a Pest test for user authentication\n"
        "- Explain Laravel's service container",
        title="Usage Guide",
        border_style="green"
    ))

@app.command()
def version():
    """
    Display the version information for the Laravel Developer Agent.
    """
    console.print("Laravel Developer Agent v0.1.0")

@app.command()
def debug_memory():
    """
    Debug the memory structure of the agent.
    This command prints detailed information about the agent's memory.
    """
    global agent
    initialize_agent()
    
    console.print("[bold]Memory Debug Information[/bold]")
    
    try:
        # Get memory variables
        memory_vars = agent.get_memory_variables()
        console.print(f"Memory variables keys: {list(memory_vars.keys())}")
        
        # Examine chat history
        chat_history = memory_vars.get('chat_history', [])
        console.print(f"Chat history length: {len(chat_history)}")
        
        # Check direct history in memory object
        direct_history = agent.memory.chat_history.messages
        console.print(f"Direct history length: {len(direct_history)}")
        
        # Check buffer memory
        try:
            buffer_messages = agent.memory.buffer_memory.chat_memory.messages
            console.print(f"Buffer memory messages length: {len(buffer_messages)}")
        except Exception as e:
            console.print(f"Error accessing buffer memory: {str(e)}")
        
        # Print details of each history type
        console.print("\n[bold]Chat History from get_memory_variables()[/bold]")
        for i, msg in enumerate(chat_history):
            console.print(f"Message {i+1}: {type(msg)} - {str(msg)[:100]}...")
            
        console.print("\n[bold]Direct Chat History[/bold]")
        for i, msg in enumerate(direct_history):
            console.print(f"Message {i+1}: {type(msg)} - {str(msg)[:100]}...")
        
    except Exception as e:
        console.print(f"[bold red]Error during debug:[/bold red] {str(e)}")

@app.command()
def test_memory():
    """
    Run a test sequence to verify the memory implementation is working.
    
    This command:
    1. Creates an agent
    2. Sends test messages
    3. Verifies they're stored in memory
    """
    global agent
    initialize_agent()
    
    console.print("[bold cyan]Running memory test sequence...[/bold cyan]")
    
    # 1. Send a test query
    test_query = "What is a Laravel migration?"
    console.print(f"\n[bold]Step 1: Sending test query:[/bold] {test_query}")
    
    try:
        response = agent.query_simple(test_query)
        console.print(Panel(Markdown(response[:200] + "..."), title="First Response (truncated)", border_style="green"))
        
        # 2. Check if message was stored in memory
        console.print("\n[bold]Step 2: Checking memory after first query[/bold]")
        direct_history = agent.memory.chat_history.messages
        console.print(f"Memory has {len(direct_history)} messages")
        
        if len(direct_history) >= 2:  # Should have at least user query + response
            console.print("[bold green]✓ First messages stored successfully[/bold green]")
        else:
            console.print("[bold red]✗ Failed to store first messages[/bold red]")
        
        # 3. Send a follow-up query that references the first
        follow_up_query = "Can you show an example of a migration for a users table?"
        console.print(f"\n[bold]Step 3: Sending follow-up query:[/bold] {follow_up_query}")
        
        response2 = agent.query_simple(follow_up_query)
        console.print(Panel(Markdown(response2[:200] + "..."), title="Second Response (truncated)", border_style="green"))
        
        # 4. Check final memory state
        console.print("\n[bold]Step 4: Checking final memory state[/bold]")
        final_history = agent.memory.chat_history.messages
        console.print(f"Memory now has {len(final_history)} messages")
        
        if len(final_history) >= 4:  # Should have at least 2 exchanges
            console.print("[bold green]✓ All messages stored successfully[/bold green]")
        else:
            console.print("[bold red]✗ Failed to store all messages[/bold red]")
        
        # 5. Display the memory contents
        console.print("\n[bold]Step 5: Final memory contents[/bold]")
        show_memory_history()
        
        console.print("\n[bold cyan]Memory test complete![/bold cyan]")
        
    except Exception as e:
        console.print(f"[bold red]Error during memory test:[/bold red] {str(e)}")
        import traceback
        console.print(traceback.format_exc())

@app.command()
def diagnose():
    """
    Run diagnostics checks on the Laravel Developer Agent configuration.
    """
    console.print(Panel.fit("[bold]Laravel Developer Agent Diagnostics[/bold]", border_style="blue"))
    
    # Check environment variables
    with Status("[bold cyan]Checking environment variables...[/bold cyan]", spinner="dots") as status:
        env_checks = {
            "ANTHROPIC_API_KEY": config.ANTHROPIC_API_KEY is not None,
            "MODEL": config.MODEL is not None,
            "TEMPERATURE": config.TEMPERATURE is not None,
            "MAX_TOKENS": config.MAX_TOKENS is not None
        }
        
        # Create a table for environment checks
        table = Table(title="Environment Configuration")
        table.add_column("Variable", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Value", style="white")
        
        for var, exists in env_checks.items():
            status = "[bold green]✓" if exists else "[bold red]✗"
            value = getattr(config, var) if exists and var != "ANTHROPIC_API_KEY" else "***" if var == "ANTHROPIC_API_KEY" and exists else "Not set"
            table.add_row(var, status, str(value))
        
        console.print(table)
    
    # Check files
    with Status("[bold cyan]Checking required files...[/bold cyan]", spinner="line") as status:
        file_checks = {
            "Memory File": {"path": MEMORY_FILE, "exists": os.path.exists(MEMORY_FILE), "required": False},
            "Project Context": {"path": PROJECT_CONTEXT_FILE, "exists": os.path.exists(PROJECT_CONTEXT_FILE), "required": False}
        }
        
        # Create a table for file checks
        table = Table(title="File System Checks")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Path", style="white")
        
        for file, info in file_checks.items():
            status = "[bold green]✓" if info["exists"] else "[bold yellow]○" if not info["required"] else "[bold red]✗"
            table.add_row(file, status, info["path"])
        
        console.print(table)
    
    # Test API connection
    with Status("[bold cyan]Testing Anthropic API connection...[/bold cyan]", spinner="growHorizontal") as status:
        if not config.ANTHROPIC_API_KEY:
            console.print("[bold red]Cannot test API connection: ANTHROPIC_API_KEY not set[/bold red]")
        else:
            try:
                # Create a very simple test prompt
                model = create_anthropic_client()
                test_result = "Successfully connected to Anthropic API"
                status.update("[bold green]API connection successful![/bold green]")
            except Exception as e:
                test_result = f"Failed to connect to Anthropic API: {str(e)}"
                status.update("[bold red]API connection failed![/bold red]")
        
        console.print(f"\n[bold]API Connection Test:[/bold] {test_result}")
    
    console.print("\n[bold green]Diagnostics complete![/bold green]")

@app.callback()
def validate_config():
    """
    Validate the configuration before running any command.
    """
    if not config.validate():
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 