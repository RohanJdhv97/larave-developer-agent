"""
FilamentPHP Table Builder expertise module.

This module provides templates and utilities for generating FilamentPHP tables
following best practices and coding standards.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class TableComponentTemplate(BaseModel):
    """Template for FilamentPHP table components."""
    name: str
    description: str
    template: str
    example: str
    tags: List[str] = Field(default_factory=list)


class FilamentTableExpertise:
    """
    FilamentPHP Table expertise.
    
    This class provides templates and utilities for generating FilamentPHP tables
    following best practices and coding standards.
    """
    
    def __init__(self):
        """Initialize the FilamentPHP Table expertise module."""
        self.templates = self._load_templates()
        self.table_components = self._load_table_components()
        
    def _load_templates(self) -> Dict[str, TableComponentTemplate]:
        """Load the table templates."""
        templates = {}
        
        # Basic table template
        templates["basic_table"] = TableComponentTemplate(
            name="Basic Table",
            description="Template for a basic FilamentPHP table.",
            template="""<?php

namespace {namespace};

use Filament\\Tables;
use Filament\\Tables\\Columns\\TextColumn;
{additional_imports}

class {class_name} extends {parent_class}
{
    protected function getTableQuery()
    {
        return {model}::query(){query_constraints};
    }
    
    protected function getTableColumns(): array
    {
        return [
{table_columns}
        ];
    }
    
    protected function getTableFilters(): array
    {
        return [
{table_filters}
        ];
    }
    
    protected function getTableActions(): array
    {
        return [
{table_actions}
        ];
    }
    
    protected function getTableBulkActions(): array
    {
        return [
{bulk_actions}
        ];
    }
}
""",
            example="""<?php

namespace App\\Filament\\Resources\\UserResource\\Pages;

use App\\Models\\User;
use Filament\\Tables;
use Filament\\Tables\\Columns\\TextColumn;
use Filament\\Resources\\Pages\\ListRecords;
use Illuminate\\Database\\Eloquent\\Builder;

class ListUsers extends ListRecords
{
    protected function getTableQuery()
    {
        return User::query()->latest();
    }
    
    protected function getTableColumns(): array
    {
        return [
            TextColumn::make('name')
                ->searchable()
                ->sortable(),
            TextColumn::make('email')
                ->searchable()
                ->sortable(),
            TextColumn::make('email_verified_at')
                ->dateTime()
                ->sortable(),
            TextColumn::make('created_at')
                ->dateTime()
                ->sortable(),
        ];
    }
    
    protected function getTableFilters(): array
    {
        return [
            Tables\\Filters\\Filter::make('verified')
                ->query(fn (Builder $query): Builder => $query->whereNotNull('email_verified_at')),
        ];
    }
    
    protected function getTableActions(): array
    {
        return [
            Tables\\Actions\\EditAction::make(),
            Tables\\Actions\\DeleteAction::make(),
        ];
    }
    
    protected function getTableBulkActions(): array
    {
        return [
            Tables\\Actions\\DeleteBulkAction::make(),
        ];
    }
}
""",
            tags=["table", "filament", "php"]
        )
        
        return templates
    
    def _load_table_components(self) -> Dict[str, Dict[str, str]]:
        """Load table component templates."""
        return {
            "columns": {
                "text": """TextColumn::make('{name}')
    ->label('{label}')
    {searchable}
    {sortable}
    {additional_options}""",
                
                "text_badge": """TextColumn::make('{name}')
    ->label('{label}')
    ->badge()
    ->color('{color}')
    {additional_options}""",
                
                "boolean": """BooleanColumn::make('{name}')
    ->label('{label}')
    {additional_options}""",
                
                "image": """ImageColumn::make('{name}')
    ->label('{label}')
    {additional_options}""",
                
                "icon": """IconColumn::make('{name}')
    ->label('{label}')
    ->options({options})
    {additional_options}""",
                
                "enum": """TextColumn::make('{name}')
    ->label('{label}')
    ->enum({enum})
    {additional_options}""",
                
                "date": """TextColumn::make('{name}')
    ->label('{label}')
    ->date('{format}')
    {additional_options}""",
                
                "date_time": """TextColumn::make('{name}')
    ->label('{label}')
    ->dateTime('{format}')
    {additional_options}""",
                
                "currency": """TextColumn::make('{name}')
    ->label('{label}')
    ->money('{currency}')
    {additional_options}""",
                
                "view": """ViewColumn::make('{name}')
    ->label('{label}')
    ->view('{view}')
    {additional_options}""",
            },
            "filters": {
                "select": """SelectFilter::make('{name}')
    ->label('{label}')
    ->options({options})
    {additional_options}""",
                
                "boolean": """BooleanFilter::make('{name}')
    ->label('{label}')
    {additional_options}""",
                
                "multi_select": """MultiSelectFilter::make('{name}')
    ->label('{label}')
    ->options({options})
    {additional_options}""",
                
                "date_range": """Filter::make('{name}')
    ->label('{label}')
    ->form([
        DatePicker::make('from'),
        DatePicker::make('until'),
    ])
    ->query(function (Builder $query, array $data): Builder {
        return $query
            ->when(
                $data['from'],
                fn (Builder $query, $date): Builder => $query->whereDate('{column}', '>=', $date),
            )
            ->when(
                $data['until'],
                fn (Builder $query, $date): Builder => $query->whereDate('{column}', '<=', $date),
            );
    })
    {additional_options}""",
                
                "relationship_select": """SelectFilter::make('{name}')
    ->label('{label}')
    ->relationship('{relationship}', '{column}')
    {additional_options}""",
            },
            "actions": {
                "edit": """EditAction::make()
    {additional_options}""",
                
                "view": """ViewAction::make()
    {additional_options}""",
                
                "delete": """DeleteAction::make()
    {additional_options}""",
                
                "custom": """Action::make('{name}')
    ->label('{label}')
    ->icon('{icon}')
    ->action(function ({action_parameters}) {
        {action_code}
    })
    {additional_options}""",
                
                "url": """Action::make('{name}')
    ->label('{label}')
    ->url('{url}')
    ->openUrlInNewTab({new_tab})
    {additional_options}""",
            },
            "bulk_actions": {
                "delete": """DeleteBulkAction::make()
    {additional_options}""",
                
                "custom": """BulkAction::make('{name}')
    ->label('{label}')
    ->action(function (Collection $records) {
        {action_code}
    })
    {additional_options}""",
            }
        }
    
    def get_template(self, template_name: str) -> Optional[TableComponentTemplate]:
        """Get a specific table template."""
        return self.templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, TableComponentTemplate]:
        """Get all table templates."""
        return self.templates
    
    def get_table_component(self, category: str, component_name: str) -> Optional[str]:
        """Get a specific table component template."""
        category_components = self.table_components.get(category)
        if category_components:
            return category_components.get(component_name)
        return None
    
    def get_category_components(self, category: str) -> Dict[str, str]:
        """Get all components for a specific category."""
        return self.table_components.get(category, {})
    
    def get_all_table_components(self) -> Dict[str, Dict[str, str]]:
        """Get all table component templates."""
        return self.table_components
    
    def generate_table(self, class_name: str, model: str, 
                       namespace: str = "App\\Filament\\Tables", 
                       parent_class: str = "Component",
                       query_constraints: str = None,
                       table_columns: str = None,
                       table_filters: str = None,
                       table_actions: str = None,
                       bulk_actions: str = None,
                       additional_imports: str = None) -> str:
        """
        Generate a FilamentPHP table.
        
        Args:
            class_name: The class name
            model: The model class
            namespace: The namespace
            parent_class: The parent class
            query_constraints: Additional query constraints
            table_columns: The table columns definition
            table_filters: The table filters definition
            table_actions: The table actions definition
            bulk_actions: The bulk actions definition
            additional_imports: Additional import statements
            
        Returns:
            The generated FilamentPHP table as a string
        """
        template = self.get_template("basic_table")
        if not template:
            return "Error: Basic table template not found"
            
        return template.template.format(
            class_name=class_name,
            namespace=namespace,
            parent_class=parent_class,
            model=model,
            query_constraints=query_constraints or '',
            table_columns=table_columns or '            // Table columns here\n',
            table_filters=table_filters or '            // Table filters here\n',
            table_actions=table_actions or '            Tables\\Actions\\EditAction::make(),\n            Tables\\Actions\\DeleteAction::make(),\n',
            bulk_actions=bulk_actions or '            Tables\\Actions\\DeleteBulkAction::make(),\n',
            additional_imports=additional_imports or ''
        )
    
    def generate_table_column(self, column_type: str, name: str, label: str = None, **kwargs) -> str:
        """
        Generate a FilamentPHP table column.
        
        Args:
            column_type: The type of column
            name: The name of the column
            label: The label for the column
            **kwargs: Additional column options
            
        Returns:
            The generated table column as a string
        """
        column_template = self.get_table_component("columns", column_type)
        if not column_template:
            return f"// Error: Table column template '{column_type}' not found"
            
        if not label:
            label = name.replace('_', ' ').title()
            
        # Process options based on column type
        if "searchable" in kwargs and kwargs["searchable"]:
            kwargs["searchable"] = "->searchable()"
        else:
            kwargs["searchable"] = ""
            
        if "sortable" in kwargs and kwargs["sortable"]:
            kwargs["sortable"] = "->sortable()"
        else:
            kwargs["sortable"] = ""
            
        # Process additional options
        additional_options = ""
        if "additional_options" in kwargs:
            additional_options = kwargs["additional_options"]
            
        # Format the column
        return column_template.format(
            name=name,
            label=label,
            **kwargs,
            additional_options=additional_options
        )
    
    def generate_table_filter(self, filter_type: str, name: str, label: str = None, **kwargs) -> str:
        """
        Generate a FilamentPHP table filter.
        
        Args:
            filter_type: The type of filter
            name: The name of the filter
            label: The label for the filter
            **kwargs: Additional filter options
            
        Returns:
            The generated table filter as a string
        """
        filter_template = self.get_table_component("filters", filter_type)
        if not filter_template:
            return f"// Error: Table filter template '{filter_type}' not found"
            
        if not label:
            label = name.replace('_', ' ').title()
            
        # Process additional options
        additional_options = ""
        if "additional_options" in kwargs:
            additional_options = kwargs["additional_options"]
            
        # Format the filter
        return filter_template.format(
            name=name,
            label=label,
            **kwargs,
            additional_options=additional_options
        )
    
    def generate_table_action(self, action_type: str, **kwargs) -> str:
        """
        Generate a FilamentPHP table action.
        
        Args:
            action_type: The type of action
            **kwargs: Additional action options
            
        Returns:
            The generated table action as a string
        """
        action_template = self.get_table_component("actions", action_type)
        if not action_template:
            return f"// Error: Table action template '{action_type}' not found"
            
        # Process additional options
        additional_options = ""
        if "additional_options" in kwargs:
            additional_options = kwargs["additional_options"]
            
        # Format the action
        return action_template.format(
            **kwargs,
            additional_options=additional_options
        )
    
    def generate_bulk_action(self, action_type: str, **kwargs) -> str:
        """
        Generate a FilamentPHP bulk action.
        
        Args:
            action_type: The type of bulk action
            **kwargs: Additional bulk action options
            
        Returns:
            The generated bulk action as a string
        """
        bulk_action_template = self.get_table_component("bulk_actions", action_type)
        if not bulk_action_template:
            return f"// Error: Bulk action template '{action_type}' not found"
            
        # Process additional options
        additional_options = ""
        if "additional_options" in kwargs:
            additional_options = kwargs["additional_options"]
            
        # Format the bulk action
        return bulk_action_template.format(
            **kwargs,
            additional_options=additional_options
        )
    
    def analyze_model_for_table(self, model_code: str) -> Dict[str, Any]:
        """
        Analyze Laravel model code to extract data for table generation.
        
        Args:
            model_code: The Laravel model code to analyze
            
        Returns:
            A dictionary with extracted model data for table generation
        """
        # This would be a more complex implementation to extract properties, relationships, etc.
        # from model code for table generation
        # Simplified implementation for now
        return {
            "model_name": "ExtractedModel",
            "table_fields": [],
            "relationships": [],
        }
    
    def suggest_table_columns(self, model_data: Dict[str, Any]) -> str:
        """
        Suggest table columns based on model data.
        
        Args:
            model_data: The extracted model data
            
        Returns:
            A string with suggested table columns
        """
        # This would generate appropriate table columns based on model attributes
        return "            // Suggested table columns here\n" 