"""
FilamentPHP Resource Builder expertise module.

This module provides templates and utilities for generating FilamentPHP resources
following best practices and coding standards.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class ResourceTemplate(BaseModel):
    """Template for FilamentPHP resources."""
    name: str
    description: str
    template: str
    example: str
    tags: List[str] = Field(default_factory=list)


class FilamentResourceExpertise:
    """
    FilamentPHP Resource expertise.
    
    This class provides templates and utilities for generating FilamentPHP resources
    following best practices and coding standards.
    """
    
    def __init__(self):
        """Initialize the FilamentPHP Resource expertise module."""
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, ResourceTemplate]:
        """Load the resource templates."""
        templates = {}
        
        # Basic resource template
        templates["basic_resource"] = ResourceTemplate(
            name="Basic Resource",
            description="Template for a basic FilamentPHP resource.",
            template="""<?php

namespace App\\Filament\\Resources;

use App\\Filament\\Resources\\{resource_name}Resource\\Pages;
use App\\Models\\{model_name};
use Filament\\Forms;
use Filament\\Resources\\Form;
use Filament\\Resources\\Resource;
use Filament\\Resources\\Table;
use Filament\\Tables;
use Illuminate\\Database\\Eloquent\\Builder;
use Illuminate\\Database\\Eloquent\\SoftDeletingScope;

class {resource_name}Resource extends Resource
{
    protected static ?string $model = {model_name}::class;

    protected static ?string $navigationIcon = '{icon}';
    
    protected static ?string $navigationGroup = '{navigation_group}';
    
    protected static ?int $navigationSort = {navigation_sort};

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
{form_schema}
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
{table_columns}
            ])
            ->filters([
{table_filters}
            ])
            ->actions([
{table_actions}
            ])
            ->bulkActions([
{bulk_actions}
            ]);
    }
    
    public static function getRelations(): array
    {
        return [
{relations}
        ];
    }
    
    public static function getPages(): array
    {
        return [
            'index' => Pages\\List{resource_name}::route('/'),
            'create' => Pages\\Create{resource_name}::route('/create'),
            'edit' => Pages\\Edit{resource_name}::route('/{record}/edit'),
{additional_pages}
        ];
    }    
}
""",
            example="""<?php

namespace App\\Filament\\Resources;

use App\\Filament\\Resources\\UserResource\\Pages;
use App\\Models\\User;
use Filament\\Forms;
use Filament\\Resources\\Form;
use Filament\\Resources\\Resource;
use Filament\\Resources\\Table;
use Filament\\Tables;
use Illuminate\\Database\\Eloquent\\Builder;
use Illuminate\\Database\\Eloquent\\SoftDeletingScope;

class UserResource extends Resource
{
    protected static ?string $model = User::class;

    protected static ?string $navigationIcon = 'heroicon-o-user';
    
    protected static ?string $navigationGroup = 'User Management';
    
    protected static ?int $navigationSort = 1;

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\\Components\\TextInput::make('name')
                    ->required()
                    ->maxLength(255),
                Forms\\Components\\TextInput::make('email')
                    ->email()
                    ->required()
                    ->maxLength(255)
                    ->unique(ignoreRecord: true),
                Forms\\Components\\DateTimePicker::make('email_verified_at'),
                Forms\\Components\\TextInput::make('password')
                    ->password()
                    ->required()
                    ->maxLength(255)
                    ->visibleOn('create'),
                Forms\\Components\\Select::make('roles')
                    ->multiple()
                    ->relationship('roles', 'name')
                    ->preload(),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\\Columns\\TextColumn::make('name')
                    ->searchable(),
                Tables\\Columns\\TextColumn::make('email')
                    ->searchable(),
                Tables\\Columns\\TextColumn::make('email_verified_at')
                    ->dateTime(),
                Tables\\Columns\\TextColumn::make('created_at')
                    ->dateTime(),
            ])
            ->filters([
                Tables\\Filters\\Filter::make('verified')
                    ->query(fn (Builder $query): Builder => $query->whereNotNull('email_verified_at')),
            ])
            ->actions([
                Tables\\Actions\\EditAction::make(),
                Tables\\Actions\\DeleteAction::make(),
            ])
            ->bulkActions([
                Tables\\Actions\\DeleteBulkAction::make(),
            ]);
    }
    
    public static function getRelations(): array
    {
        return [
            //
        ];
    }
    
    public static function getPages(): array
    {
        return [
            'index' => Pages\\ListUsers::route('/'),
            'create' => Pages\\CreateUser::route('/create'),
            'edit' => Pages\\EditUser::route('/{record}/edit'),
        ];
    }    
}
""",
            tags=["resource", "filament", "php"]
        )
        
        return templates
    
    def get_template(self, template_name: str) -> Optional[ResourceTemplate]:
        """Get a specific resource template."""
        return self.templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, ResourceTemplate]:
        """Get all resource templates."""
        return self.templates
    
    def generate_resource(self, model_name: str, resource_name: str = None, 
                         navigation_icon: str = 'heroicon-o-collection',
                         navigation_group: str = None,
                         navigation_sort: int = 10,
                         form_schema: str = None,
                         table_columns: str = None,
                         table_filters: str = None,
                         table_actions: str = None,
                         bulk_actions: str = None,
                         relations: str = None,
                         additional_pages: str = None) -> str:
        """
        Generate a FilamentPHP resource.
        
        Args:
            model_name: The model name
            resource_name: The resource name (defaults to model_name)
            navigation_icon: The navigation icon
            navigation_group: The navigation group
            navigation_sort: The navigation sort order
            form_schema: The form schema definition
            table_columns: The table columns definition
            table_filters: The table filters definition
            table_actions: The table actions definition
            bulk_actions: The bulk actions definition
            relations: The relations definition
            additional_pages: Additional pages definition
            
        Returns:
            The generated FilamentPHP resource as a string
        """
        template = self.get_template("basic_resource")
        if not template:
            return "Error: Basic resource template not found"
            
        if not resource_name:
            resource_name = model_name
        
        return template.template.format(
            model_name=model_name,
            resource_name=resource_name,
            icon=navigation_icon,
            navigation_group=navigation_group or '',
            navigation_sort=navigation_sort,
            form_schema=form_schema or '                //\n',
            table_columns=table_columns or '                //\n',
            table_filters=table_filters or '                //\n',
            table_actions=table_actions or '                Tables\\Actions\\EditAction::make(),\n                Tables\\Actions\\DeleteAction::make(),\n',
            bulk_actions=bulk_actions or '                Tables\\Actions\\DeleteBulkAction::make(),\n',
            relations=relations or '            //\n',
            additional_pages=additional_pages or ''
        )
    
    def analyze_model_for_resource(self, model_code: str) -> Dict[str, Any]:
        """
        Analyze Laravel model code to extract data for resource generation.
        
        Args:
            model_code: The Laravel model code to analyze
            
        Returns:
            A dictionary with extracted model data for resource generation
        """
        # This would be a more complex implementation to extract properties, relationships, etc.
        # from model code for resource generation
        # Simplified implementation for now
        return {
            "model_name": "ExtractedModel",
            "fillable_fields": [],
            "relationships": [],
            "casts": {}
        }
    
    def suggest_form_fields(self, model_data: Dict[str, Any]) -> str:
        """
        Suggest form fields based on model data.
        
        Args:
            model_data: The extracted model data
            
        Returns:
            A string with suggested form fields
        """
        # This would generate appropriate form fields based on model attributes
        return "                // Form fields here\n"
    
    def suggest_table_columns(self, model_data: Dict[str, Any]) -> str:
        """
        Suggest table columns based on model data.
        
        Args:
            model_data: The extracted model data
            
        Returns:
            A string with suggested table columns
        """
        # This would generate appropriate table columns based on model attributes
        return "                // Table columns here\n" 