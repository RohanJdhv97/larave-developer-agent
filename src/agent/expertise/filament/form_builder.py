"""
FilamentPHP Form Builder expertise module.

This module provides templates and utilities for generating FilamentPHP forms
following best practices and coding standards.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class FormComponentTemplate(BaseModel):
    """Template for FilamentPHP form components."""
    name: str
    description: str
    template: str
    example: str
    tags: List[str] = Field(default_factory=list)


class FilamentFormExpertise:
    """
    FilamentPHP Form expertise.
    
    This class provides templates and utilities for generating FilamentPHP forms
    following best practices and coding standards.
    """
    
    def __init__(self):
        """Initialize the FilamentPHP Form expertise module."""
        self.templates = self._load_templates()
        self.form_components = self._load_form_components()
        
    def _load_templates(self) -> Dict[str, FormComponentTemplate]:
        """Load the form templates."""
        templates = {}
        
        # Basic form template
        templates["basic_form"] = FormComponentTemplate(
            name="Basic Form",
            description="Template for a basic FilamentPHP form.",
            template="""<?php

namespace {namespace};

use Filament\\Forms;
use Filament\\Forms\\Components\\Card;
{additional_imports}

class {class_name} extends {parent_class}
{
    protected function getFormSchema(): array
    {
        return [
            Card::make()
                ->schema([
{form_components}
                ])
                ->columns({columns}),
{additional_cards}
        ];
    }
}
""",
            example="""<?php

namespace App\\Filament\\Resources\\UserResource\\Pages;

use Filament\\Forms;
use Filament\\Forms\\Components\\Card;
use Filament\\Resources\\Pages\\CreateRecord;

class CreateUser extends CreateRecord
{
    protected function getFormSchema(): array
    {
        return [
            Card::make()
                ->schema([
                    Forms\\Components\\TextInput::make('name')
                        ->required()
                        ->maxLength(255),
                    Forms\\Components\\TextInput::make('email')
                        ->email()
                        ->required()
                        ->maxLength(255)
                        ->unique(),
                    Forms\\Components\\DateTimePicker::make('email_verified_at'),
                    Forms\\Components\\TextInput::make('password')
                        ->password()
                        ->required()
                        ->maxLength(255),
                ])
                ->columns(2),
            Card::make()
                ->schema([
                    Forms\\Components\\Select::make('roles')
                        ->multiple()
                        ->relationship('roles', 'name')
                        ->preload(),
                ])
                ->columns(1),
        ];
    }
}
""",
            tags=["form", "filament", "php"]
        )
        
        return templates
    
    def _load_form_components(self) -> Dict[str, str]:
        """Load form component templates."""
        return {
            "text_input": """Forms\\Components\\TextInput::make('{name}')
    ->label('{label}')
    {additional_options}""",
            
            "text_input_required": """Forms\\Components\\TextInput::make('{name}')
    ->label('{label}')
    ->required()
    ->maxLength({max_length})
    {additional_options}""",
            
            "email": """Forms\\Components\\TextInput::make('{name}')
    ->label('{label}')
    ->email()
    ->required()
    ->maxLength(255)
    {additional_options}""",
            
            "password": """Forms\\Components\\TextInput::make('{name}')
    ->label('{label}')
    ->password()
    ->required()
    ->maxLength(255)
    {visibility_modifier}
    {additional_options}""",
            
            "textarea": """Forms\\Components\\Textarea::make('{name}')
    ->label('{label}')
    ->rows({rows})
    {additional_options}""",
            
            "rich_editor": """Forms\\Components\\RichEditor::make('{name}')
    ->label('{label}')
    {additional_options}""",
            
            "select": """Forms\\Components\\Select::make('{name}')
    ->label('{label}')
    ->options({options})
    {additional_options}""",
            
            "relationship_select": """Forms\\Components\\Select::make('{name}')
    ->label('{label}')
    ->relationship('{relationship}', '{column}')
    {multiple}
    {preload}
    {additional_options}""",
            
            "checkbox": """Forms\\Components\\Checkbox::make('{name}')
    ->label('{label}')
    {additional_options}""",
            
            "toggle": """Forms\\Components\\Toggle::make('{name}')
    ->label('{label}')
    {additional_options}""",
            
            "date_picker": """Forms\\Components\\DatePicker::make('{name}')
    ->label('{label}')
    {additional_options}""",
            
            "date_time_picker": """Forms\\Components\\DateTimePicker::make('{name}')
    ->label('{label}')
    {additional_options}""",
            
            "file_upload": """Forms\\Components\\FileUpload::make('{name}')
    ->label('{label}')
    ->disk('{disk}')
    ->directory('{directory}')
    {additional_options}""",
            
            "repeater": """Forms\\Components\\Repeater::make('{name}')
    ->label('{label}')
    ->schema([
{schema}
    ])
    {additional_options}""",
            
            "group": """Forms\\Components\\Group::make()
    ->schema([
{schema}
    ])
    {additional_options}""",
            
            "fieldset": """Forms\\Components\\Fieldset::make('{name}')
    ->label('{label}')
    ->schema([
{schema}
    ])
    {additional_options}""",
        }
    
    def get_template(self, template_name: str) -> Optional[FormComponentTemplate]:
        """Get a specific form template."""
        return self.templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, FormComponentTemplate]:
        """Get all form templates."""
        return self.templates
    
    def get_form_component(self, component_name: str) -> Optional[str]:
        """Get a specific form component template."""
        return self.form_components.get(component_name)
    
    def get_all_form_components(self) -> Dict[str, str]:
        """Get all form component templates."""
        return self.form_components
    
    def generate_form(self, class_name: str, namespace: str = "App\\Filament\\Forms", 
                      parent_class: str = "Component",
                      form_components: str = None,
                      columns: int = 1,
                      additional_cards: str = None,
                      additional_imports: str = None) -> str:
        """
        Generate a FilamentPHP form.
        
        Args:
            class_name: The class name
            namespace: The namespace
            parent_class: The parent class
            form_components: The form components definition
            columns: The number of columns
            additional_cards: Additional card components
            additional_imports: Additional import statements
            
        Returns:
            The generated FilamentPHP form as a string
        """
        template = self.get_template("basic_form")
        if not template:
            return "Error: Basic form template not found"
            
        return template.template.format(
            class_name=class_name,
            namespace=namespace,
            parent_class=parent_class,
            form_components=form_components or '                    // Form components here\n',
            columns=columns,
            additional_cards=additional_cards or '',
            additional_imports=additional_imports or ''
        )
    
    def generate_form_component(self, component_type: str, name: str, label: str = None, **kwargs) -> str:
        """
        Generate a FilamentPHP form component.
        
        Args:
            component_type: The type of component
            name: The name of the component
            label: The label for the component
            **kwargs: Additional component options
            
        Returns:
            The generated form component as a string
        """
        component_template = self.get_form_component(component_type)
        if not component_template:
            return f"// Error: Form component template '{component_type}' not found"
            
        if not label:
            label = name.replace('_', ' ').title()
            
        # Process options based on component type
        if component_type == "text_input_required" and "max_length" not in kwargs:
            kwargs["max_length"] = 255
            
        if component_type == "password" and "visibility_modifier" not in kwargs:
            kwargs["visibility_modifier"] = "->visibleOn('create')"
            
        if component_type == "textarea" and "rows" not in kwargs:
            kwargs["rows"] = 3
            
        if component_type == "relationship_select":
            if "multiple" in kwargs and kwargs["multiple"]:
                kwargs["multiple"] = "->multiple()"
            else:
                kwargs["multiple"] = ""
                
            if "preload" in kwargs and kwargs["preload"]:
                kwargs["preload"] = "->preload()"
            else:
                kwargs["preload"] = ""
                
        # Process additional options
        additional_options = ""
        if "additional_options" in kwargs:
            additional_options = kwargs["additional_options"]
        else:
            additional_options = ""
            
        # Format the component
        return component_template.format(
            name=name,
            label=label,
            **kwargs,
            additional_options=additional_options
        )
    
    def analyze_model_for_form(self, model_code: str) -> Dict[str, Any]:
        """
        Analyze Laravel model code to extract data for form generation.
        
        Args:
            model_code: The Laravel model code to analyze
            
        Returns:
            A dictionary with extracted model data for form generation
        """
        # This would be a more complex implementation to extract properties, rules, etc.
        # from model code for form generation
        # Simplified implementation for now
        return {
            "model_name": "ExtractedModel",
            "fillable_fields": [],
            "validations": {},
            "relationships": []
        }
    
    def suggest_form_components(self, model_data: Dict[str, Any]) -> str:
        """
        Suggest form components based on model data.
        
        Args:
            model_data: The extracted model data
            
        Returns:
            A string with suggested form components
        """
        # This would generate appropriate form components based on model attributes
        return "                    // Suggested form components here\n" 