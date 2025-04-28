"""
Demo script for planning and analytical reasoning capabilities.

This script demonstrates how to use the requirement analysis, database planning,
and implementation strategy capabilities of the Laravel Developer Agent.
"""

import json
import os
from src.agent import RequirementAnalysis, DatabasePlanning, ImplementationStrategyPlanner

def main():
    """Run the planning demo."""
    print("Laravel Developer Agent Planning Capabilities Demo")
    print("=" * 50)
    
    # Sample requirements
    requirements = """
    Create a blog system that allows users to create, edit, and publish articles.
    Users should be able to register and login to the system.
    Each article should have a title, content, and tags.
    Users should be able to comment on articles.
    The system should have an admin panel to manage users, articles, and comments.
    """
    
    # Step 1: Analyze the requirements
    print("\n1. Analyzing requirements...")
    analyzer = RequirementAnalysis()
    analysis_result = analyzer.analyze_requirements(requirements)
    
    # Output the requirement analysis
    print("\nRequirement Analysis Results:")
    print("-" * 30)
    analysis_output = analyzer.generate_breakdown_output(analysis_result)
    print(analysis_output)
    
    # Step 2: Plan the database schema
    print("\n\n2. Planning database schema...")
    db_planner = DatabasePlanning()
    db_schema = db_planner.plan_database_schema(analysis_result.dict())
    
    # Output the database schema plan
    print("\nDatabase Schema Plan:")
    print("-" * 30)
    schema_output = db_planner.generate_schema_output(db_schema)
    print(schema_output)
    
    # Step 3: Generate implementation strategy
    print("\n\n3. Generating implementation strategy...")
    strategy_planner = ImplementationStrategyPlanner()
    implementation_strategy = strategy_planner.plan_implementation_strategy(
        analysis_result.dict(),
        db_schema.dict()
    )
    
    # Output the implementation strategy
    print("\nImplementation Strategy:")
    print("-" * 30)
    strategy_output = strategy_planner.generate_strategy_output(implementation_strategy)
    print(strategy_output)
    
    # Save output to file
    print("\n\nSaving analysis to files...")
    os.makedirs("output", exist_ok=True)
    
    with open("output/requirement_analysis.md", "w") as f:
        f.write(analysis_output)
    
    with open("output/database_schema.md", "w") as f:
        f.write(schema_output)
        
    with open("output/implementation_strategy.md", "w") as f:
        f.write(strategy_output)
    
    print("Done! Files saved to the 'output' directory.")

if __name__ == "__main__":
    main() 