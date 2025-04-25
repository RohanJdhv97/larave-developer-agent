import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from src.agent.langchain_integration import test_laravel_chain
from src.utils.config import config

# Initialize typer app and rich console
app = typer.Typer(
    help="Laravel Developer Agent - AI assistant for Laravel development",
    add_completion=False
)
console = Console()

@app.command()
def query(
    query_text: str = typer.Argument(..., help="The Laravel development query to process"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    Process a single Laravel development query and display the result.
    """
    if verbose:
        console.print("[bold cyan]Processing query...[/bold cyan]")
        console.print(f"Model: {config.MODEL}")
        console.print(f"Temperature: {config.TEMPERATURE}")
    
    try:
        response = test_laravel_chain(query_text)
        console.print(Panel(Markdown(response), title="Laravel Agent Response", border_style="green"))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@app.command()
def interactive():
    """
    Start an interactive session with the Laravel Developer Agent.
    """
    console.print(Panel.fit(
        "[bold purple]Laravel Developer Agent[/bold purple]\n"
        "Ask any questions related to Laravel, Filament, or PHP development.\n"
        "Type 'exit' or 'quit' to end the session.",
        title="Welcome",
        border_style="purple"
    ))
    
    while True:
        user_input = Prompt.ask("\n[bold blue]Your Laravel question[/bold blue]")
        
        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold]Thank you for using Laravel Developer Agent. Goodbye![/bold]")
            break
            
        try:
            response = test_laravel_chain(user_input)
            console.print(Panel(Markdown(response), title="Laravel Agent Response", border_style="green"))
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

@app.command()
def version():
    """
    Display the version information for the Laravel Developer Agent.
    """
    console.print("Laravel Developer Agent v0.1.0")

@app.callback()
def validate_config():
    """
    Validate the configuration before running any command.
    """
    if not config.validate():
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 