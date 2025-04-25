"""
Project context store for Laravel projects.

This module provides a data structure and utilities for storing
and maintaining information about Laravel projects.
"""

from typing import Dict, List, Any, Optional, Set
from pydantic import BaseModel, Field
from datetime import datetime
import json
import os

class LaravelPackage(BaseModel):
    """Model representing a Laravel/PHP package."""
    name: str
    version: str
    description: Optional[str] = None
    is_dev: bool = False

class LaravelModel(BaseModel):
    """Model representing a Laravel Eloquent model."""
    name: str
    table_name: str
    fillable: List[str] = Field(default_factory=list)
    relationships: Dict[str, str] = Field(default_factory=dict)  # name: relation_type
    has_timestamps: bool = True
    
class DatabaseTable(BaseModel):
    """Model representing a database table in a Laravel project."""
    name: str
    columns: Dict[str, str] = Field(default_factory=dict)  # column_name: column_type
    indexes: List[str] = Field(default_factory=list)
    has_timestamps: bool = True

class LaravelProjectContext(BaseModel):
    """
    Storage for Laravel project context information.
    
    This class maintains persistent information about the Laravel project
    being worked on, including framework version, config, models, etc.
    """
    
    # Basic project information
    name: str = "Laravel Project"
    description: Optional[str] = None
    laravel_version: str = "10.x"
    php_version: str = "8.2"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Project structure
    using_filament: bool = False
    using_pest: bool = False
    using_inertia: bool = False
    using_livewire: bool = False
    
    # Package information
    packages: List[LaravelPackage] = Field(default_factory=list)
    
    # Database and models
    models: Dict[str, LaravelModel] = Field(default_factory=dict)
    tables: Dict[str, DatabaseTable] = Field(default_factory=dict)
    
    # Config and environment
    environment_variables: Dict[str, str] = Field(default_factory=dict)
    config_values: Dict[str, Any] = Field(default_factory=dict)
    
    # Project features
    has_authentication: bool = False
    has_api: bool = False
    api_routes: List[str] = Field(default_factory=list)
    web_routes: List[str] = Field(default_factory=list)
    
    def update_project_info(self, **kwargs):
        """Update basic project information."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def add_package(self, name: str, version: str, description: Optional[str] = None, is_dev: bool = False):
        """Add a package to the project context."""
        package = LaravelPackage(
            name=name,
            version=version,
            description=description,
            is_dev=is_dev
        )
        
        # Replace if exists, otherwise append
        for i, pkg in enumerate(self.packages):
            if pkg.name == name:
                self.packages[i] = package
                return
        
        self.packages.append(package)
        self.updated_at = datetime.now()
    
    def add_model(self, name: str, table_name: str, fillable: List[str] = None, 
                  relationships: Dict[str, str] = None, has_timestamps: bool = True):
        """Add a model to the project context."""
        model = LaravelModel(
            name=name,
            table_name=table_name,
            fillable=fillable or [],
            relationships=relationships or {},
            has_timestamps=has_timestamps
        )
        
        self.models[name] = model
        self.updated_at = datetime.now()
    
    def add_table(self, name: str, columns: Dict[str, str] = None, 
                 indexes: List[str] = None, has_timestamps: bool = True):
        """Add a database table to the project context."""
        table = DatabaseTable(
            name=name,
            columns=columns or {},
            indexes=indexes or [],
            has_timestamps=has_timestamps
        )
        
        self.tables[name] = table
        self.updated_at = datetime.now()
    
    def get_model(self, name: str) -> Optional[LaravelModel]:
        """Get a model by name."""
        return self.models.get(name)
    
    def get_table(self, name: str) -> Optional[DatabaseTable]:
        """Get a table by name."""
        return self.tables.get(name)
    
    def get_package(self, name: str) -> Optional[LaravelPackage]:
        """Get a package by name."""
        for package in self.packages:
            if package.name == name:
                return package
        return None
    
    def get_database_schema(self) -> Dict[str, Any]:
        """Get the full database schema."""
        return {name: table.dict() for name, table in self.tables.items()}
    
    def get_models_schema(self) -> Dict[str, Any]:
        """Get the full models schema."""
        return {name: model.dict() for name, model in self.models.items()}
    
    def save(self, path: str = "project_context.json"):
        """Save the project context to a JSON file."""
        # Convert to dict and handle datetime serialization
        data = self.dict()
        data["created_at"] = data["created_at"].isoformat()
        data["updated_at"] = data["updated_at"].isoformat()
        
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls, path: str = "project_context.json") -> "LaravelProjectContext":
        """Load the project context from a JSON file."""
        if not os.path.exists(path):
            return cls()
            
        with open(path, "r") as f:
            data = json.load(f)
            
        # Convert string dates back to datetime
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        return cls(**data)
    
    def get_context_summary(self) -> str:
        """
        Get a text summary of the project context.
        
        Returns:
            A string summarizing the key aspects of the project context.
        """
        summary = [
            f"Project: {self.name} (Laravel {self.laravel_version}, PHP {self.php_version})",
        ]
        
        # Add framework information
        frameworks = []
        if self.using_filament:
            frameworks.append("Filament")
        if self.using_pest:
            frameworks.append("Pest")
        if self.using_inertia:
            frameworks.append("Inertia.js")
        if self.using_livewire:
            frameworks.append("Livewire")
            
        if frameworks:
            summary.append(f"Frameworks: {', '.join(frameworks)}")
            
        # Add model information
        if self.models:
            summary.append(f"Models: {', '.join(self.models.keys())}")
            
        # Add table information
        if self.tables:
            summary.append(f"Tables: {', '.join(self.tables.keys())}")
            
        # Add package information
        if self.packages:
            summary.append(f"Packages: {len(self.packages)}")
            
        # Add feature information
        features = []
        if self.has_authentication:
            features.append("Authentication")
        if self.has_api:
            features.append("API")
            
        if features:
            summary.append(f"Features: {', '.join(features)}")
            
        return "\n".join(summary) 