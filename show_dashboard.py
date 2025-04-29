"""
Memory Dashboard Launcher

This script initializes the memory dashboard interface.
"""

import sys
import os
from src.ui.memory_dashboard import MemoryDashboard

def main():
    print("Launching Memory Dashboard...")
    
    # Create and launch the dashboard without a memory system
    # The dashboard will create its own memory system for demonstration
    dashboard = MemoryDashboard()
    dashboard.start_standalone()

if __name__ == "__main__":
    main() 