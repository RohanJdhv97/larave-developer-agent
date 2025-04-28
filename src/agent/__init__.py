"""
Laravel Developer Agent components.

This package contains the core agent components for Laravel development assistance.
"""

from src.agent.langchain_integration import LaravelDeveloperAgent, test_laravel_chain
from src.agent.memory import LaravelAgentMemory
from src.agent.project_context import LaravelProjectContext
from src.agent.knowledge_base import LaravelKnowledgeBase, load_knowledge_base
from src.agent.expertise.planning import RequirementAnalysis, DatabasePlanning, ImplementationStrategyPlanner

# Expertise modules
from src.agent.expertise.laravel import (
    LaravelApiExpertise,
    LaravelDatabaseExpertise,
    LaravelCodeStandardsExpertise,
)

from src.agent.expertise.testing import (
    LaravelPestTestingExpertise,
    LaravelLarecipeExpertise,
)

from src.agent.expertise.filament import (
    FilamentResourceExpertise,
    FilamentFormExpertise,
    FilamentTableExpertise,
    FilamentTestingExpertise,
)

__all__ = [
    'LaravelDeveloperAgent',
    'test_laravel_chain',
    'LaravelAgentMemory',
    'LaravelProjectContext',
    'LaravelKnowledgeBase',
    'load_knowledge_base',
    'RequirementAnalysis',
    'DatabasePlanning',
    'ImplementationStrategyPlanner',
    'LaravelApiExpertise',
    'LaravelDatabaseExpertise',
    'LaravelCodeStandardsExpertise',
    'LaravelPestTestingExpertise',
    'LaravelLarecipeExpertise',
    'FilamentResourceExpertise',
    'FilamentFormExpertise',
    'FilamentTableExpertise',
    'FilamentTestingExpertise',
] 