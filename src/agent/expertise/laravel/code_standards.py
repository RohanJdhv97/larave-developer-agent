"""
Laravel code standards expertise module.

This module provides templates and guidelines for generating properly commented
code adhering to Laravel best practices and coding standards.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class CodeStandardTemplate(BaseModel):
    """Template for Laravel code standards."""
    name: str
    description: str
    template: str
    example: str
    tags: List[str] = Field(default_factory=list)


class LaravelCodeStandardsExpertise:
    """
    Laravel code standards expertise.
    
    This class provides templates and utilities for generating properly formatted
    and commented Laravel code following best practices and coding standards.
    """
    
    def __init__(self):
        """Initialize the Laravel code standards expertise module."""
        self.templates = self._load_templates()
        self.psr_standards = self._load_psr_standards()
        self.laravel_conventions = self._load_laravel_conventions()
        
    def _load_templates(self) -> Dict[str, CodeStandardTemplate]:
        """Load the code standards templates."""
        templates = {}
        
        # Class template
        templates["class"] = CodeStandardTemplate(
            name="PHP Class",
            description="Template for a PHP class following PSR-12 standards.",
            template="""<?php

{namespace}

{imports}

/**
 * {class_description}
 {class_annotations}
 */
class {class_name}{extends}{implements}
{
{traits}
{constants}
{properties}
{methods}
}
""",
            example="""<?php

namespace App\\Services;

use App\\Contracts\\PaymentGatewayInterface;
use App\\Models\\Payment;
use App\\Models\\User;
use Illuminate\\Support\\Facades\\Log;

/**
 * Payment service for processing transactions through various gateways
 * 
 * @package App\\Services
 */
class PaymentService
{
    use LogsActivity;
    
    /**
     * The payment gateway implementation.
     *
     * @var \\App\\Contracts\\PaymentGatewayInterface
     */
    protected $gateway;
    
    /**
     * Default currency for payments.
     *
     * @var string
     */
    protected $currency = 'USD';
    
    /**
     * Create a new payment service instance.
     *
     * @param  \\App\\Contracts\\PaymentGatewayInterface  $gateway
     * @return void
     */
    public function __construct(PaymentGatewayInterface $gateway)
    {
        $this->gateway = $gateway;
    }
    
    /**
     * Process a payment for a user.
     *
     * @param  \\App\\Models\\User  $user
     * @param  float  $amount
     * @param  string  $description
     * @return \\App\\Models\\Payment
     * 
     * @throws \\App\\Exceptions\\PaymentFailedException
     */
    public function processPayment(User $user, float $amount, string $description): Payment
    {
        try {
            $response = $this->gateway->charge([
                'amount' => $amount,
                'currency' => $this->currency,
                'description' => $description,
                'user_id' => $user->id,
            ]);
            
            return Payment::create([
                'user_id' => $user->id,
                'amount' => $amount,
                'currency' => $this->currency,
                'description' => $description,
                'transaction_id' => $response['transaction_id'],
                'status' => 'completed',
            ]);
        } catch (\\Exception $e) {
            Log::error('Payment failed: ' . $e->getMessage(), [
                'user_id' => $user->id,
                'amount' => $amount,
            ]);
            
            throw new \\App\\Exceptions\\PaymentFailedException($e->getMessage());
        }
    }
}
""",
            tags=["class", "psr-12", "code-standards"]
        )
        
        # Method template
        templates["method"] = CodeStandardTemplate(
            name="PHP Method",
            description="Template for a PHP method with proper doc block.",
            template="""    /**
     * {method_description}
     *
{parameters}     *
     * @return {return_type}
{throws}     */
    {visibility}function {method_name}({method_parameters}): {return_hint}
    {
{method_body}
    }
""",
            example="""    /**
     * Process a payment for a user.
     *
     * @param  \\App\\Models\\User  $user
     * @param  float  $amount
     * @param  string  $description
     *
     * @return \\App\\Models\\Payment
     * 
     * @throws \\App\\Exceptions\\PaymentFailedException
     */
    public function processPayment(User $user, float $amount, string $description): Payment
    {
        try {
            $response = $this->gateway->charge([
                'amount' => $amount,
                'currency' => $this->currency,
                'description' => $description,
                'user_id' => $user->id,
            ]);
            
            return Payment::create([
                'user_id' => $user->id,
                'amount' => $amount,
                'currency' => $this->currency,
                'description' => $description,
                'transaction_id' => $response['transaction_id'],
                'status' => 'completed',
            ]);
        } catch (\\Exception $e) {
            Log::error('Payment failed: ' . $e->getMessage(), [
                'user_id' => $user->id,
                'amount' => $amount,
            ]);
            
            throw new \\App\\Exceptions\\PaymentFailedException($e->getMessage());
        }
    }
""",
            tags=["method", "docblock", "code-standards"]
        )
        
        # Property template
        templates["property"] = CodeStandardTemplate(
            name="PHP Property",
            description="Template for a PHP class property with proper doc block.",
            template="""    /**
     * {property_description}
     *
     * @var {property_type}
     */
    {visibility}{static}${property_name}{default_value};
""",
            example="""    /**
     * The payment gateway implementation.
     *
     * @var \\App\\Contracts\\PaymentGatewayInterface
     */
    protected $gateway;
    
    /**
     * Default currency for payments.
     *
     * @var string
     */
    protected $currency = 'USD';
""",
            tags=["property", "docblock", "code-standards"]
        )

        # Route group template
        templates["route_group"] = CodeStandardTemplate(
            name="Laravel Route Group",
            description="Template for Laravel route groups with proper formatting.",
            template="""Route::middleware([{middleware}])->group(function () {
    {routes}
});

Route::prefix('{prefix}')->name('{name}.')->group(function () {
    {routes}
});

Route::middleware([{middleware}])->prefix('{prefix}')->name('{name}.')->group(function () {
    {routes}
});
""",
            example="""Route::middleware(['auth:sanctum'])->group(function () {
    Route::get('/user', [UserController::class, 'show']);
    Route::put('/user', [UserController::class, 'update']);
    Route::delete('/user', [UserController::class, 'destroy']);
});

Route::prefix('admin')->name('admin.')->group(function () {
    Route::get('/dashboard', [AdminController::class, 'dashboard'])->name('dashboard');
    Route::resource('users', AdminUserController::class);
});

Route::middleware(['auth:sanctum', 'admin'])->prefix('admin')->name('admin.')->group(function () {
    Route::get('/dashboard', [AdminController::class, 'dashboard'])->name('dashboard');
    Route::resource('users', AdminUserController::class);
    Route::post('/settings', [AdminSettingsController::class, 'update'])->name('settings.update');
});
""",
            tags=["routes", "laravel", "code-standards"]
        )
        
        return templates
    
    def _load_psr_standards(self) -> Dict[str, str]:
        """Load PSR-12 coding standards guidelines."""
        return {
            "file_structure": """
PHP files MUST:
- Use only <?php or <?= opening tags
- Use the UTF-8 encoding without BOM
- Either declare symbols (classes, functions, constants) OR cause side-effects (outputting, including files) but NOT both
- Use 4 spaces for indentation (not tabs)
- End lines with a unix-style line ending (LF)
- Have a blank line after the namespace declaration
- Have one blank line after the block of use declarations
            """,
            
            "namespace_import": """
Namespace and import declarations:
- The namespace declaration must be on the same line: `namespace Vendor\\Package;`
- Import statements must be unqualified (no leading backslash)
- One import per declaration: `use Vendor\\Package\\ClassName;`
- Import statements must be grouped: PHP classes/interfaces/traits, function imports, constant imports
- Within each group, the declarations should be sorted alphabetically
            """,
            
            "classes": """
Class structure:
- The opening brace MUST go on its own line
- The closing brace MUST go on the next line after the body
- Lists of implements/extends MUST be on a single line if they fit, or split with one interface per line
- Properties and methods MUST have visibility declared (public, protected, private)
- Method arguments with default values MUST go at the end of the argument list
- The abstract, final, and static declarations MUST precede the visibility declaration
- Method and function names MUST NOT be prefixed with a single underscore to indicate protected or private visibility
            """,
            
            "control_structures": """
Control structures:
- There MUST be one space after the control structure keyword
- Opening braces MUST be on the same line as the control structure
- Closing braces MUST be on the next line after the body
- Opening parentheses MUST NOT have a space after them
- Closing parentheses MUST NOT have a space before them
- The body MUST be indented once
- The body MUST NOT be on the same line as the condition
            """,
            
            "operators": """
Operators:
- Binary operators (+, -, *, /, %, <, >, etc.) MUST have one space before and after
- Unary operators (!, ++, --, etc.) MUST NOT have a space between the operator and the operand
- The null coalescing operator (??) has a space on either side
- Type cast operators MUST NOT have a space between the cast and variable: (int)$foo
            """,
            
            "line_length": """
Line length:
- Lines SHOULD be 80 characters or less
- Lines MUST NOT be longer than 120 characters
- Lines SHOULD NOT be terminated with trailing whitespace
            """,
            
            "typing": """
Type declarations:
- Nullable type declarations MUST have no space: ?int, ?string
- Return type declarations MUST have one space between the colon and the type: function foo(): int
- When deciding to use a return type declaration, all methods in a class SHOULD have a declared return type or none
            """,
        }
    
    def _load_laravel_conventions(self) -> Dict[str, str]:
        """Load Laravel coding conventions and best practices."""
        return {
            "naming": """
Laravel naming conventions:
- Controllers: Singular, PascalCase with Controller suffix (UserController)
- Models: Singular, PascalCase (User)
- Table names: Plural, snake_case (users)
- Migrations: Snake case, descriptive (create_users_table, add_votes_to_posts_table)
- Routes: Kebab-case (user-profile)
- Route names: Dot notation, snake_case (admin.users.show)
- Config files: Snake case (app_settings.php)
- Views: Dot notation for directories, snake_case (admin.users.show)
- Validation rules: Snake case (before_or_equal)
- Form requests: PascalCase, descriptive purpose (StoreUserRequest)
- Traits: PascalCase, adjective or purpose (Notifiable, HandleApiResponses)
- Interfaces: PascalCase with Interface suffix (RepositoryInterface)
- Events: PascalCase, past tense verb (UserRegistered)
- Listeners: PascalCase, action (SendWelcomeEmail)
- Jobs: PascalCase, imperative (ProcessPodcast)
            """,
            
            "controllers": """
Controllers best practices:
- Keep controllers thin, move business logic to services or action classes
- Use type-hinted dependency injection in constructor or methods
- Use resource controllers for CRUD operations with standard methods
- Use form requests for complex validation
- Return appropriate HTTP status codes (200, 201, 422, etc.)
- Use route model binding when possible
- Limit to 5-7 actions per controller, create specialized controllers for additional needs
- Use middleware for filtering request access
            """,
            
            "models": """
Eloquent models best practices:
- Define mass-assignable properties with $fillable or $guarded
- Define property type-hints and casts properly
- Document properties with phpDoc blocks
- Define relationships with descriptive method names (posts, author, etc.)
- Use model events and observers for side effects
- Keep query logic in model scopes
- Use accessors and mutators for property transformations
- Avoid N+1 queries by using eager loading
- Use proper date casting for timestamps
            """,
            
            "blades": """
Blade templates best practices:
- Use layout inheritance with @extends/@section
- Keep logic out of templates, use view composers
- Break down complex templates into smaller partials with @include/@component
- Use short echo syntax ({{ $var }}) for escaped output
- Use {!! $html !!} only when you absolutely need unescaped HTML
- Use @foreach, @if directives for control structures
- Use @auth, @guest for authentication checks
- Use @csrf for CSRF protection in forms
- Use components and slots for reusable UI
            """,
            
            "services": """
Services best practices:
- Create services for encapsulating complex business logic
- Use dependency injection in service constructors
- Register service bindings in service providers
- Follow single responsibility principle
- Return clear response values or throw appropriate exceptions
- Document public methods with phpDoc blocks
- Use interfaces for services that have multiple implementations
- Keep methods small and focused
            """,
            
            "dependency_injection": """
Dependency injection best practices:
- Type hint interfaces rather than concrete implementations
- Register bindings in service providers
- Use contextual binding for specific implementations
- Use constructor injection for required dependencies
- Use method injection for optional dependencies
- Consider using Laravel's automatic resolution when appropriate
- Use singletons for services that maintain state
            """,
            
            "error_handling": """
Error handling best practices:
- Use custom exceptions for domain-specific errors
- Register exception handlers in App\\Exceptions\\Handler
- Return appropriate error responses for different contexts (web vs API)
- Log errors at appropriate levels (debug, info, warning, error)
- Use try/catch blocks for expected exceptions
- Use Laravel's validation for input validation
- Consider using form requests for complex validation
            """,
        }
    
    def get_template(self, template_name: str) -> Optional[CodeStandardTemplate]:
        """Get a template by name."""
        return self.templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, CodeStandardTemplate]:
        """Get all available templates."""
        return self.templates
    
    def get_psr_standard(self, standard_name: str) -> Optional[str]:
        """Get a PSR-12 standard by name."""
        return self.psr_standards.get(standard_name)
    
    def get_all_psr_standards(self) -> Dict[str, str]:
        """Get all PSR-12 standards."""
        return self.psr_standards
    
    def get_laravel_convention(self, convention_name: str) -> Optional[str]:
        """Get a Laravel convention by name."""
        return self.laravel_conventions.get(convention_name)
    
    def get_all_laravel_conventions(self) -> Dict[str, str]:
        """Get all Laravel conventions."""
        return self.laravel_conventions
    
    def generate_class(self, class_name: str, namespace: str, class_description: str, properties: List[Dict[str, Any]] = None,
                      methods: List[Dict[str, Any]] = None, traits: List[str] = None, constants: List[Dict[str, Any]] = None,
                      extends: str = None, implements: List[str] = None, class_annotations: List[str] = None) -> str:
        """
        Generate a PHP class following PSR-12 and Laravel standards.
        
        Args:
            class_name: The name of the class
            namespace: Fully qualified namespace
            class_description: Description for the class doc block
            properties: List of property definitions
            methods: List of method definitions
            traits: List of traits to use
            constants: List of constant definitions
            extends: Parent class to extend
            implements: List of interfaces to implement
            class_annotations: Additional annotations for class doc block
            
        Returns:
            The generated class code
        """
        template = self.get_template("class")
        if not template:
            raise ValueError("Class template not found")
        
        # Format namespace
        formatted_namespace = f"namespace {namespace};" if namespace else ""
        
        # Collect imports from properties, methods, extends, and implements
        imports = set()
        
        # Add extends import if needed
        if extends:
            # Simple check - in real implementation would need more sophistication
            if '\\' in extends and not extends.startswith('\\'):
                imports.add(f"use {extends};")
                extends = extends.split('\\')[-1]
                
        # Add implements imports
        if implements:
            for interface in implements:
                if '\\' in interface and not interface.startswith('\\'):
                    imports.add(f"use {interface};")
                    # Update the interface name in the list to just the class name
                    implements_index = implements.index(interface)
                    implements[implements_index] = interface.split('\\')[-1]
        
        # Format extends
        formatted_extends = f" extends {extends}" if extends else ""
        
        # Format implements
        formatted_implements = ""
        if implements and len(implements) > 0:
            formatted_implements = f" implements {', '.join(implements)}"
        
        # Format traits
        formatted_traits = ""
        if traits and len(traits) > 0:
            for trait in traits:
                trait_name = trait.split('\\')[-1] if '\\' in trait else trait
                formatted_traits += f"    use {trait_name};\n"
                
                # Add to imports if needed
                if '\\' in trait and not trait.startswith('\\'):
                    imports.add(f"use {trait};")
        
        # Format constants
        formatted_constants = ""
        if constants and len(constants) > 0:
            for constant in constants:
                name = constant.get('name', '')
                value = constant.get('value', '')
                visibility = constant.get('visibility', 'public')
                description = constant.get('description', f"The {name} constant.")
                
                formatted_constants += f"""    /**
     * {description}
     */
    {visibility} const {name} = {value};
"""
            
            if formatted_constants:
                formatted_constants += "\n"
        
        # Format properties using property template
        formatted_properties = ""
        if properties and len(properties) > 0:
            property_template = self.get_template("property")
            
            for prop in properties:
                name = prop.get('name', '')
                description = prop.get('description', f"The {name} property.")
                visibility = prop.get('visibility', 'protected')
                prop_type = prop.get('type', 'mixed')
                static = "static " if prop.get('static', False) else ""
                
                # Handle default value
                default_value = prop.get('default')
                formatted_default = ""
                if default_value is not None:
                    if isinstance(default_value, str):
                        formatted_default = f" = '{default_value}'"
                    elif isinstance(default_value, bool):
                        formatted_default = f" = " + ("true" if default_value else "false")
                    else:
                        formatted_default = f" = {default_value}"
                
                # Add to imports if type contains a namespace
                if '\\' in prop_type and not prop_type.startswith('\\'):
                    # Extract the class from the type (handling arrays, collections, etc.)
                    class_match = prop_type.replace('[]', '').strip()
                    imports.add(f"use {class_match};")
                
                formatted_properties += property_template.template.replace(
                    "{property_description}", description
                ).replace(
                    "{property_type}", prop_type
                ).replace(
                    "{visibility}", visibility + " "
                ).replace(
                    "{static}", static
                ).replace(
                    "{property_name}", name
                ).replace(
                    "{default_value}", formatted_default
                )
        
        # Format methods using method template
        formatted_methods = ""
        if methods and len(methods) > 0:
            method_template = self.get_template("method")
            
            for method in methods:
                name = method.get('name', '')
                description = method.get('description', f"The {name} method.")
                visibility = method.get('visibility', 'public')
                return_type = method.get('return_type', 'void')
                return_hint = return_type
                
                # Handle parameters
                params = method.get('parameters', [])
                formatted_param_docs = ""
                formatted_param_list = []
                
                for param in params:
                    param_name = param.get('name', '')
                    param_type = param.get('type', 'mixed')
                    param_description = param.get('description', '')
                    param_default = param.get('default')
                    
                    # Format parameter doc
                    formatted_param_docs += f"     * @param  {param_type}  ${param_name} {param_description}\n"
                    
                    # Format parameter list
                    param_str = f"{param_type} ${param_name}"
                    if param_default is not None:
                        if isinstance(param_default, str):
                            param_str += f" = '{param_default}'"
                        elif isinstance(param_default, bool):
                            param_str += f" = " + ("true" if param_default else "false")
                        else:
                            param_str += f" = {param_default}"
                    
                    formatted_param_list.append(param_str)
                    
                    # Add to imports if type contains a namespace
                    if '\\' in param_type and not param_type.startswith('\\'):
                        class_match = param_type.replace('[]', '').strip()
                        imports.add(f"use {class_match};")
                
                # Format method body
                method_body = method.get('body', '        // Method implementation')
                
                # Format throws
                throws = method.get('throws', [])
                formatted_throws = ""
                for exception in throws:
                    formatted_throws += f"     * @throws {exception}\n"
                
                # Add return type to imports if needed
                if '\\' in return_type and not return_type.startswith('\\'):
                    class_match = return_type.replace('[]', '').strip()
                    imports.add(f"use {class_match};")
                    
                    # Update return hint to just the class name
                    return_hint = return_type.split('\\')[-1]
                
                formatted_methods += method_template.template.replace(
                    "{method_description}", description
                ).replace(
                    "{parameters}", formatted_param_docs
                ).replace(
                    "{return_type}", return_type
                ).replace(
                    "{throws}", formatted_throws
                ).replace(
                    "{visibility}", visibility + " "
                ).replace(
                    "{method_name}", name
                ).replace(
                    "{method_parameters}", ", ".join(formatted_param_list)
                ).replace(
                    "{return_hint}", return_hint
                ).replace(
                    "{method_body}", method_body
                )
        
        # Format class annotations
        formatted_annotations = ""
        if class_annotations and len(class_annotations) > 0:
            for annotation in class_annotations:
                formatted_annotations += f" * {annotation}\n"
        
        # Format imports
        sorted_imports = sorted(list(imports))
        formatted_imports = "\n".join(sorted_imports)
        if formatted_imports:
            formatted_imports += "\n"
        
        # Combine all elements
        return template.template.replace(
            "{namespace}", formatted_namespace
        ).replace(
            "{imports}", formatted_imports
        ).replace(
            "{class_description}", class_description
        ).replace(
            "{class_annotations}", formatted_annotations
        ).replace(
            "{class_name}", class_name
        ).replace(
            "{extends}", formatted_extends
        ).replace(
            "{implements}", formatted_implements
        ).replace(
            "{traits}", formatted_traits
        ).replace(
            "{constants}", formatted_constants
        ).replace(
            "{properties}", formatted_properties
        ).replace(
            "{methods}", formatted_methods
        )
    
    def format_route_group(self, middleware: List[str] = None, prefix: str = None, 
                           name: str = None, routes: List[str] = None) -> str:
        """
        Generate a formatted Laravel route group.
        
        Args:
            middleware: List of middleware to apply
            prefix: Route prefix
            name: Route name prefix
            routes: List of routes in the group
            
        Returns:
            The formatted route group
        """
        template = self.get_template("route_group")
        if not template:
            raise ValueError("Route group template not found")
        
        # Format middleware
        formatted_middleware = "'web'" if not middleware else "'" + "', '".join(middleware) + "'"
        
        # Format routes
        formatted_routes = "    // Routes go here" if not routes else "    " + "\n    ".join(routes)
        
        # Format prefix
        formatted_prefix = "api" if not prefix else prefix
        
        # Format name
        formatted_name = "api" if not name else name
        
        # Select the right template based on input
        if middleware and prefix and name:
            route_group = template.template.split("\n\n")[2]
        elif prefix and name:
            route_group = template.template.split("\n\n")[1]
        else:
            route_group = template.template.split("\n\n")[0]
            
        # Replace placeholders
        return route_group.replace(
            "{middleware}", formatted_middleware
        ).replace(
            "{prefix}", formatted_prefix
        ).replace(
            "{name}", formatted_name
        ).replace(
            "{routes}", formatted_routes
        )
    
    def generate_php_docblock(self, description: str, tags: Dict[str, List[str]] = None) -> str:
        """
        Generate a PHP docblock.
        
        Args:
            description: The main description
            tags: Dictionary of tags (e.g., @param, @return)
            
        Returns:
            The formatted docblock
        """
        # Format description
        lines = description.strip().split('\n')
        formatted_description = '\n * '.join([""] + lines)
        
        # Format tags
        formatted_tags = ""
        if tags and len(tags) > 0:
            formatted_tags = " *\n"  # Add a blank line between description and tags
            
            for tag_name, tag_values in tags.items():
                for value in tag_values:
                    formatted_tags += f" * @{tag_name} {value}\n"
        
        # Combine all elements
        return f"""/**{formatted_description}
{formatted_tags} */""" 