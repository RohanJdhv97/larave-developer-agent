"""
Database design and schema planning module.

This module provides capabilities for planning database relationships,
recommending indexing strategies, and generating database schemas.
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from pydantic import BaseModel, Field
from enum import Enum

class RelationshipType(str, Enum):
    """Types of database relationships."""
    ONE_TO_ONE = "one_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    MANY_TO_MANY = "many_to_many"

class NormalizationLevel(str, Enum):
    """Database normalization levels."""
    FIRST_NORMAL_FORM = "1NF"
    SECOND_NORMAL_FORM = "2NF"
    THIRD_NORMAL_FORM = "3NF"
    BCNF = "BCNF"

class ColumnType(str, Enum):
    """Common database column types."""
    INTEGER = "integer"
    BIGINT = "bigint"
    VARCHAR = "varchar"
    TEXT = "text"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    TIMESTAMP = "timestamp"
    DECIMAL = "decimal"
    FLOAT = "float"
    JSON = "json"
    ENUM = "enum"

class IndexType(str, Enum):
    """Types of database indexes."""
    PRIMARY = "primary"
    UNIQUE = "unique"
    INDEX = "index"
    FULLTEXT = "fulltext"

class Column(BaseModel):
    """Model representing a database column."""
    name: str
    type: ColumnType
    length: Optional[int] = None
    nullable: bool = False
    default: Optional[Any] = None
    comment: Optional[str] = None

class Index(BaseModel):
    """Model representing a database index."""
    columns: List[str]
    type: IndexType = IndexType.INDEX
    name: Optional[str] = None

class Relationship(BaseModel):
    """Model representing a relationship between tables."""
    source_table: str
    target_table: str
    type: RelationshipType
    source_column: str
    target_column: str
    is_nullable: bool = False
    with_timestamps: bool = False
    with_soft_deletes: bool = False

class Table(BaseModel):
    """Model representing a database table."""
    name: str
    columns: List[Column] = Field(default_factory=list)
    indexes: List[Index] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)
    has_timestamps: bool = True
    has_soft_deletes: bool = False
    description: Optional[str] = None

class DatabaseSchema(BaseModel):
    """Model representing a complete database schema."""
    tables: List[Table] = Field(default_factory=list)
    normalization_level: NormalizationLevel = NormalizationLevel.THIRD_NORMAL_FORM

class DatabasePlanning:
    """
    Provides capabilities for database relationship planning, indexing strategies,
    and schema generation.
    """
    
    def __init__(self):
        """Initialize the DatabasePlanning with prompt templates."""
        self.entity_extraction_prompt = self._load_entity_extraction_prompt()
        self.relationship_planning_prompt = self._load_relationship_planning_prompt()
        self.indexing_prompt = self._load_indexing_prompt()
        self.normalization_prompt = self._load_normalization_prompt()
        self.migration_template = self._load_migration_template()
    
    def _load_entity_extraction_prompt(self) -> str:
        """Load the prompt template for entity extraction."""
        return """
        You are an expert Laravel developer tasked with designing a database schema based on requirement analysis.
        Analyze the extracted entities and their relationships to define database tables.

        Requirements Analysis:
        {requirement_analysis}

        For each entity, determine:
        1. Appropriate table name (snake_case, plural)
        2. All columns with proper types
        3. Primary key strategy
        4. Timestamps and soft delete requirements

        Provide your database design in the following JSON format:
        ```json
        {
          "tables": [
            {
              "name": "users",
              "description": "Stores user account information",
              "columns": [
                {"name": "id", "type": "bigint", "nullable": false},
                {"name": "name", "type": "varchar", "length": 255, "nullable": false},
                {"name": "email", "type": "varchar", "length": 255, "nullable": false},
                {"name": "password", "type": "varchar", "length": 255, "nullable": false},
                {"name": "remember_token", "type": "varchar", "length": 100, "nullable": true},
                {"name": "created_at", "type": "timestamp", "nullable": true},
                {"name": "updated_at", "type": "timestamp", "nullable": true}
              ],
              "has_timestamps": true,
              "has_soft_deletes": false
            }
          ]
        }
        ```
        
        Follow Laravel conventions for table and column naming. Use appropriate column types for each attribute.
        """
    
    def _load_relationship_planning_prompt(self) -> str:
        """Load the prompt template for relationship planning."""
        return """
        You are an expert Laravel developer tasked with defining relationships between database tables.
        Analyze the tables and determine the appropriate relationships between them.

        Tables:
        {tables}

        For each relationship, determine:
        1. The type (one-to-one, one-to-many, many-to-many)
        2. The participating tables
        3. The linking columns
        4. Whether it should be nullable
        5. Any additional pivot table requirements for many-to-many relationships

        Provide your relationship design in the following JSON format:
        ```json
        {
          "relationships": [
            {
              "source_table": "users",
              "target_table": "profiles",
              "type": "one_to_one",
              "source_column": "id",
              "target_column": "user_id",
              "is_nullable": false
            },
            {
              "source_table": "users",
              "target_table": "posts",
              "type": "one_to_many",
              "source_column": "id",
              "target_column": "user_id",
              "is_nullable": false
            },
            {
              "source_table": "posts",
              "target_table": "tags",
              "type": "many_to_many",
              "source_column": "id",
              "target_column": "id",
              "pivot_table": "post_tag",
              "with_timestamps": true
            }
          ]
        }
        ```
        
        Follow Laravel conventions for foreign key naming and relationship definition.
        """
    
    def _load_indexing_prompt(self) -> str:
        """Load the prompt template for indexing strategy."""
        return """
        You are an expert Laravel developer tasked with recommending database indexing strategies.
        Analyze the tables, columns, and relationships to suggest appropriate indexes.

        Database Schema:
        {schema}

        For each table, recommend indexes for:
        1. Foreign keys
        2. Frequently queried columns
        3. Columns used in sorting or filtering
        4. Columns with unique constraints

        Provide your indexing recommendations in the following JSON format:
        ```json
        {
          "indexes": [
            {
              "table": "users",
              "indexes": [
                {"columns": ["email"], "type": "unique", "name": "users_email_unique"},
                {"columns": ["created_at"], "type": "index", "name": "users_created_at_index"}
              ]
            },
            {
              "table": "posts",
              "indexes": [
                {"columns": ["user_id"], "type": "index", "name": "posts_user_id_index"},
                {"columns": ["title"], "type": "index", "name": "posts_title_index"},
                {"columns": ["published_at"], "type": "index", "name": "posts_published_at_index"}
              ]
            }
          ]
        }
        ```
        
        Consider performance implications and only recommend indexes that will provide significant query improvements.
        """
    
    def _load_normalization_prompt(self) -> str:
        """Load the prompt template for normalization recommendations."""
        return """
        You are an expert Laravel developer tasked with ensuring proper database normalization.
        Analyze the current schema design and suggest normalization improvements.

        Current Schema:
        {schema}

        For each table, evaluate:
        1. First Normal Form (1NF): No repeating groups, all values atomic
        2. Second Normal Form (2NF): No partial dependencies on primary key
        3. Third Normal Form (3NF): No transitive dependencies
        4. BCNF: Every determinant is a candidate key

        Provide your normalization recommendations in the following JSON format:
        ```json
        {
          "current_normalization_level": "2NF",
          "recommendations": [
            {
              "table": "users",
              "issues": [
                {
                  "description": "The 'address' column contains multiple pieces of information (street, city, zip)",
                  "resolution": "Create separate columns for address components or create an addresses table"
                }
              ],
              "suggested_schema": {
                "tables": [
                  {
                    "name": "users",
                    "columns": [...],
                    "relationships": [...]
                  },
                  {
                    "name": "addresses",
                    "columns": [...],
                    "relationships": [...]
                  }
                ]
              }
            }
          ]
        }
        ```
        
        Balance normalization principles with practical application needs. Avoid over-normalization for simple cases.
        """
    
    def _load_migration_template(self) -> str:
        """Load the template for Laravel migration files."""
        return """<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('{table_name}', function (Blueprint $table) {
{columns}
{indexes}
{relationships}
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('{table_name}');
    }
};
"""
    
    def plan_database_schema(self, requirement_analysis: Dict[str, Any]) -> DatabaseSchema:
        """
        Plan a database schema based on the requirement analysis.
        
        Args:
            requirement_analysis: The requirement analysis result
            
        Returns:
            A complete database schema design
        """
        # Step 1: Extract entities and define tables
        tables = self._extract_tables(requirement_analysis)
        
        # Step 2: Plan relationships between tables
        tables_with_relationships = self._plan_relationships(tables)
        
        # Step 3: Recommend indexing strategies
        tables_with_indexes = self._recommend_indexes(tables_with_relationships)
        
        # Step 4: Apply normalization recommendations
        normalized_tables, normalization_level = self._apply_normalization(tables_with_indexes)
        
        # Step 5: Create the final schema
        schema = DatabaseSchema(
            tables=normalized_tables,
            normalization_level=normalization_level
        )
        
        return schema
    
    def _extract_tables(self, requirement_analysis: Dict[str, Any]) -> List[Table]:
        """
        Extract tables from the requirement analysis.
        
        This would use the LLM with the entity extraction prompt in a real implementation.
        For now, we'll return a simplified example.
        
        Args:
            requirement_analysis: The requirement analysis result
            
        Returns:
            A list of database tables
        """
        # In a real implementation, this would use an LLM with the entity extraction prompt
        # For now, return simplified mock tables
        return [
            Table(
                name="users",
                description="Stores user account information",
                columns=[
                    Column(name="id", type=ColumnType.BIGINT, nullable=False),
                    Column(name="name", type=ColumnType.VARCHAR, length=255, nullable=False),
                    Column(name="email", type=ColumnType.VARCHAR, length=255, nullable=False),
                    Column(name="password", type=ColumnType.VARCHAR, length=255, nullable=False),
                    Column(name="remember_token", type=ColumnType.VARCHAR, length=100, nullable=True),
                ],
                has_timestamps=True,
                has_soft_deletes=False
            ),
            Table(
                name="profiles",
                description="Stores user profile information",
                columns=[
                    Column(name="id", type=ColumnType.BIGINT, nullable=False),
                    Column(name="user_id", type=ColumnType.BIGINT, nullable=False),
                    Column(name="bio", type=ColumnType.TEXT, nullable=True),
                    Column(name="avatar", type=ColumnType.VARCHAR, length=255, nullable=True),
                ],
                has_timestamps=True,
                has_soft_deletes=False
            )
        ]
    
    def _plan_relationships(self, tables: List[Table]) -> List[Table]:
        """
        Plan relationships between tables.
        
        This would use the LLM with the relationship planning prompt in a real implementation.
        For now, we'll implement a simplified algorithm.
        
        Args:
            tables: The list of database tables
            
        Returns:
            Tables with relationships defined
        """
        # In a real implementation, this would use an LLM with the relationship planning prompt
        # For now, add a simple relationship example
        
        # Create a map of table names for easy lookup
        table_map = {table.name: table for table in tables}
        
        # Add a relationship example (users to profiles)
        if "users" in table_map and "profiles" in table_map:
            relationship = Relationship(
                source_table="users",
                target_table="profiles",
                type=RelationshipType.ONE_TO_ONE,
                source_column="id",
                target_column="user_id",
                is_nullable=False
            )
            
            # Add to the users table
            users_table = table_map["users"]
            users_table.relationships.append(relationship)
            
            # Update in the table_map
            table_map["users"] = users_table
            
            # Convert back to list
            tables = list(table_map.values())
        
        return tables
    
    def _recommend_indexes(self, tables: List[Table]) -> List[Table]:
        """
        Recommend indexing strategies for tables.
        
        This would use the LLM with the indexing prompt in a real implementation.
        For now, we'll implement a simplified algorithm.
        
        Args:
            tables: The list of database tables with relationships
            
        Returns:
            Tables with indexes defined
        """
        # In a real implementation, this would use an LLM with the indexing prompt
        # For now, apply some basic indexing rules
        
        # Create a map of table names for easy lookup
        table_map = {table.name: table for table in tables}
        
        # Process each table
        for table_name, table in table_map.items():
            # Always index foreign keys
            foreign_key_columns = []
            for column in table.columns:
                if column.name.endswith('_id') and column.name != 'id':
                    foreign_key_columns.append(column.name)
            
            # Add indexes for foreign keys
            for fk_column in foreign_key_columns:
                index = Index(
                    columns=[fk_column],
                    type=IndexType.INDEX,
                    name=f"{table_name}_{fk_column}_index"
                )
                table.indexes.append(index)
            
            # Add unique indexes for typically unique columns
            for column in table.columns:
                if column.name in ['email', 'username', 'slug']:
                    index = Index(
                        columns=[column.name],
                        type=IndexType.UNIQUE,
                        name=f"{table_name}_{column.name}_unique"
                    )
                    table.indexes.append(index)
            
            # Update in the table_map
            table_map[table_name] = table
        
        # Convert back to list
        return list(table_map.values())
    
    def _apply_normalization(self, tables: List[Table]) -> Tuple[List[Table], NormalizationLevel]:
        """
        Apply normalization recommendations to tables.
        
        This would use the LLM with the normalization prompt in a real implementation.
        For now, we'll return the tables as is.
        
        Args:
            tables: The list of database tables with relationships and indexes
            
        Returns:
            A tuple of (normalized tables, normalization level)
        """
        # In a real implementation, this would use an LLM with the normalization prompt
        # For now, return the tables as is with 3NF
        return tables, NormalizationLevel.THIRD_NORMAL_FORM
    
    def generate_migration_code(self, table: Table) -> str:
        """
        Generate Laravel migration code for a table.
        
        Args:
            table: The table to generate migration code for
            
        Returns:
            String containing the migration code
        """
        template = self.migration_template
        
        # Generate columns code
        columns_code = []
        
        # Add ID if not explicitly defined
        if not any(column.name == 'id' for column in table.columns):
            columns_code.append("            $table->id();")
        
        # Add other columns
        for column in table.columns:
            if column.name == 'id':
                columns_code.append("            $table->id();")
                continue
                
            # Build column definition
            column_def = f"            $table->{self._map_column_type(column)}"
            
            # Add nullable
            if column.nullable:
                column_def += "->nullable()"
            
            # Add default if specified
            if column.default is not None:
                if isinstance(column.default, str):
                    column_def += f"->default('{column.default}')"
                else:
                    column_def += f"->default({column.default})"
            
            # Add comment if specified
            if column.comment:
                column_def += f"->comment('{column.comment}')"
            
            column_def += ";"
            columns_code.append(column_def)
        
        # Add timestamps if needed
        if table.has_timestamps:
            columns_code.append("            $table->timestamps();")
        
        # Add soft deletes if needed
        if table.has_soft_deletes:
            columns_code.append("            $table->softDeletes();")
        
        # Generate indexes code
        indexes_code = []
        for index in table.indexes:
            if len(index.columns) == 1:
                # Single column index
                column = index.columns[0]
                if index.type == IndexType.UNIQUE:
                    indexes_code.append(f"            $table->unique('{column}');")
                elif index.type == IndexType.INDEX:
                    indexes_code.append(f"            $table->index('{column}');")
                elif index.type == IndexType.FULLTEXT:
                    indexes_code.append(f"            $table->fullText('{column}');")
            else:
                # Multi-column index
                columns_string = "', '".join(index.columns)
                if index.type == IndexType.UNIQUE:
                    indexes_code.append(f"            $table->unique(['{columns_string}']);")
                elif index.type == IndexType.INDEX:
                    indexes_code.append(f"            $table->index(['{columns_string}']);")
                elif index.type == IndexType.FULLTEXT:
                    indexes_code.append(f"            $table->fullText(['{columns_string}']);")
        
        # Generate foreign key constraints
        relationships_code = []
        for relationship in table.relationships:
            if relationship.source_table == table.name:
                target_column = relationship.target_column or 'id'
                constraint = f"            $table->foreign('{relationship.source_column}')"
                constraint += f"->references('{target_column}')"
                constraint += f"->on('{relationship.target_table}')"
                
                if relationship.is_nullable:
                    constraint += "->nullOnDelete()"
                else:
                    constraint += "->cascadeOnDelete()"
                
                constraint += ";"
                relationships_code.append(constraint)
        
        # Replace template placeholders
        migration_code = template.replace("{table_name}", table.name)
        migration_code = migration_code.replace("{columns}", "\n".join(columns_code))
        migration_code = migration_code.replace("{indexes}", "\n".join(indexes_code))
        migration_code = migration_code.replace("{relationships}", "\n".join(relationships_code))
        
        return migration_code
    
    def _map_column_type(self, column: Column) -> str:
        """
        Map a column type to Laravel migration column type method.
        
        Args:
            column: The column to map
            
        Returns:
            Laravel migration column type method
        """
        type_map = {
            ColumnType.INTEGER: "integer",
            ColumnType.BIGINT: "bigInteger",
            ColumnType.VARCHAR: f"string('{column.name}'," + (f" {column.length}" if column.length else "") + ")",
            ColumnType.TEXT: "text",
            ColumnType.BOOLEAN: "boolean",
            ColumnType.DATE: "date",
            ColumnType.DATETIME: "datetime",
            ColumnType.TIMESTAMP: "timestamp",
            ColumnType.DECIMAL: "decimal",
            ColumnType.FLOAT: "float",
            ColumnType.JSON: "json",
            ColumnType.ENUM: "enum" # Would need enum values
        }
        
        return type_map.get(column.type, "string")
    
    def generate_schema_output(self, schema: DatabaseSchema) -> str:
        """
        Generate a formatted output of the database schema.
        
        Args:
            schema: The database schema
            
        Returns:
            A formatted string representation of the schema
        """
        output = []
        
        # Schema overview
        output.append("# Database Schema Design")
        output.append(f"\nNormalization Level: {schema.normalization_level.value}")
        
        # Tables section
        output.append("\n## Tables")
        for table in schema.tables:
            output.append(f"\n### {table.name}")
            if table.description:
                output.append(f"Description: {table.description}")
            
            # Columns
            output.append("\n#### Columns")
            for column in table.columns:
                nullable = "NULL" if column.nullable else "NOT NULL"
                default = f" DEFAULT {column.default}" if column.default is not None else ""
                output.append(f"- {column.name}: {column.type.value}" + 
                              (f"({column.length})" if column.length else "") + 
                              f" {nullable}{default}")
            
            # Indexes
            if table.indexes:
                output.append("\n#### Indexes")
                for index in table.indexes:
                    index_type = index.type.value.upper()
                    columns = ", ".join(index.columns)
                    output.append(f"- {index_type} KEY on ({columns})")
            
            # Relationships
            if table.relationships:
                output.append("\n#### Relationships")
                for relationship in table.relationships:
                    rel_type = relationship.type.value.replace("_", " ").title()
                    output.append(f"- {rel_type} relationship with {relationship.target_table}" +
                                  f" ({relationship.source_column} -> {relationship.target_column})")
            
            # Timestamps and soft deletes
            features = []
            if table.has_timestamps:
                features.append("Timestamps (created_at, updated_at)")
            if table.has_soft_deletes:
                features.append("Soft Deletes (deleted_at)")
            
            if features:
                output.append("\n#### Features")
                for feature in features:
                    output.append(f"- {feature}")
        
        # Entity Relationship Diagram (text-based)
        output.append("\n## Entity Relationships")
        output.append("\n```")
        
        # Create a simple text-based ERD
        erd_tables = {}
        for table in schema.tables:
            columns = [column.name for column in table.columns]
            erd_tables[table.name] = columns
        
        # Draw ERD tables
        for table_name, columns in erd_tables.items():
            output.append(f"+------------------+")
            output.append(f"| {table_name.upper().ljust(16)} |")
            output.append(f"+------------------+")
            for column in columns:
                output.append(f"| {column.ljust(16)} |")
            output.append(f"+------------------+")
            output.append("")
        
        # Draw relationships
        output.append("Relationships:")
        for table in schema.tables:
            for relationship in table.relationships:
                rel_symbol = {
                    RelationshipType.ONE_TO_ONE: "1:1",
                    RelationshipType.ONE_TO_MANY: "1:n",
                    RelationshipType.MANY_TO_ONE: "n:1",
                    RelationshipType.MANY_TO_MANY: "n:m"
                }.get(relationship.type, "")
                
                output.append(f"{relationship.source_table}.{relationship.source_column} " +
                              f"{rel_symbol} " +
                              f"{relationship.target_table}.{relationship.target_column}")
        
        output.append("```")
        
        return "\n".join(output) 