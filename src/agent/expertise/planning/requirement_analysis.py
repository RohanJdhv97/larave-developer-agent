"""
Requirement analysis and breakdown module.

This module provides capabilities for analyzing software requirements and breaking
them down into implementable components.
"""

from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field
import re
from enum import Enum

class RequirementType(str, Enum):
    """Types of requirements for categorization."""
    DATA_STORAGE = "data_storage"
    USER_INTERACTION = "user_interaction"
    BUSINESS_LOGIC = "business_logic"
    AUTHENTICATION = "authentication"
    INTEGRATION = "integration"
    REPORTING = "reporting"
    NOTIFICATION = "notification"
    FILE_MANAGEMENT = "file_management"
    BACKGROUND_PROCESS = "background_process"
    SECURITY = "security"
    PERFORMANCE = "performance"
    OTHER = "other"

class RequirementPriority(str, Enum):
    """Priority levels for requirements."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RequirementEntity(BaseModel):
    """Model representing an entity extracted from requirements."""
    name: str
    attributes: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    related_entities: List[str] = Field(default_factory=list)

class RequirementAction(BaseModel):
    """Model representing an action or operation extracted from requirements."""
    name: str
    description: str
    actor: Optional[str] = None
    target_entities: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)

class RequirementConstraint(BaseModel):
    """Model representing a constraint extracted from requirements."""
    description: str
    constraint_type: str
    related_entities: List[str] = Field(default_factory=list)
    related_actions: List[str] = Field(default_factory=list)

class RequirementDependency(BaseModel):
    """Model representing a dependency between requirements."""
    source_id: str
    target_id: str
    dependency_type: str
    description: Optional[str] = None

class RequirementComponent(BaseModel):
    """Model representing a single requirement component."""
    id: str
    title: str
    description: str
    requirement_type: RequirementType
    priority: RequirementPriority = RequirementPriority.MEDIUM
    entities: List[RequirementEntity] = Field(default_factory=list)
    actions: List[RequirementAction] = Field(default_factory=list)
    constraints: List[RequirementConstraint] = Field(default_factory=list)
    dependencies: List[RequirementDependency] = Field(default_factory=list)
    estimated_complexity: int = 1  # Scale of 1-5
    notes: Optional[str] = None

class RequirementAnalysisResult(BaseModel):
    """Model representing the complete result of a requirement analysis."""
    components: List[RequirementComponent] = Field(default_factory=list)
    entities: List[RequirementEntity] = Field(default_factory=list)
    suggested_implementation_order: List[str] = Field(default_factory=list)
    technical_considerations: List[str] = Field(default_factory=list)

class RequirementAnalysis:
    """
    Provides capabilities for analyzing software requirements and breaking
    them down into implementable components.
    """
    
    def __init__(self):
        """Initialize the RequirementAnalysis with prompt templates."""
        self.extraction_prompt = self._load_extraction_prompt()
        self.categorization_prompt = self._load_categorization_prompt()
        self.dependency_prompt = self._load_dependency_prompt()
        self.prioritization_prompt = self._load_prioritization_prompt()
        self.validation_prompt = self._load_validation_prompt()
    
    def _load_extraction_prompt(self) -> str:
        """Load the prompt template for information extraction."""
        return """
        You are an expert Laravel developer tasked with extracting structured information from software requirements. 
        Analyze the following requirements and extract:

        1. Entities (data models) with their attributes
        2. Actions/Operations that will be performed
        3. Relationships between entities
        4. Constraints and business rules
        5. Users/Actors involved

        Requirements:
        {requirements}

        Provide your analysis in the following JSON format:
        ```json
        {
          "entities": [
            {
              "name": "Entity name (singular, PascalCase)",
              "attributes": ["attribute1", "attribute2"],
              "description": "Brief description of what this entity represents",
              "related_entities": ["RelatedEntity1", "RelatedEntity2"]
            }
          ],
          "actions": [
            {
              "name": "Action name (verb, camelCase)",
              "description": "Description of the action",
              "actor": "Who/what performs this action",
              "target_entities": ["Entity1", "Entity2"],
              "constraints": ["Constraint 1", "Constraint 2"]
            }
          ],
          "constraints": [
            {
              "description": "Detailed description of the constraint",
              "constraint_type": "business_rule/validation/security/etc",
              "related_entities": ["Entity1", "Entity2"],
              "related_actions": ["action1", "action2"]
            }
          ]
        }
        ```
        
        Focus on extracting information relevant to a Laravel application's design. Consider database models, controllers, services, and user interfaces.
        """
    
    def _load_categorization_prompt(self) -> str:
        """Load the prompt template for requirement categorization."""
        return """
        You are an expert Laravel developer tasked with categorizing software requirements into functional areas.
        Review the extracted information and categorize each component into one of the following types:

        - data_storage: Requirements related to data models, database schema, and persistence
        - user_interaction: Requirements related to UI, forms, and user experience
        - business_logic: Requirements related to business rules, calculations, and processing
        - authentication: Requirements related to user authentication and authorization
        - integration: Requirements related to third-party service integration
        - reporting: Requirements related to data reporting and analytics
        - notification: Requirements related to alerts, emails, and other notifications
        - file_management: Requirements related to file uploads, processing, and storage
        - background_process: Requirements related to queue jobs and scheduled tasks
        - security: Requirements related to data protection and access control
        - performance: Requirements related to system speed and efficiency
        - other: Any requirements that don't fit the above categories

        Extracted Information:
        {extracted_info}

        For each identified component, provide:
        1. A clear title
        2. The appropriate category
        3. A priority level (critical, high, medium, low)
        4. An estimated complexity (1-5 scale)

        Provide your categorization in the following JSON format:
        ```json
        {
          "components": [
            {
              "id": "REQ-001",
              "title": "Concise title for the requirement",
              "description": "Detailed description of what needs to be implemented",
              "requirement_type": "category_from_the_list_above",
              "priority": "high/medium/low/critical",
              "entities": ["Entity1", "Entity2"],
              "actions": ["action1", "action2"],
              "constraints": ["constraint1", "constraint2"],
              "estimated_complexity": 3,
              "notes": "Any additional information or considerations"
            }
          ]
        }
        ```
        
        Group related functionalities into single components when appropriate. Ensure each component is specific enough to be implemented independently.
        """
    
    def _load_dependency_prompt(self) -> str:
        """Load the prompt template for identifying technical dependencies."""
        return """
        You are an expert Laravel developer tasked with identifying technical dependencies between requirement components.
        Review the categorized components and identify which ones must be implemented before others.

        Categorized Components:
        {categorized_components}

        For each component, identify any dependencies it has on other components. Consider:
        1. Data dependencies (one component needs data created by another)
        2. Functional dependencies (one component builds upon functionality in another)
        3. Technical dependencies (one component requires infrastructure established by another)

        Provide your dependency analysis in the following JSON format:
        ```json
        {
          "dependencies": [
            {
              "source_id": "REQ-002",
              "target_id": "REQ-001",
              "dependency_type": "data/functional/technical",
              "description": "REQ-002 depends on REQ-001 because..."
            }
          ]
        }
        ```
        
        Ensure you identify all critical dependencies that would block implementation if not addressed in the correct order.
        """
    
    def _load_prioritization_prompt(self) -> str:
        """Load the prompt template for implementation order prioritization."""
        return """
        You are an expert Laravel developer tasked with determining the optimal implementation order for software requirements.
        Using the components and their dependencies, suggest an implementation order that:

        1. Respects all identified dependencies
        2. Prioritizes critical components first
        3. Groups related components when possible for efficiency
        4. Considers complexity and risk in sequencing

        Components and Dependencies:
        {components_and_dependencies}

        Provide your suggested implementation order in the following JSON format:
        ```json
        {
          "suggested_implementation_order": ["REQ-001", "REQ-003", "REQ-002"],
          "technical_considerations": [
            "Consider implementing the database migrations early to establish the data structure",
            "Authentication should be implemented before user-specific features",
            "Third-party integrations should be tested with mock data before connecting to production APIs"
          ]
        }
        ```
        
        Include technical considerations that explain your reasoning and provide guidance for the implementation process.
        """
    
    def _load_validation_prompt(self) -> str:
        """Load the prompt template for requirement validation."""
        return """
        You are an expert Laravel developer tasked with validating a requirement analysis for completeness and consistency.
        Review the complete analysis and check for:

        1. Missing or incomplete requirements
        2. Inconsistencies or contradictions
        3. Ambiguous specifications
        4. Technical feasibility issues
        5. Potential scalability concerns

        Complete Analysis:
        {complete_analysis}

        Provide your validation in the following format:
        ```json
        {
          "is_valid": true/false,
          "issues": [
            {
              "issue_type": "missing_requirement/inconsistency/ambiguity/technical_concern",
              "description": "Detailed description of the issue",
              "related_components": ["REQ-001", "REQ-002"],
              "suggested_resolution": "How to address this issue"
            }
          ],
          "recommended_changes": [
            "Specific change recommendation 1",
            "Specific change recommendation 2"
          ]
        }
        ```
        
        Be thorough in your validation to ensure the requirements are ready for implementation.
        """
    
    def analyze_requirements(self, requirements: str) -> RequirementAnalysisResult:
        """
        Analyze software requirements and break them down into implementable components.
        
        Args:
            requirements: The raw requirements text to analyze
            
        Returns:
            A complete analysis result with components, entities, and implementation order
        """
        # Step 1: Extract structured information from requirements
        extracted_info = self._extract_information(requirements)
        
        # Step 2: Categorize requirements into functional areas
        categorized_components = self._categorize_requirements(extracted_info)
        
        # Step 3: Identify technical dependencies between components
        dependencies = self._identify_dependencies(categorized_components)
        
        # Step 4: Update components with dependencies
        updated_components = self._update_components_with_dependencies(categorized_components, dependencies)
        
        # Step 5: Determine optimal implementation order
        implementation_order, considerations = self._determine_implementation_order(updated_components)
        
        # Step 6: Validate the complete analysis
        validation_result = self._validate_analysis(updated_components, implementation_order, considerations)
        
        # If validation finds issues, incorporate the feedback
        if validation_result.get("is_valid", True) is False:
            updated_components = self._incorporate_validation_feedback(
                updated_components, validation_result
            )
            # Recalculate implementation order with updated components
            implementation_order, considerations = self._determine_implementation_order(updated_components)
        
        # Step 7: Create the final analysis result
        analysis_result = RequirementAnalysisResult(
            components=updated_components,
            entities=extracted_info.get("entities", []),
            suggested_implementation_order=implementation_order,
            technical_considerations=considerations
        )
        
        return analysis_result
    
    def _extract_information(self, requirements: str) -> Dict[str, Any]:
        """
        Extract structured information from the requirements text.
        
        This would use the LLM with the extraction prompt in a real implementation.
        For now, we'll return a simplified example.
        """
        # In a real implementation, this would use an LLM with the extraction prompt
        # For now, return a simplified mock result
        return {
            "entities": [
                {
                    "name": "User",
                    "attributes": ["name", "email", "password"],
                    "description": "Application user",
                    "related_entities": ["Profile", "Order"]
                },
                {
                    "name": "Product",
                    "attributes": ["name", "description", "price", "stock"],
                    "description": "Product available for purchase",
                    "related_entities": ["Category", "Order"]
                }
            ],
            "actions": [
                {
                    "name": "registerUser",
                    "description": "Register a new user in the system",
                    "actor": "Guest",
                    "target_entities": ["User"],
                    "constraints": ["Email must be unique", "Password must be strong"]
                }
            ],
            "constraints": [
                {
                    "description": "Email must be unique in the system",
                    "constraint_type": "validation",
                    "related_entities": ["User"],
                    "related_actions": ["registerUser"]
                }
            ]
        }
    
    def _categorize_requirements(self, extracted_info: Dict[str, Any]) -> List[RequirementComponent]:
        """
        Categorize requirements into functional areas based on extracted information.
        
        This would use the LLM with the categorization prompt in a real implementation.
        For now, we'll return a simplified example.
        """
        # In a real implementation, this would use an LLM with the categorization prompt
        # For now, return simplified mock components
        return [
            RequirementComponent(
                id="REQ-001",
                title="User Registration System",
                description="Implement user registration with email validation",
                requirement_type=RequirementType.AUTHENTICATION,
                priority=RequirementPriority.HIGH,
                entities=[RequirementEntity(name="User", attributes=["name", "email", "password"])],
                actions=[
                    RequirementAction(
                        name="registerUser",
                        description="Register a new user in the system",
                        actor="Guest",
                        target_entities=["User"],
                        constraints=["Email must be unique"]
                    )
                ],
                constraints=[
                    RequirementConstraint(
                        description="Email must be unique in the system",
                        constraint_type="validation",
                        related_entities=["User"],
                        related_actions=["registerUser"]
                    )
                ],
                estimated_complexity=2
            )
        ]
    
    def _identify_dependencies(self, categorized_components: List[RequirementComponent]) -> List[RequirementDependency]:
        """
        Identify technical dependencies between requirement components.
        
        This would use the LLM with the dependency prompt in a real implementation.
        For now, we'll return a simplified example.
        """
        # In a real implementation, this would use an LLM with the dependency prompt
        # For now, return simplified mock dependencies
        return [
            RequirementDependency(
                source_id="REQ-002",
                target_id="REQ-001",
                dependency_type="functional",
                description="User authentication must be implemented before user profiles"
            )
        ]
    
    def _update_components_with_dependencies(
        self, 
        components: List[RequirementComponent],
        dependencies: List[RequirementDependency]
    ) -> List[RequirementComponent]:
        """
        Update components with their identified dependencies.
        
        Args:
            components: The categorized requirement components
            dependencies: The identified dependencies between components
            
        Returns:
            Updated components with dependency information
        """
        # Create a mapping of component IDs to components for easy access
        component_map = {component.id: component for component in components}
        
        # Group dependencies by source component
        dependency_map = {}
        for dependency in dependencies:
            if dependency.source_id not in dependency_map:
                dependency_map[dependency.source_id] = []
            dependency_map[dependency.source_id].append(dependency)
        
        # Update each component with its dependencies
        for component_id, deps in dependency_map.items():
            if component_id in component_map:
                component_map[component_id].dependencies = deps
        
        return list(component_map.values())
    
    def _determine_implementation_order(
        self, 
        components: List[RequirementComponent]
    ) -> Tuple[List[str], List[str]]:
        """
        Determine the optimal implementation order based on dependencies and priorities.
        
        This would use the LLM with the prioritization prompt in a real implementation.
        For now, we'll implement a simplified algorithm.
        
        Args:
            components: The requirement components with dependencies
            
        Returns:
            A tuple of (ordered component IDs, technical considerations)
        """
        # Create a dependency graph
        dependency_graph = {}
        for component in components:
            dependency_graph[component.id] = []
            
        for component in components:
            for dependency in component.dependencies:
                if dependency.target_id in dependency_graph:
                    dependency_graph[dependency.source_id].append(dependency.target_id)
        
        # Perform a simple topological sort with priority considerations
        visited = set()
        result = []
        
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            
            # Visit dependencies first
            for dependency in dependency_graph.get(node, []):
                dfs(dependency)
            
            result.append(node)
        
        # Sort components by priority to process highest priority first
        sorted_components = sorted(
            components, 
            key=lambda c: [
                # Order by priority (CRITICAL first)
                {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(c.priority, 4),
                # Then by complexity (less complex first)
                c.estimated_complexity
            ]
        )
        
        # Process components in priority order
        for component in sorted_components:
            dfs(component.id)
        
        # Technical considerations
        considerations = [
            "Database migrations should be created and run first to establish the data structure",
            "Authentication features should be implemented before user-specific functionality",
            "Core business logic should be implemented before peripheral features",
            "Consider creating interfaces and contracts for external services early"
        ]
        
        return result, considerations
    
    def _validate_analysis(
        self,
        components: List[RequirementComponent],
        implementation_order: List[str],
        considerations: List[str]
    ) -> Dict[str, Any]:
        """
        Validate the complete analysis for completeness and consistency.
        
        This would use the LLM with the validation prompt in a real implementation.
        For now, we'll return a simplified result.
        
        Args:
            components: The requirement components
            implementation_order: The suggested implementation order
            considerations: Technical considerations for implementation
            
        Returns:
            Validation result with any issues and recommendations
        """
        # In a real implementation, this would use an LLM with the validation prompt
        # For now, return a simplified mock validation
        return {
            "is_valid": True,
            "issues": [],
            "recommended_changes": []
        }
    
    def _incorporate_validation_feedback(
        self,
        components: List[RequirementComponent],
        validation_result: Dict[str, Any]
    ) -> List[RequirementComponent]:
        """
        Incorporate validation feedback into the components.
        
        Args:
            components: The original requirement components
            validation_result: The validation result with issues and recommendations
            
        Returns:
            Updated components with validation feedback incorporated
        """
        # In a real implementation, this would modify the components based on validation feedback
        # For now, return the original components
        return components
    
    def generate_breakdown_output(self, analysis_result: RequirementAnalysisResult) -> str:
        """
        Generate a formatted output of the requirement breakdown.
        
        Args:
            analysis_result: The complete requirement analysis result
            
        Returns:
            A formatted string representation of the breakdown
        """
        output = []
        
        # Project overview
        output.append("# Requirement Analysis Breakdown")
        output.append("\n## Project Overview")
        output.append("\nThis analysis breaks down the requirements into implementable components and suggests an implementation order.")
        
        # Entities section
        output.append("\n## Identified Entities")
        for entity in analysis_result.entities:
            output.append(f"\n### {entity.name}")
            output.append(f"Description: {entity.description or 'No description provided'}")
            if entity.attributes:
                output.append("\nAttributes:")
                for attr in entity.attributes:
                    output.append(f"- {attr}")
            if entity.related_entities:
                output.append("\nRelated to:")
                for related in entity.related_entities:
                    output.append(f"- {related}")
            output.append("")
        
        # Components section
        output.append("\n## Requirement Components")
        for component in analysis_result.components:
            output.append(f"\n### {component.id}: {component.title}")
            output.append(f"Type: {component.requirement_type.value}")
            output.append(f"Priority: {component.priority.value}")
            output.append(f"Complexity: {component.estimated_complexity}/5")
            output.append(f"\nDescription: {component.description}")
            
            # Dependencies
            if component.dependencies:
                output.append("\nDependencies:")
                for dep in component.dependencies:
                    output.append(f"- Depends on {dep.target_id}: {dep.description}")
            
            # Entities involved
            if component.entities:
                output.append("\nEntities involved:")
                for entity in component.entities:
                    output.append(f"- {entity.name}")
            
            # Actions
            if component.actions:
                output.append("\nActions:")
                for action in component.actions:
                    output.append(f"- {action.name}: {action.description}")
            
            # Constraints
            if component.constraints:
                output.append("\nConstraints:")
                for constraint in component.constraints:
                    output.append(f"- {constraint.description}")
            
            # Notes
            if component.notes:
                output.append(f"\nNotes: {component.notes}")
                
            output.append("")
        
        # Implementation order
        output.append("\n## Suggested Implementation Order")
        for i, component_id in enumerate(analysis_result.suggested_implementation_order, 1):
            # Find the component
            component = next((c for c in analysis_result.components if c.id == component_id), None)
            if component:
                output.append(f"{i}. [{component_id}] {component.title} (Priority: {component.priority.value})")
        
        # Technical considerations
        output.append("\n## Technical Considerations")
        for consideration in analysis_result.technical_considerations:
            output.append(f"- {consideration}")
        
        return "\n".join(output) 