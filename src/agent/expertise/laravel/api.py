"""
Laravel API development expertise module.

This module provides templates and knowledge for generating Laravel API endpoints
following RESTful conventions and Laravel best practices.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class ApiEndpointTemplate(BaseModel):
    """Template for a Laravel API endpoint."""
    name: str
    description: str
    template: str
    example: str
    tags: List[str] = Field(default_factory=list)


class LaravelApiExpertise:
    """
    Laravel API development expertise.
    
    This class provides templates and utilities for generating Laravel API endpoints,
    controllers, routes, and resources following Laravel best practices.
    """
    
    def __init__(self):
        """Initialize the Laravel API expertise module."""
        self.api_templates = self._load_api_templates()
        
    def _load_api_templates(self) -> Dict[str, ApiEndpointTemplate]:
        """Load the API endpoint templates."""
        templates = {}
        
        # API Resource Controller template
        templates["api_resource_controller"] = ApiEndpointTemplate(
            name="API Resource Controller",
            description="A Laravel controller for RESTful API resource operations.",
            template="""
<?php

namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Models\\{model};
use App\\Http\\Resources\\{model}Resource;
use App\\Http\\Resources\\{model}Collection;
use App\\Http\\Requests\\Store{model}Request;
use App\\Http\\Requests\\Update{model}Request;
use Illuminate\\Http\\Request;
use Illuminate\\Http\\Response;

class {model}Controller extends Controller
{
    /**
     * Display a listing of the resources.
     *
     * @return \\App\\Http\\Resources\\{model}Collection
     */
    public function index()
    {
        return new {model}Collection({model}::paginate());
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \\App\\Http\\Requests\\Store{model}Request  $request
     * @return \\App\\Http\\Resources\\{model}Resource
     */
    public function store(Store{model}Request $request)
    {
        $validated = $request->validated();
        
        ${modelVariable} = {model}::create($validated);
        
        return new {model}Resource(${modelVariable});
    }

    /**
     * Display the specified resource.
     *
     * @param  \\App\\Models\\{model}  ${modelVariable}
     * @return \\App\\Http\\Resources\\{model}Resource
     */
    public function show({model} ${modelVariable})
    {
        return new {model}Resource(${modelVariable});
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \\App\\Http\\Requests\\Update{model}Request  $request
     * @param  \\App\\Models\\{model}  ${modelVariable}
     * @return \\App\\Http\\Resources\\{model}Resource
     */
    public function update(Update{model}Request $request, {model} ${modelVariable})
    {
        $validated = $request->validated();
        
        ${modelVariable}->update($validated);
        
        return new {model}Resource(${modelVariable});
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \\App\\Models\\{model}  ${modelVariable}
     * @return \\Illuminate\\Http\\Response
     */
    public function destroy({model} ${modelVariable})
    {
        ${modelVariable}->delete();
        
        return response()->noContent();
    }
}
""",
            example="""
<?php

namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Models\\Product;
use App\\Http\\Resources\\ProductResource;
use App\\Http\\Resources\\ProductCollection;
use App\\Http\\Requests\\StoreProductRequest;
use App\\Http\\Requests\\UpdateProductRequest;
use Illuminate\\Http\\Request;
use Illuminate\\Http\\Response;

class ProductController extends Controller
{
    /**
     * Display a listing of the products.
     *
     * @return \\App\\Http\\Resources\\ProductCollection
     */
    public function index()
    {
        return new ProductCollection(Product::paginate());
    }

    /**
     * Store a newly created product in storage.
     *
     * @param  \\App\\Http\\Requests\\StoreProductRequest  $request
     * @return \\App\\Http\\Resources\\ProductResource
     */
    public function store(StoreProductRequest $request)
    {
        $validated = $request->validated();
        
        $product = Product::create($validated);
        
        return new ProductResource($product);
    }

    /**
     * Display the specified product.
     *
     * @param  \\App\\Models\\Product  $product
     * @return \\App\\Http\\Resources\\ProductResource
     */
    public function show(Product $product)
    {
        return new ProductResource($product);
    }

    /**
     * Update the specified product in storage.
     *
     * @param  \\App\\Http\\Requests\\UpdateProductRequest  $request
     * @param  \\App\\Models\\Product  $product
     * @return \\App\\Http\\Resources\\ProductResource
     */
    public function update(UpdateProductRequest $request, Product $product)
    {
        $validated = $request->validated();
        
        $product->update($validated);
        
        return new ProductResource($product);
    }

    /**
     * Remove the specified product from storage.
     *
     * @param  \\App\\Models\\Product  $product
     * @return \\Illuminate\\Http\\Response
     */
    public function destroy(Product $product)
    {
        $product->delete();
        
        return response()->noContent();
    }
}
""",
            tags=["api", "controller", "resource", "restful"]
        )
        
        # API Resource template
        templates["api_resource"] = ApiEndpointTemplate(
            name="API Resource",
            description="A Laravel API resource for transforming models to JSON responses.",
            template="""
<?php

namespace App\\Http\\Resources;

use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\JsonResource;

class {model}Resource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return array
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
{fields}
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
""",
            example="""
<?php

namespace App\\Http\\Resources;

use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\JsonResource;

class ProductResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return array
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'description' => $this->description,
            'price' => $this->price,
            'category_id' => $this->category_id,
            'category' => new CategoryResource($this->whenLoaded('category')),
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
""",
            tags=["api", "resource", "json"]
        )
        
        # API Resource Collection template
        templates["api_resource_collection"] = ApiEndpointTemplate(
            name="API Resource Collection",
            description="A Laravel API resource collection for transforming collections to JSON responses.",
            template="""
<?php

namespace App\\Http\\Resources;

use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\ResourceCollection;

class {model}Collection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return array
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
            'meta' => [
                'total' => $this->collection->count(),
            ],
        ];
    }
}
""",
            example="""
<?php

namespace App\\Http\\Resources;

use Illuminate\\Http\\Request;
use Illuminate\\Http\\Resources\\Json\\ResourceCollection;

class ProductCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return array
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => route('api.products.index'),
            ],
            'meta' => [
                'total' => $this->collection->count(),
                'per_page' => 15,
                'current_page' => 1,
            ],
        ];
    }
}
""",
            tags=["api", "resource", "collection", "json"]
        )
        
        # API Routes template
        templates["api_routes"] = ApiEndpointTemplate(
            name="API Routes",
            description="Laravel API routes definition for RESTful resources.",
            template="""
<?php

use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Route;
use App\\Http\\Controllers\\Api\\{model}Controller;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application.
|
*/

Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('{routeName}', {model}Controller::class);
});
""",
            example="""
<?php

use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Route;
use App\\Http\\Controllers\\Api\\ProductController;
use App\\Http\\Controllers\\Api\\CategoryController;
use App\\Http\\Controllers\\Api\\AuthController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application.
|
*/

// Public routes
Route::post('/login', [AuthController::class, 'login']);
Route::post('/register', [AuthController::class, 'register']);

// Protected routes
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('products', ProductController::class);
    Route::apiResource('categories', CategoryController::class);
    Route::post('/logout', [AuthController::class, 'logout']);
});
""",
            tags=["api", "routes", "restful"]
        )
        
        # Form Request template
        templates["form_request"] = ApiEndpointTemplate(
            name="Form Request",
            description="Laravel form request for validation with API controller.",
            template="""
<?php

namespace App\\Http\\Requests;

use Illuminate\\Foundation\\Http\\FormRequest;
use Illuminate\\Validation\\Rule;

class Store{model}Request extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \\Illuminate\\Contracts\\Validation\\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
{rules}
        ];
    }
}
""",
            example="""
<?php

namespace App\\Http\\Requests;

use Illuminate\\Foundation\\Http\\FormRequest;
use Illuminate\\Validation\\Rule;

class StoreProductRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \\Illuminate\\Contracts\\Validation\\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'price' => ['required', 'numeric', 'min:0'],
            'category_id' => ['required', 'exists:categories,id'],
            'is_active' => ['boolean'],
            'tags' => ['sometimes', 'array'],
            'tags.*' => ['exists:tags,id'],
        ];
    }
}
""",
            tags=["api", "validation", "request"]
        )
        
        # API Authentication with Sanctum template
        templates["api_auth_sanctum"] = ApiEndpointTemplate(
            name="API Authentication with Sanctum",
            description="Laravel Sanctum authentication controller for API.",
            template="""
<?php

namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Models\\User;
use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Hash;
use Illuminate\\Validation\\ValidationException;

class AuthController extends Controller
{
    /**
     * Register a new user and return a token.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return \\Illuminate\\Http\\Response
     */
    public function register(Request $request)
    {
        $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'email', 'max:255', 'unique:users'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ]);

        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);

        $token = $user->createToken('api-token')->plainTextToken;

        return response()->json([
            'message' => 'Registration successful',
            'user' => $user,
            'token' => $token
        ], 201);
    }

    /**
     * Authenticate a user and return a token.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return \\Illuminate\\Http\\Response
     */
    public function login(Request $request)
    {
        $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
            'device_name' => ['sometimes', 'string'],
        ]);

        $user = User::where('email', $request->email)->first();

        if (! $user || ! Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }

        $device = $request->device_name ?? $request->userAgent() ?? 'API Token';
        $token = $user->createToken($device)->plainTextToken;

        return response()->json([
            'message' => 'Login successful',
            'user' => $user,
            'token' => $token
        ]);
    }

    /**
     * Logout the user (revoke token).
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return \\Illuminate\\Http\\Response
     */
    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'message' => 'Logged out successfully'
        ]);
    }
}
""",
            example="""
<?php

namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Models\\User;
use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Hash;
use Illuminate\\Validation\\ValidationException;

class AuthController extends Controller
{
    /**
     * Register a new user and return a token.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return \\Illuminate\\Http\\Response
     */
    public function register(Request $request)
    {
        $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'email', 'max:255', 'unique:users'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ]);

        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);

        $token = $user->createToken('api-token')->plainTextToken;

        return response()->json([
            'message' => 'Registration successful',
            'user' => $user,
            'token' => $token
        ], 201);
    }

    /**
     * Authenticate a user and return a token.
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return \\Illuminate\\Http\\Response
     */
    public function login(Request $request)
    {
        $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
            'device_name' => ['sometimes', 'string'],
        ]);

        $user = User::where('email', $request->email)->first();

        if (! $user || ! Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }

        $device = $request->device_name ?? $request->userAgent() ?? 'API Token';
        $token = $user->createToken($device)->plainTextToken;

        return response()->json([
            'message' => 'Login successful',
            'user' => $user,
            'token' => $token
        ]);
    }

    /**
     * Logout the user (revoke token).
     *
     * @param  \\Illuminate\\Http\\Request  $request
     * @return \\Illuminate\\Http\\Response
     */
    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'message' => 'Logged out successfully'
        ]);
    }
}
""",
            tags=["api", "auth", "sanctum", "authentication"]
        )
        
        return templates
    
    def get_template(self, template_name: str) -> Optional[ApiEndpointTemplate]:
        """Get a template by name."""
        return self.api_templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, ApiEndpointTemplate]:
        """Get all available templates."""
        return self.api_templates
    
    def generate_api_controller(self, model_name: str) -> str:
        """
        Generate an API controller for the given model.
        
        Args:
            model_name: The name of the model (e.g., 'Product')
            
        Returns:
            The generated controller code
        """
        template = self.get_template("api_resource_controller")
        if not template:
            raise ValueError("API resource controller template not found")
        
        # Convert model name for variable (e.g., Product -> product)
        model_variable = model_name[0].lower() + model_name[1:]
        
        return template.template.replace("{model}", model_name).replace("{modelVariable}", model_variable)
    
    def generate_api_resource(self, model_name: str, fields: List[str]) -> str:
        """
        Generate an API resource for the given model.
        
        Args:
            model_name: The name of the model (e.g., 'Product')
            fields: The fields to include in the resource
            
        Returns:
            The generated resource code
        """
        template = self.get_template("api_resource")
        if not template:
            raise ValueError("API resource template not found")
        
        # Format fields
        formatted_fields = ""
        for field in fields:
            formatted_fields += f"            '{field}' => $this->{field},\n"
        
        return template.template.replace("{model}", model_name).replace("{fields}", formatted_fields)
    
    def generate_api_resource_collection(self, model_name: str) -> str:
        """
        Generate an API resource collection for the given model.
        
        Args:
            model_name: The name of the model (e.g., 'Product')
            
        Returns:
            The generated resource collection code
        """
        template = self.get_template("api_resource_collection")
        if not template:
            raise ValueError("API resource collection template not found")
        
        return template.template.replace("{model}", model_name)
    
    def generate_form_request(self, model_name: str, validation_rules: Dict[str, List[str]]) -> str:
        """
        Generate a form request for the given model.
        
        Args:
            model_name: The name of the model (e.g., 'Product')
            validation_rules: Dict mapping field names to validation rules
            
        Returns:
            The generated form request code
        """
        template = self.get_template("form_request")
        if not template:
            raise ValueError("Form request template not found")
        
        # Format validation rules
        formatted_rules = ""
        for field, rules in validation_rules.items():
            rules_str = "', '".join(rules)
            formatted_rules += f"            '{field}' => ['{rules_str}'],\n"
        
        return template.template.replace("{model}", model_name).replace("{rules}", formatted_rules)
    
    def generate_api_routes(self, model_name: str, route_name: Optional[str] = None) -> str:
        """
        Generate API routes for the given model.
        
        Args:
            model_name: The name of the model (e.g., 'Product')
            route_name: The route name (defaults to plural lowercase of model_name)
            
        Returns:
            The generated routes code
        """
        template = self.get_template("api_routes")
        if not template:
            raise ValueError("API routes template not found")
        
        if not route_name:
            # Convert from singular CamelCase to plural snake_case
            # This is a simplified version - a more robust solution would use a library
            route_name = model_name.lower() + 's'
        
        return template.template.replace("{model}", model_name).replace("{routeName}", route_name) 