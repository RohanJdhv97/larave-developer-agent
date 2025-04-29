"""
Memory System UI implementation for command-line interfaces.

This module provides a UI component for visualizing and interacting with the dual memory system,
showing memory state, transitions, and operations with beautiful terminal output.
"""

import time
from typing import Dict, List, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.syntax import Syntax
from rich import box
from rich.text import Text
from rich.prompt import Confirm
from rich.style import Style
from datetime import datetime, timedelta
from rich.columns import Columns


class MemoryUI:
    """
    UI component for the memory system that provides visual feedback and interface components
    for memory operations.
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize the memory UI with a rich console instance.
        
        Args:
            console: Optional Rich Console instance. If not provided, a new one will be created.
        """
        self.console = console or Console()
        self._progress: Optional[Progress] = None
        
    def _get_console(self) -> Console:
        """Get the Rich console instance for this UI."""
        return self.console
        
    def show_memory_state(self, memory, with_contents=False):
        """Display the current state of the memory, with counts of temporary and permanent entries."""
        if not memory:
            print("No memory available.")
            return
            
        # Try to access messages from various sources
        messages = []
        
        try:
            # First try the chat_history adapter property
            if hasattr(memory, 'chat_history_adapter'):
                if hasattr(memory.chat_history_adapter, 'messages'):
                    messages = memory.chat_history_adapter.messages
            
            # Then try the direct chat_history property
            elif hasattr(memory, 'chat_history'):
                if hasattr(memory.chat_history, 'messages'):
                    messages = memory.chat_history.messages
                elif isinstance(memory.chat_history, list):
                    messages = memory.chat_history
            
            # Try the dual_memory direct access as fallback
            elif hasattr(memory, 'dual_memory') and hasattr(memory.dual_memory, 'temporary_memory'):
                temp_messages = memory.dual_memory.temporary_memory.get_messages()
                messages = [m for m in temp_messages]
            
            # If this is a DualMemorySystem itself, access the temporary_memory directly
            elif hasattr(memory, 'temporary_memory') and hasattr(memory.temporary_memory, 'get_messages'):
                temp_messages = memory.temporary_memory.get_messages()
                messages = [m for m in temp_messages]
                
            # Count message types - handle both dict-style and object-style messages
            user_msgs = 0
            ai_msgs = 0
            
            for m in messages:
                # Handle dictionary-style messages
                if isinstance(m, dict):
                    if m.get('role') == 'user':
                        user_msgs += 1
                    elif m.get('role') == 'assistant':
                        ai_msgs += 1
                # Handle object-style messages with type attribute
                elif hasattr(m, 'type'):
                    if m.type == 'human':
                        user_msgs += 1
                    elif m.type == 'ai':
                        ai_msgs += 1
                # Handle LangChain message classes
                elif type(m).__name__ == 'HumanMessage':
                    user_msgs += 1
                elif type(m).__name__ == 'AIMessage':
                    ai_msgs += 1
                
            total_msgs = user_msgs + ai_msgs
            
            # Display memory state
            console = self._get_console()
            panel = Panel(
                f"[bold cyan]Memory State[/]\n\n"
                f"💬 Temporary Memory: [bold]{total_msgs}[/] messages "
                f"([green]{user_msgs}[/] user, [blue]{ai_msgs}[/] AI)\n",
                title="Memory",
                border_style="green",
                expand=False
            )
            console.print(panel)
            
            # Display permanent memory stats if available
            perm_count = 0
            
            # Try different ways to access the permanent memory
            if hasattr(memory, 'dual_memory') and hasattr(memory.dual_memory, 'permanent_memory'):
                perm_memory = memory.dual_memory.permanent_memory
                if hasattr(perm_memory, 'get_count'):
                    perm_count = perm_memory.get_count()
                elif hasattr(perm_memory, 'get_entries'):
                    perm_count = len(perm_memory.get_entries())
            # Direct access if this is a DualMemorySystem
            elif hasattr(memory, 'permanent_memory'):
                perm_memory = memory.permanent_memory
                if hasattr(perm_memory, 'get_count'):
                    perm_count = perm_memory.get_count()
                elif hasattr(perm_memory, 'get_entries'):
                    perm_count = len(perm_memory.get_entries())
                
            if perm_count > 0:
                perm_panel = Panel(
                    f"📚 [bold magenta]Permanent Memory:[/] [bold]{perm_count}[/] items stored\n",
                    border_style="magenta",
                    expand=False
                )
                console.print(perm_panel)
                
        except Exception as e:
            print(f"Error displaying memory: {str(e)}")
        
    def memory_thinking(self, message: str):
        """
        Show that the memory system is actively thinking about a specific task.
        
        Args:
            message: The thinking message to display
        """
        thinking_text = Text("🧠 ")
        thinking_text.append(message, style="blue italic")
        self.console.print(thinking_text)
        
    def show_memory_usage(self, operation: str, memory_type: str):
        """
        Display which memory system is being used for an operation.
        
        Args:
            operation: The operation being performed (e.g., "search", "retrieval")
            memory_type: The type of memory being used ("temporary" or "permanent")
        """
        style = "cyan" if memory_type.lower() == "temporary" else "green"
        memory_name = "Temporary Memory" if memory_type.lower() == "temporary" else "Permanent Memory"
        
        text = Text("📝 ")
        text.append(f"{operation} ", style="bold")
        text.append("using ", style="dim")
        text.append(memory_name, style=style)
        
        self.console.print(text)
        
    def analyzing_temporary_memory(self, with_progress: bool = True):
        """
        Show progress during memory analysis.
        
        Args:
            with_progress: Whether to display a progress bar (for longer operations)
        """
        self.console.print(Text("🔍 Analyzing temporary memory...", style="blue bold"))
        
        if with_progress:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(bar_width=40),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=self.console,
                expand=True
            )
            
            # Store the progress bar for later reference
            self._progress = progress
            progress.start()
            return progress
        else:
            # Just show a simple message for quick operations
            self.console.print("[bold blue]Analyzing temporary memory...[/]")
            return None
            
    def show_storing_knowledge(self, count: int, entries: List[Dict[str, Any]]):
        """
        Display information about knowledge being stored in permanent memory.
        
        Args:
            count: Number of entries being stored
            entries: List of knowledge entries with their details
        """
        if count == 0:
            self.console.print(Text("ℹ️ No new knowledge to store", style="yellow"))
            return
            
        panel_text = Text(f"📚 Stored {count} knowledge entries in permanent memory\n\n")
        
        # Show up to 3 sample entries
        for i, entry in enumerate(entries[:3]):
            # Format timestamp if present
            timestamp = entry.get("timestamp", "")
            if timestamp and isinstance(timestamp, str):
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    pass
                    
            # Get a preview of the content
            content = entry.get("content", "")
            if len(content) > 100:
                content = content[:97] + "..."
                
            # Add entry details
            panel_text.append(f"{i+1}. ", style="bold")
            panel_text.append(f"[{entry.get('category', 'general')}] ", style="cyan")
            panel_text.append(content)
            if i < min(2, len(entries) - 1):  # Add newline except after last entry
                panel_text.append("\n")
        
        # If there are more entries than we're showing
        if len(entries) > 3:
            panel_text.append(f"\n\n...and {len(entries) - 3} more entries")
            
        self.console.print(Panel(
            panel_text,
            title="Knowledge Storage",
            border_style="green",
            box=box.ROUNDED
        ))
        
    def show_code_snippet(self, code: str, language: str = "python"):
        """
        Display a formatted code snippet.
        
        Args:
            code: The code string to display
            language: The programming language for syntax highlighting
        """
        # Limit code length for display
        if len(code) > 1000:
            code = code[:997] + "..."
            
        self.console.print(f"\n[bold]Code Snippet ({language}):[/bold]")
        self.console.print(Panel(code, language=language))
        
    def memory_saved(self, file_path: str):
        """
        Notification that memory has been saved to a file.
        
        Args:
            file_path: The file path where memory was saved
        """
        self.console.print(Text(f"💾 Memory saved to {file_path}", style="green bold"))
        
    def memory_loaded(self, file_path: str, temp_count: int, perm_count: int):
        """
        Notification that memory has been loaded from a file.
        
        Args:
            file_path: The file path from which memory was loaded
            temp_count: Number of temporary memory entries loaded
            perm_count: Number of permanent memory entries loaded
        """
        text = Text("📂 ")
        text.append("Memory loaded", style="green bold")
        text.append(f" from {file_path}\n")
        text.append(f"    {temp_count} temporary messages, {perm_count} permanent entries")
        
        self.console.print(text)
        
    def show_memory_completion(self):
        """Stop any progress indicators and show completion of memory operations."""
        if self._progress:
            self._progress.stop()
            self._progress = None
            
        self.console.print(Text("✅ Memory analysis complete", style="green bold"))
        
    def show_search_results(self, results: List[Dict[str, Any]], query: str):
        """
        Display memory search results in a formatted table.
        
        Args:
            results: List of memory entries from the search
            query: The search query that produced these results
        """
        if not results:
            self.console.print(Text(f"🔍 No results found for '{query}'", style="yellow"))
            return
            
        table = Table(title=f"Search Results for '{query}'", box=box.ROUNDED, highlight=True)
        table.add_column("Source", style="cyan")
        table.add_column("Content", style="white")
        table.add_column("Relevance", style="green")
        
        for result in results:
            # Format content for display
            content = result.get("content", "")
            if len(content) > 70:
                content = content[:67] + "..."
                
            # Source formatting
            source = result.get("source", "unknown")
            source_style = "cyan" if source == "temporary_memory" else "green"
            source_display = "Temporary" if source == "temporary_memory" else "Permanent"
            
            # Relevance score
            relevance = result.get("relevance", 0)
            if isinstance(relevance, float):
                relevance_str = f"{relevance:.2f}"
            else:
                relevance_str = str(relevance)
                
            table.add_row(
                Text(source_display, style=source_style),
                content,
                relevance_str
            )
            
        self.console.print(table)
        
    def conversation_summary(self, summary: Dict[str, Any]):
        """
        Display a summary of conversation metrics.
        
        Args:
            summary: Dictionary containing conversation metrics like message count,
                 tokens used, knowledge entries created, etc.
        """
        table = Table(title="Conversation Summary", box=box.ROUNDED, highlight=True)
        table.add_column("Metric", style="cyan bold")
        table.add_column("Value", style="green")
        
        # Add basic metrics
        table.add_row("Messages", str(summary.get("messages_count", 0)))
        table.add_row("Knowledge Entries", str(summary.get("knowledge_entries_count", 0)))
        table.add_row("Searches Performed", str(summary.get("searches_performed", 0)))
        table.add_row("Memory Transitions", str(summary.get("memory_transitions", 0)))
        
        # Format session time if available
        if "session_start" in summary:
            try:
                start_time = datetime.fromisoformat(summary["session_start"])
                duration = datetime.now() - start_time
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = f"{hours}h {minutes}m {seconds}s"
                table.add_row("Session Duration", duration_str)
            except (ValueError, TypeError):
                pass
        
        self.console.print(table)
        
    def show_memory_transition(self, from_memory: str, to_memory: str, reason: str):
        """
        Display when the system transitions between memory types.
        
        Args:
            from_memory: The memory type transitioning from
            to_memory: The memory type transitioning to
            reason: The reason for the transition
        """
        text = Text("🔄 ")
        text.append("Memory Transition", style="magenta bold")
        text.append(f": {from_memory} → {to_memory}", style="magenta")
        text.append(f"\n    {reason}", style="italic")
        
        self.console.print(Panel(text, border_style="magenta"))
        
    def error(self, message: str):
        """
        Display an error message.
        
        Args:
            message: The error message to display
        """
        self.console.print(Text(f"❌ Error: {message}", style="bold red"))


# Create a global instance for easy access
memory_ui = MemoryUI() 