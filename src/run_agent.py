"""
Run Laravel Developer Agent

This script initializes and runs the Laravel Developer Agent.
It serves as the entry point for interaction with the agent.
"""

import argparse
import sys
from typing import Dict, Any, List, Optional

from src.agent import LaravelAgent
from src.agent.memory import LaravelAgentMemory
from src.agent.knowledge_base import LaravelKnowledgeBase
from src.agent.workflow import create_workflow

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Run the Laravel Developer Agent")
    
    # Add arguments
    parser.add_argument(
        "--query", 
        type=str, 
        help="User query to process"
    )
    parser.add_argument(
        "--demo-planning",
        action="store_true",
        help="Run a planning capabilities demo"
    )
    
    return parser.parse_args()

def run_planning_demo() -> None:
    """
    Run a demo of the agent's planning capabilities.
    """
    print("Running Laravel Developer Agent Planning Capabilities Demo")
    print("=" * 50)
    
    # Initialize components
    memory = LaravelAgentMemory()
    knowledge_base = LaravelKnowledgeBase()
    workflow = create_workflow(memory, knowledge_base)
    
    # Create the agent
    agent = LaravelAgent(memory, knowledge_base, workflow)
    
    # Define a sample planning query
    planning_query = """
    I need to build a blog system with the following requirements:
    1. Users can register, login, and manage their profiles
    2. Users can create, edit, and delete blog posts
    3. Posts can have categories and tags
    4. Users can comment on posts
    5. Admin users can moderate comments and manage all content
    
    Please analyze these requirements, design a database schema, and provide an implementation strategy.
    """
    
    print("Sample Planning Query:")
    print("-" * 50)
    print(planning_query)
    print("-" * 50)
    print("\nGenerating response...\n")
    
    # Process the query
    response = agent.process_query(planning_query)
    
    print("Response:")
    print("-" * 50)
    print(response)
    print("-" * 50)

def main() -> None:
    """
    Main entry point for the Laravel Developer Agent.
    """
    args = parse_args()
    
    # Run planning demo if requested
    if args.demo_planning:
        run_planning_demo()
        return
    
    # If no query provided, read from stdin
    query = args.query
    if not query:
        print("Enter your query (Ctrl+D to submit):")
        query = sys.stdin.read().strip()
    
    if not query:
        print("No query provided. Exiting.")
        return
    
    # Initialize components
    memory = LaravelAgentMemory()
    knowledge_base = LaravelKnowledgeBase()
    workflow = create_workflow(memory, knowledge_base)
    
    # Create the agent
    agent = LaravelAgent(memory, knowledge_base, workflow)
    
    # Process the query
    response = agent.process_query(query)
    
    # Output the response
    print("\nResponse:")
    print("-" * 50)
    print(response)
    print("-" * 50)

if __name__ == "__main__":
    main() 