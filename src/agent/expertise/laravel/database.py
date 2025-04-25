"""
Laravel database management expertise module.

This module provides templates and knowledge for generating Laravel database related
code including migrations, models with relationships, and seeders.
"""

from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field
import re
import datetime


class DatabaseTemplate(BaseModel):
    """Template for Laravel database-related code."""
    name: str
    description: str
    template: str
    example: str
    tags: List[str] = Field(default_factory=list)


class LaravelDatabaseExpertise:
    """
    Laravel database management expertise.
    
    This class provides templates and utilities for generating Laravel database-related
    code including migrations, models, seeders, factories, and relationships.
    """
    
    def __init__(self):
        """Initialize the Laravel database management expertise module."""
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, DatabaseTemplate]:
        """Load the database templates."""
        templates = {}
        
        # Migration template
        templates["migration"] = DatabaseTemplate(
            name="Migration",
            description="Laravel database migration template.",
            template="""<?php

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
            $table->id();
{columns}
            $table->timestamps();
{soft_deletes}
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
""",
            example="""<?php

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
        Schema::create('products', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->text('description')->nullable();
            $table->decimal('price', 10, 2);
            $table->boolean('is_active')->default(true);
            $table->foreignId('category_id')->constrained()->onDelete('cascade');
            $table->timestamps();
            $table->softDeletes();
            
            $table->index('name');
            $table->index('price');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('products');
    }
};
""",
            tags=["migration", "database", "schema"]
        )
        
        # Model template
        templates["model"] = DatabaseTemplate(
            name="Model",
            description="Laravel Eloquent model template.",
            template="""<?php

namespace App\\Models{namespace};

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;
{soft_deletes_import}
{imports}

class {model_name} extends Model
{
    use HasFactory{soft_deletes_trait};

    {table}
    
    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
{fillable}
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
{casts}
    ];
    
{relationships}
{scopes}
}
""",
            example="""<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;
use Illuminate\\Database\\Eloquent\\SoftDeletes;
use App\\Models\\Category;
use App\\Models\\Review;
use App\\Models\\Tag;

class Product extends Model
{
    use HasFactory, SoftDeletes;
    
    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'name',
        'description',
        'price',
        'is_active',
        'category_id',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'price' => 'decimal:2',
        'is_active' => 'boolean',
    ];
    
    /**
     * Get the category that owns the product.
     */
    public function category()
    {
        return $this->belongsTo(Category::class);
    }
    
    /**
     * Get the reviews for the product.
     */
    public function reviews()
    {
        return $this->hasMany(Review::class);
    }
    
    /**
     * The tags that belong to the product.
     */
    public function tags()
    {
        return $this->belongsToMany(Tag::class);
    }
    
    /**
     * Scope a query to only include active products.
     */
    public function scopeActive($query)
    {
        return $query->where('is_active', 1);
    }
}
""",
            tags=["model", "eloquent", "database"]
        )
        
        # Seeder template
        templates["seeder"] = DatabaseTemplate(
            name="Seeder",
            description="Laravel database seeder template.",
            template="""<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Console\\Seeds\\WithoutModelEvents;
use Illuminate\\Database\\Seeder;
use App\\Models{namespace}\\{model_name};

class {model_name}Seeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        {model_name}::factory({count})->create();
        
{custom_seeds}
    }
}
""",
            example="""<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Console\\Seeds\\WithoutModelEvents;
use Illuminate\\Database\\Seeder;
use App\\Models\\Product;
use App\\Models\\Category;

class ProductSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Create 50 products with random categories
        Product::factory(50)->create();
        
        // Create featured products
        Product::factory(5)->create([
            'is_featured' => true,
            'is_active' => true,
        ]);
        
        // Create products for specific category
        $category = Category::where('name', 'Electronics')->first();
        
        if ($category) {
            Product::factory(10)->create([
                'category_id' => $category->id,
            ]);
        }
    }
}
""",
            tags=["seeder", "database", "faker"]
        )
        
        # Factory template
        templates["factory"] = DatabaseTemplate(
            name="Factory",
            description="Laravel model factory template.",
            template="""<?php

namespace Database\\Factories;

use Illuminate\\Database\\Eloquent\\Factories\\Factory;
use App\\Models{namespace}\\{model_name};
{imports}

/**
 * @extends \\Illuminate\\Database\\Eloquent\\Factories\\Factory<\\App\\Models{namespace}\\{model_name}>
 */
class {model_name}Factory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = {model_name}::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
{definition}
        ];
    }
{states}
}
""",
            example="""<?php

namespace Database\\Factories;

use Illuminate\\Database\\Eloquent\\Factories\\Factory;
use App\\Models\\Product;
use App\\Models\\Category;

/**
 * @extends \\Illuminate\\Database\\Eloquent\\Factories\\Factory<\\App\\Models\\Product>
 */
class ProductFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = Product::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->words(3, true),
            'description' => fake()->paragraph(),
            'price' => fake()->randomFloat(2, 10, 1000),
            'is_active' => fake()->boolean(80),
            'category_id' => Category::factory(),
        ];
    }
    
    /**
     * Indicate that the product is featured.
     *
     * @return $this
     */
    public function featured()
    {
        return $this->state(fn (array $attributes) => [
            'is_featured' => true,
        ]);
    }
    
    /**
     * Indicate that the product is inactive.
     *
     * @return $this
     */
    public function inactive()
    {
        return $this->state(fn (array $attributes) => [
            'is_active' => false,
        ]);
    }
}
""",
            tags=["factory", "database", "faker"]
        )
        
        # Pivot migration template
        templates["pivot_migration"] = DatabaseTemplate(
            name="Pivot Migration",
            description="Laravel pivot table migration template.",
            template="""<?php

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
        Schema::create('{table1}_{table2}', function (Blueprint $table) {
            $table->id();
            $table->foreignId('{table1_singular}_id')->constrained()->onDelete('cascade');
            $table->foreignId('{table2_singular}_id')->constrained()->onDelete('cascade');
{extra_columns}
            $table->timestamps();
            
            $table->unique(['{table1_singular}_id', '{table2_singular}_id']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('{table1}_{table2}');
    }
};
""",
            example="""<?php

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
        Schema::create('product_tag', function (Blueprint $table) {
            $table->id();
            $table->foreignId('product_id')->constrained()->onDelete('cascade');
            $table->foreignId('tag_id')->constrained()->onDelete('cascade');
            $table->timestamps();
            
            $table->unique(['product_id', 'tag_id']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('product_tag');
    }
};
""",
            tags=["migration", "database", "pivot", "many-to-many"]
        )
        
        return templates
    
    def get_template(self, template_name: str) -> Optional[DatabaseTemplate]:
        """Get a template by name."""
        return self.templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, DatabaseTemplate]:
        """Get all available templates."""
        return self.templates
    
    def generate_migration(self, table_name: str, columns: Dict[str, Dict[str, Any]], soft_deletes: bool = False, 
                          indexes: List[str] = None, foreign_keys: Dict[str, Dict[str, Any]] = None) -> str:
        """
        Generate a migration for the given table.
        
        Args:
            table_name: The name of the table (plural, snake_case)
            columns: Dictionary of column definitions with data types and modifiers
            soft_deletes: Whether to include soft deletes
            indexes: List of columns to index
            foreign_keys: Dictionary of foreign key definitions
            
        Returns:
            The generated migration code
        """
        template = self.get_template("migration")
        if not template:
            raise ValueError("Migration template not found")
        
        # Generate column definitions
        columns_code = []
        
        for name, config in columns.items():
            column_type = config.get('type', 'string')
            
            # Basic column definition
            column_def = f"            $table->{column_type}('{name}')"
            
            # Add type parameters if needed
            if column_type in ['decimal', 'float', 'double']:
                precision = config.get('precision', 8)
                scale = config.get('scale', 2)
                column_def = f"            $table->{column_type}('{name}', {precision}, {scale})"
            elif column_type == 'enum':
                values = config.get('values', [])
                values_str = "'" + "', '".join(values) + "'"
                column_def = f"            $table->{column_type}('{name}', [{values_str}])"
            elif column_type == 'string' and 'length' in config:
                length = config.get('length')
                column_def = f"            $table->{column_type}('{name}', {length})"
            
            # Add modifiers
            if config.get('nullable', False):
                column_def += "->nullable()"
            
            if 'default' in config:
                default = config['default']
                if isinstance(default, bool):
                    default = str(default).lower()
                elif isinstance(default, str):
                    default = f"'{default}'"
                column_def += f"->default({default})"
            
            if config.get('unique', False):
                column_def += "->unique()"
                
            # End the line
            column_def += ";"
            columns_code.append(column_def)
        
        # Add foreign keys
        if foreign_keys:
            for name, config in foreign_keys.items():
                references = config.get('references', 'id')
                on = config.get('on', name.replace('_id', 's'))
                on_delete = config.get('on_delete', 'cascade')
                
                fk_def = f"            $table->foreignId('{name}')"
                
                if config.get('nullable', False):
                    fk_def += "->nullable()"
                    
                fk_def += f"->constrained('{on}')"
                
                if references != 'id':
                    fk_def += f"->references('{references}')"
                    
                if on_delete:
                    fk_def += f"->onDelete('{on_delete}')"
                    
                fk_def += ";"
                columns_code.append(fk_def)
        
        # Add indexes
        if indexes:
            for index in indexes:
                if isinstance(index, list):
                    index_columns = "', '".join(index)
                    columns_code.append(f"            $table->index(['{index_columns}']);")
                else:
                    columns_code.append(f"            $table->index('{index}');")
        
        # Format soft deletes
        soft_deletes_code = "            $table->softDeletes();" if soft_deletes else ""
        
        # Combine all elements
        return template.template.replace(
            "{table_name}", table_name
        ).replace(
            "{columns}", "\n".join(columns_code)
        ).replace(
            "{soft_deletes}", soft_deletes_code
        )
    
    def generate_model(self, model_name: str, fillable: List[str], relationships: Dict[str, Dict[str, Any]] = None,
                      casts: Dict[str, str] = None, uses_soft_deletes: bool = False, 
                      namespace: str = "", table: str = None, scopes: List[Dict[str, Any]] = None) -> str:
        """
        Generate a model for the given name.
        
        Args:
            model_name: The name of the model (singular, PascalCase)
            fillable: List of fillable properties
            relationships: Dictionary of relationships to define
            casts: Dictionary of attribute cast types
            uses_soft_deletes: Whether to use soft deletes
            namespace: Optional namespace (after App\\Models)
            table: Optional custom table name
            scopes: List of scope methods to define
            
        Returns:
            The generated model code
        """
        template = self.get_template("model")
        if not template:
            raise ValueError("Model template not found")
        
        # Format imports
        imports = []
        
        if uses_soft_deletes:
            imports.append("use Illuminate\\Database\\Eloquent\\SoftDeletes;")
            
        # Add relationship imports
        if relationships:
            related_models = set()
            for _, config in relationships.items():
                related_model = config.get('model')
                if related_model and related_model != model_name:
                    related_models.add(related_model)
            
            for related_model in sorted(related_models):
                # Basic import assuming model is in App\Models
                imports.append(f"use App\\Models\\{related_model};")
        
        # Format fillable
        formatted_fillable = []
        for field in fillable:
            formatted_fillable.append(f"        '{field}',")
        
        # Format casts
        formatted_casts = []
        if casts:
            for field, cast_type in casts.items():
                formatted_casts.append(f"        '{field}' => '{cast_type}',")
        
        # Format soft deletes
        soft_deletes_import = "use Illuminate\\Database\\Eloquent\\SoftDeletes;" if uses_soft_deletes else ""
        soft_deletes_trait = ", SoftDeletes" if uses_soft_deletes else ""
        
        # Format table override
        table_code = f"protected $table = '{table}';" if table else ""
        
        # Format namespace
        formatted_namespace = f"\\{namespace}" if namespace else ""
        
        # Format relationships
        relationships_code = []
        if relationships:
            for name, config in relationships.items():
                relationship_type = config.get('type', 'belongsTo')
                related_model = config.get('model', '')
                
                # Method definition
                method_def = f"""    /**
     * {config.get('comment', f'Get the {name} relationship.')}
     */
    public function {name}()
    {{
        return $this->{relationship_type}({related_model}::class"""
                
                # Add any extra parameters
                if relationship_type == 'belongsToMany':
                    pivot_table = config.get('pivot_table')
                    if pivot_table:
                        method_def += f", '{pivot_table}'"
                    
                    foreign_pivot_key = config.get('foreign_pivot_key')
                    if foreign_pivot_key:
                        method_def += f", '{foreign_pivot_key}'"
                    
                    related_pivot_key = config.get('related_pivot_key')
                    if related_pivot_key:
                        method_def += f", '{related_pivot_key}'"
                    
                    # Add withPivot if needed
                    pivot_fields = config.get('pivot_fields')
                    if pivot_fields:
                        fields = "', '".join(pivot_fields)
                        method_def += f")->withPivot('{fields}'"
                    
                    # Add withTimestamps if needed
                    if config.get('with_timestamps', False):
                        method_def += ")->withTimestamps()"
                    else:
                        method_def += ")"
                else:
                    method_def += ")"
                
                method_def += ";\n    }"
                relationships_code.append(method_def)
        
        # Format scopes
        scopes_code = []
        if scopes:
            for scope in scopes:
                name = scope.get('name', '')
                parameters = scope.get('parameters', '$query')
                body = scope.get('body', '')
                
                scope_def = f"""    /**
     * {scope.get('comment', f'Scope a query to {name} condition.')}
     */
    public function scope{name.capitalize()}({parameters})
    {{
        return {body};
    }}"""
                scopes_code.append(scope_def)
        
        # Combine all elements
        return template.template.replace(
            "{model_name}", model_name
        ).replace(
            "{namespace}", formatted_namespace
        ).replace(
            "{soft_deletes_import}", soft_deletes_import
        ).replace(
            "{imports}", "\n".join(imports)
        ).replace(
            "{soft_deletes_trait}", soft_deletes_trait
        ).replace(
            "{table}", table_code
        ).replace(
            "{fillable}", "\n".join(formatted_fillable)
        ).replace(
            "{casts}", "\n".join(formatted_casts)
        ).replace(
            "{relationships}", "\n".join(relationships_code)
        ).replace(
            "{scopes}", "\n".join(scopes_code)
        )
    
    def generate_seeder(self, model_name: str, count: int = 10, namespace: str = "", custom_seeds: str = "") -> str:
        """
        Generate a seeder for the given model.
        
        Args:
            model_name: The name of the model (singular, PascalCase)
            count: Number of records to generate
            namespace: Optional namespace (after App\\Models)
            custom_seeds: Optional custom seeding logic
            
        Returns:
            The generated seeder code
        """
        template = self.get_template("seeder")
        if not template:
            raise ValueError("Seeder template not found")
            
        formatted_namespace = f"\\{namespace}" if namespace else ""
        
        return template.template.replace(
            "{model_name}", model_name
        ).replace(
            "{namespace}", formatted_namespace
        ).replace(
            "{count}", str(count)
        ).replace(
            "{custom_seeds}", custom_seeds
        )
    
    def generate_factory(self, model_name: str, definition: Dict[str, str], states: List[Dict[str, Any]] = None,
                       namespace: str = "", imports: List[str] = None) -> str:
        """
        Generate a factory for the given model.
        
        Args:
            model_name: The name of the model (singular, PascalCase)
            definition: Dictionary of field definitions
            states: List of factory states
            namespace: Optional namespace (after App\\Models)
            imports: Optional list of additional imports
            
        Returns:
            The generated factory code
        """
        template = self.get_template("factory")
        if not template:
            raise ValueError("Factory template not found")
        
        # Format definition
        formatted_definition = []
        for field, value in definition.items():
            formatted_definition.append(f"            '{field}' => {value},")
        
        # Format states
        formatted_states = []
        if states:
            for state in states:
                name = state.get('name', '')
                attributes = state.get('attributes', {})
                
                # Format attributes
                formatted_attributes = []
                for field, value in attributes.items():
                    formatted_attributes.append(f"                '{field}' => {value},")
                
                state_code = f"""
    /**
     * {state.get('comment', f'Indicate that the model is {name}.')}
     *
     * @return $this
     */
    public function {name}()
    {{
        return $this->state(fn (array $attributes) => [
{chr(10).join(formatted_attributes)}
        ]);
    }}"""
                formatted_states.append(state_code)
        
        # Format namespace
        formatted_namespace = f"\\{namespace}" if namespace else ""
        
        # Format imports
        formatted_imports = ""
        if imports:
            formatted_imports = "\n" + "\n".join(imports)
            
        return template.template.replace(
            "{model_name}", model_name
        ).replace(
            "{namespace}", formatted_namespace
        ).replace(
            "{imports}", formatted_imports
        ).replace(
            "{definition}", "\n".join(formatted_definition)
        ).replace(
            "{states}", "".join(formatted_states)
        )
    
    def generate_pivot_migration(self, table1: str, table2: str, extra_columns: Dict[str, Dict[str, Any]] = None) -> str:
        """
        Generate a migration for a pivot table.
        
        Args:
            table1: First table name (plural, snake_case)
            table2: Second table name (plural, snake_case)
            extra_columns: Optional dictionary of extra columns for the pivot table
            
        Returns:
            The generated pivot migration code
        """
        template = self.get_template("pivot_migration")
        if not template:
            raise ValueError("Pivot migration template not found")
        
        # Ensure tables are in alphabetical order (Laravel convention)
        if table1 > table2:
            table1, table2 = table2, table1
            
        # Get singular forms
        table1_singular = self._to_singular(table1)
        table2_singular = self._to_singular(table2)
        
        # Format extra columns
        extra_columns_code = ""
        if extra_columns:
            for name, config in extra_columns.items():
                column_type = config.get('type', 'string')
                
                column_def = f"            $table->{column_type}('{name}')"
                
                if config.get('nullable', False):
                    column_def += "->nullable()"
                
                if 'default' in config:
                    default = config['default']
                    if isinstance(default, bool):
                        default = str(default).lower()
                    elif isinstance(default, str):
                        default = f"'{default}'"
                    column_def += f"->default({default})"
                    
                column_def += ";"
                extra_columns_code += f"{column_def}\n"
        
        return template.template.replace(
            "{table1}", table1
        ).replace(
            "{table2}", table2
        ).replace(
            "{table1_singular}", table1_singular
        ).replace(
            "{table2_singular}", table2_singular
        ).replace(
            "{extra_columns}", extra_columns_code
        )
    
    def _to_singular(self, plural: str) -> str:
        """
        Convert a plural snake_case word to singular snake_case.
        This is a simplified version - a more robust solution would use a library.
        
        Args:
            plural: Plural snake_case word
            
        Returns:
            Singular snake_case word
        """
        # Handle common cases
        if plural.endswith('ies'):
            return plural[:-3] + 'y'
        elif plural.endswith('s'):
            return plural[:-1]
        return plural
        
    def generate_migration_filename(self, table_name: str, action: str = "create") -> str:
        """
        Generate a migration filename with current timestamp.
        
        Args:
            table_name: The name of the table
            action: The action (create, update, etc.)
            
        Returns:
            Migration filename
        """
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        return f"{timestamp}_{action}_{table_name}_table.php" 