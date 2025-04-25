#!/usr/bin/env python3
"""
Laravel Command Generator - A companion tool for Laravel Assistant.
This script generates common Laravel commands based on user input.
"""

import os
import sys
import argparse
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

# Initialize Rich console for better output
console = Console()

class LaravelCommandGenerator:
    """Generate common Laravel commands based on user input."""
    
    COMMAND_CATEGORIES = {
        "artisan": "Laravel Artisan Commands",
        "migration": "Database Migrations",
        "model": "Eloquent Models",
        "controller": "Controllers",
        "resource": "Resources & APIs",
        "filament": "Filament PHP Commands", 
        "pest": "Pest PHP Testing",
        "composer": "Composer Commands"
    }
    
    def __init__(self):
        """Initialize the Laravel Command Generator."""
        self.commands = self._load_commands()
    
    def _load_commands(self) -> Dict[str, List[Dict[str, str]]]:
        """Load the available Laravel commands."""
        return {
            "artisan": [
                {"name": "List commands", "command": "php artisan list"},
                {"name": "Clear cache", "command": "php artisan cache:clear"},
                {"name": "Clear config cache", "command": "php artisan config:clear"},
                {"name": "Clear route cache", "command": "php artisan route:clear"},
                {"name": "Clear view cache", "command": "php artisan view:clear"},
                {"name": "Maintenance mode on", "command": "php artisan down"},
                {"name": "Maintenance mode off", "command": "php artisan up"},
                {"name": "Optimize", "command": "php artisan optimize"},
                {"name": "Create key", "command": "php artisan key:generate"},
            ],
            "migration": [
                {"name": "Create migration", "command": "php artisan make:migration {name}"},
                {"name": "Run migrations", "command": "php artisan migrate"},
                {"name": "Rollback last migration", "command": "php artisan migrate:rollback"},
                {"name": "Reset all migrations", "command": "php artisan migrate:reset"},
                {"name": "Refresh all migrations", "command": "php artisan migrate:refresh"},
                {"name": "Refresh with seed", "command": "php artisan migrate:refresh --seed"},
                {"name": "Show migration status", "command": "php artisan migrate:status"},
            ],
            "model": [
                {"name": "Create model", "command": "php artisan make:model {name}"},
                {"name": "Create model with migration", "command": "php artisan make:model {name} -m"},
                {"name": "Create model with factory", "command": "php artisan make:model {name} -f"},
                {"name": "Create model with seeder", "command": "php artisan make:model {name} -s"},
                {"name": "Create model with all", "command": "php artisan make:model {name} -mfs"},
                {"name": "Create model with controller", "command": "php artisan make:model {name} -c"},
            ],
            "controller": [
                {"name": "Create controller", "command": "php artisan make:controller {name}Controller"},
                {"name": "Create resource controller", "command": "php artisan make:controller {name}Controller --resource"},
                {"name": "Create API controller", "command": "php artisan make:controller {name}Controller --api"},
                {"name": "Create invokable controller", "command": "php artisan make:controller {name}Controller --invokable"},
            ],
            "resource": [
                {"name": "Create resource", "command": "php artisan make:resource {name}Resource"},
                {"name": "Create resource collection", "command": "php artisan make:resource {name}Collection"},
                {"name": "Create API resource", "command": "php artisan make:resource {name}Resource --collection"},
            ],
            "filament": [
                {"name": "Create Filament resource", "command": "php artisan make:filament-resource {name}"},
                {"name": "Create Filament resource with soft deletes", "command": "php artisan make:filament-resource {name} --soft-deletes"},
                {"name": "Create Filament page", "command": "php artisan make:filament-page {name}"},
                {"name": "Create Filament widget", "command": "php artisan make:filament-widget {name}"},
                {"name": "Create Filament relation manager", "command": "php artisan make:filament-relation-manager {model} {relationship}"},
                {"name": "Create Filament theme", "command": "php artisan make:filament-theme"},
                {"name": "Create Filament user", "command": "php artisan make:filament-user"},
            ],
            "pest": [
                {"name": "Create Pest feature test", "command": "php artisan make:test {name}Test"},
                {"name": "Create Pest unit test", "command": "php artisan make:test {name}Test --unit"},
                {"name": "Run Pest tests", "command": "./vendor/bin/pest"},
                {"name": "Run Pest tests with coverage", "command": "./vendor/bin/pest --coverage"},
            ],
            "composer": [
                {"name": "Install dependencies", "command": "composer install"},
                {"name": "Update dependencies", "command": "composer update"},
                {"name": "Require package", "command": "composer require {package}"},
                {"name": "Require dev package", "command": "composer require --dev {package}"},
                {"name": "Remove package", "command": "composer remove {package}"},
                {"name": "Show installed packages", "command": "composer show"},
                {"name": "Dump autoload", "command": "composer dump-autoload"},
                {"name": "Validate composer.json", "command": "composer validate"},
            ],
        }
    
    def display_categories(self):
        """Display the available command categories."""
        table = Table(title="Laravel Command Categories")
        table.add_column("Number", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Description", style="yellow")
        
        for i, (key, description) in enumerate(self.COMMAND_CATEGORIES.items(), 1):
            table.add_row(str(i), key, description)
        
        console.print(table)
    
    def display_commands(self, category: str):
        """Display the available commands for a category."""
        if category not in self.commands:
            console.print(f"[bold red]Error:[/bold red] Category '{category}' not found.")
            return
        
        table = Table(title=f"Laravel {category.capitalize()} Commands")
        table.add_column("Number", style="cyan")
        table.add_column("Command Name", style="green")
        table.add_column("Command", style="yellow")
        
        for i, cmd in enumerate(self.commands[category], 1):
            table.add_row(str(i), cmd["name"], cmd["command"])
        
        console.print(table)
    
    def generate_command(self, category: str, command_index: int) -> Optional[str]:
        """
        Generate a command based on the category and index.
        
        Args:
            category: The command category
            command_index: The 1-based index of the command
            
        Returns:
            The generated command or None if not found
        """
        if category not in self.commands:
            console.print(f"[bold red]Error:[/bold red] Category '{category}' not found.")
            return None
        
        if command_index < 1 or command_index > len(self.commands[category]):
            console.print(f"[bold red]Error:[/bold red] Command index out of range.")
            return None
        
        command = self.commands[category][command_index - 1]["command"]
        
        # Replace placeholders with user input
        while "{" in command and "}" in command:
            placeholder = command[command.find("{")+1:command.find("}")]
            value = Prompt.ask(f"Enter value for [cyan]{placeholder}[/cyan]")
            command = command.replace(f"{{{placeholder}}}", value)
        
        return command
    
    def interactive_mode(self):
        """Run the generator in interactive mode."""
        console.print(Panel.fit(
            "[bold purple]Laravel Command Generator[/bold purple]\n"
            "Generate common Laravel commands with ease.\n"
            "Type 'exit' or 'quit' at any prompt to exit.",
            title="Welcome",
            border_style="purple"
        ))
        
        while True:
            # Display categories
            self.display_categories()
            
            # Get category selection
            category_input = Prompt.ask("\n[bold blue]Select a category[/bold blue] (number or name, 'exit' to quit)")
            
            if category_input.lower() in ["exit", "quit"]:
                console.print("[bold]Thank you for using Laravel Command Generator. Goodbye![/bold]")
                break
            
            # Convert number input to category key
            category = category_input
            if category_input.isdigit():
                index = int(category_input)
                if 1 <= index <= len(self.COMMAND_CATEGORIES):
                    category = list(self.COMMAND_CATEGORIES.keys())[index - 1]
                else:
                    console.print("[bold red]Invalid category number.[/bold red]")
                    continue
            
            if category not in self.commands:
                console.print(f"[bold red]Category '{category}' not found.[/bold red]")
                continue
            
            # Display commands for the selected category
            self.display_commands(category)
            
            # Get command selection
            command_input = Prompt.ask("\n[bold blue]Select a command[/bold blue] (number, 'back' to go back)")
            
            if command_input.lower() == "back":
                continue
                
            if not command_input.isdigit():
                console.print("[bold red]Please enter a valid command number.[/bold red]")
                continue
            
            command_index = int(command_input)
            
            # Generate the command
            command = self.generate_command(category, command_index)
            if command:
                console.print(f"\n[bold green]Generated Command:[/bold green]")
                console.print(Panel(command, border_style="green"))
                
                # Copy to clipboard if pyperclip is available
                try:
                    import pyperclip
                    pyperclip.copy(command)
                    console.print("[italic]Command copied to clipboard![/italic]")
                except ImportError:
                    pass
                
                # Ask if the user wants to execute the command
                if Confirm.ask("Execute this command?"):
                    console.print(f"\n[bold cyan]Executing:[/bold cyan] {command}")
                    os.system(command)

def main():
    """Main entry point for the command generator."""
    parser = argparse.ArgumentParser(description="Laravel Command Generator")
    parser.add_argument("--category", "-c", help="Command category")
    parser.add_argument("--index", "-i", type=int, help="Command index within the category")
    args = parser.parse_args()
    
    generator = LaravelCommandGenerator()
    
    if args.category and args.index:
        # Generate a specific command
        command = generator.generate_command(args.category, args.index)
        if command:
            print(command)
    else:
        # Interactive mode
        generator.interactive_mode()

if __name__ == "__main__":
    main() 