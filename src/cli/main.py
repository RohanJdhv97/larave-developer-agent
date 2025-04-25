import typer
import asyncio
import os
import atexit
import json
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint

from src.agent.langchain_integration import test_laravel_chain, LaravelDeveloperAgent
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

def initialize_agent():
    """Initialize the agent with memory loaded from disk if available."""
    global agent
    if agent is None:
        agent = LaravelDeveloperAgent()
        
        # Try to load saved memory if it exists
        if os.path.exists(MEMORY_FILE):
            try:
                # Load memory directly instead of using load_state
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
            agent.save_state(memory_path=MEMORY_FILE, context_path=PROJECT_CONTEXT_FILE)
            console.print(f"[bold green]Saved conversation memory to {MEMORY_FILE}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error saving memory: {str(e)}[/bold red]")

# Register the exit handler
atexit.register(save_memory_on_exit)

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
        if simple:
            # Use the simple chain for compatibility
            response = test_laravel_chain(query_text)
        else:
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
        "[bold purple]Laravel Developer Agent[/bold purple]\n"
        "Ask any questions related to Laravel, Filament, or PHP development.\n"
        "Type 'exit' or 'quit' to end the session.\n"
        "Type '!simple' to toggle simple mode.\n"
        "Type '!help' to see all available commands.",
        title="Welcome",
        border_style="purple"
    ))
    
    # Keep track of whether to use simple mode
    use_simple_mode = no_workflow
    
    while True:
        # Show the current mode
        mode_indicator = "[Simple Mode]" if use_simple_mode else "[Memory Mode]"
        user_input = Prompt.ask(f"\n[bold blue]{mode_indicator} Your Laravel question[/bold blue]")
        
        # Handle special commands
        if user_input.lower() in ["exit", "quit"]:
            # Save memory before exiting
            try:
                # Save memory directly
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
            show_project_context()
            continue
        elif user_input.lower() == "!memory":
            # Display the memory contents from agent.memory.chat_history directly
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
                agent.memory.save(MEMORY_FILE)
                console.print(f"[bold green]Agent memory saved to {MEMORY_FILE}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error saving memory: {str(e)}[/bold red]")
            continue
        elif user_input.lower() == "!load":
            try:
                agent.memory = LaravelAgentMemory.load(MEMORY_FILE)
                console.print(f"[bold green]Agent memory loaded from {MEMORY_FILE} with {len(agent.memory.chat_history.messages)} messages[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error loading memory: {str(e)}[/bold red]")
            continue
        elif user_input.lower() == "!reset":
            if Prompt.ask("[bold yellow]Reset all memory? This cannot be undone. (y/n)[/bold yellow]").lower() == 'y':
                # Create a fresh memory instance
                agent.memory = LaravelAgentMemory()
                console.print("[bold red]Memory reset complete. All conversation history cleared.[/bold red]")
            continue
        elif user_input.lower() == "!help":
            show_help()
            continue
            
        try:
            if use_simple_mode:
                response = agent.query_simple(user_input)
            else:
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
    table = Table(title="Available Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")
    
    table.add_row("exit, quit", "Exit the interactive session")
    table.add_row("!simple", "Toggle between simple mode and memory mode")
    table.add_row("!context", "Show the current project context")
    table.add_row("!memory", "Show the conversation history")
    table.add_row("!debug", "Display debug information about the memory")
    table.add_row("!save", "Save the agent's state to disk")
    table.add_row("!load", "Load the agent's state from disk") 
    table.add_row("!reset", "Reset all memory and start fresh")
    table.add_row("!help", "Show this help message")
    
    console.print(table)

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
    Run a diagnostic check on the memory system.
    
    This command:
    1. Checks the memory file existence and format
    2. Attempts to load memory
    3. Checks the agent's memory state
    4. Verifies the save process
    """
    console.print("[bold cyan]Running memory system diagnostics...[/bold cyan]")
    
    # Check memory file
    console.print("\n[bold]1. Checking memory file[/bold]")
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                file_contents = f.read()
                console.print(f"Memory file exists ({len(file_contents)} bytes)")
                
                memory_data = json.loads(file_contents)
                console.print(f"Memory file contains keys: {list(memory_data.keys())}")
                
                chat_history = memory_data.get("chat_history", [])
                console.print(f"Found {len(chat_history)} messages in file")
                
                for i, msg in enumerate(chat_history):
                    console.print(f"Message {i+1}: Type={msg.get('type')}, Content={msg.get('content')[:30]}...")
        except Exception as e:
            console.print(f"[bold red]Error reading memory file:[/bold red] {str(e)}")
    else:
        console.print("Memory file does not exist")
    
    # Initialize agent
    console.print("\n[bold]2. Initializing agent and loading memory[/bold]")
    global agent
    agent = LaravelDeveloperAgent()
    
    # Load memory manually
    console.print("\n[bold]3. Loading memory directly[/bold]")
    try:
        # Call the load function directly
        agent.memory = LaravelAgentMemory.load(MEMORY_FILE)
        console.print("[bold green]Memory loaded successfully[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error loading memory:[/bold red] {str(e)}")
    
    # Check memory state
    console.print("\n[bold]4. Checking memory state[/bold]")
    try:
        direct_history = agent.memory.chat_history.messages
        console.print(f"Agent has {len(direct_history)} messages in memory")
        
        memory_vars = agent.get_memory_variables()
        console.print(f"Memory variables: {list(memory_vars.keys())}")
        
        chat_history = memory_vars.get('chat_history', [])
        console.print(f"Memory variables has {len(chat_history)} messages")
    except Exception as e:
        console.print(f"[bold red]Error checking memory state:[/bold red] {str(e)}")
    
    # Add a test message
    console.print("\n[bold]5. Adding and saving a test message[/bold]")
    try:
        # Add a test message
        agent.memory.add_user_message("This is a test message from diagnostics")
        
        # Check memory state again
        direct_history = agent.memory.chat_history.messages
        console.print(f"Agent now has {len(direct_history)} messages in memory")
        
        # Save memory
        agent.save_state(memory_path=MEMORY_FILE, context_path=PROJECT_CONTEXT_FILE)
        console.print("[bold green]Memory saved successfully[/bold green]")
        
        # Verify save by reading file again
        with open(MEMORY_FILE, "r") as f:
            memory_data = json.load(f)
            chat_history = memory_data.get("chat_history", [])
            console.print(f"Memory file now has {len(chat_history)} messages")
    except Exception as e:
        console.print(f"[bold red]Error in add/save test:[/bold red] {str(e)}")
    
    console.print("\n[bold cyan]Memory diagnostics complete![/bold cyan]")

@app.callback()
def validate_config():
    """
    Validate the configuration before running any command.
    """
    if not config.validate():
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 