"""
FilamentPHP Testing expertise module.

This module provides templates and utilities for testing FilamentPHP components
following best practices and coding standards.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class TestTemplate(BaseModel):
    """Template for FilamentPHP tests."""
    name: str
    description: str
    template: str
    example: str
    tags: List[str] = Field(default_factory=list)


class FilamentTestingExpertise:
    """
    FilamentPHP Testing expertise.
    
    This class provides templates and utilities for testing FilamentPHP components
    following best practices and coding standards.
    """
    
    def __init__(self):
        """Initialize the FilamentPHP Testing expertise module."""
        self.templates = self._load_templates()
        self.test_patterns = self._load_test_patterns()
        
    def _load_templates(self) -> Dict[str, TestTemplate]:
        """Load the test templates."""
        templates = {}
        
        # Resource test template
        templates["resource_test"] = TestTemplate(
            name="Filament Resource Test",
            description="Template for testing a FilamentPHP resource.",
            template="""<?php

use {resource_namespace}\\{resource_name}Resource;
use {resource_namespace}\\{resource_name}Resource\\Pages\\{page_class};
use {model_namespace}\\{model_name};
{use_statements}

/**
 * {test_description}
 */
test('{test_name}', function () {
    // Arrange
{arrange}
    
    // Act
{act}
    
    // Assert
{assertions}
});
""",
            example="""<?php

use App\\Filament\\Resources\\UserResource;
use App\\Filament\\Resources\\UserResource\\Pages\\ListUsers;
use App\\Models\\User;
use function Pest\\Livewire\\livewire;

/**
 * Test user resource list page
 */
test('can view user list page', function () {
    // Arrange
    $users = User::factory()->count(10)->create();
    
    // Act
    $response = livewire(ListUsers::class);
    
    // Assert
    $response->assertSuccessful();
    
    // Test that the table contains our users
    foreach ($users as $user) {
        $response->assertSee($user->name);
        $response->assertSee($user->email);
    }
});
""",
            tags=["resource_test", "filament", "pest"]
        )
        
        # Form test template
        templates["form_test"] = TestTemplate(
            name="Filament Form Test",
            description="Template for testing a FilamentPHP form.",
            template="""<?php

use {resource_namespace}\\{resource_name}Resource;
use {resource_namespace}\\{resource_name}Resource\\Pages\\{page_class};
use {model_namespace}\\{model_name};
{use_statements}

/**
 * {test_description}
 */
test('{test_name}', function () {
    // Arrange
{arrange}
    
    // Act
{act}
    
    // Assert
{assertions}
});
""",
            example="""<?php

use App\\Filament\\Resources\\UserResource;
use App\\Filament\\Resources\\UserResource\\Pages\\CreateUser;
use App\\Models\\User;
use function Pest\\Livewire\\livewire;

/**
 * Test user resource create form
 */
test('can create a user', function () {
    // Arrange
    $newUserData = [
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => 'password',
        'password_confirmation' => 'password',
    ];
    
    // Act
    $response = livewire(CreateUser::class)
        ->fillForm($newUserData)
        ->call('create');
    
    // Assert
    $response->assertHasNoFormErrors();
    
    // Check that the user was created in the database
    $this->assertDatabaseHas('users', [
        'name' => 'Test User',
        'email' => 'test@example.com',
    ]);
});
""",
            tags=["form_test", "filament", "pest"]
        )
        
        # Table test template
        templates["table_test"] = TestTemplate(
            name="Filament Table Test",
            description="Template for testing a FilamentPHP table.",
            template="""<?php

use {resource_namespace}\\{resource_name}Resource;
use {resource_namespace}\\{resource_name}Resource\\Pages\\{page_class};
use {model_namespace}\\{model_name};
{use_statements}

/**
 * {test_description}
 */
test('{test_name}', function () {
    // Arrange
{arrange}
    
    // Act
{act}
    
    // Assert
{assertions}
});
""",
            example="""<?php

use App\\Filament\\Resources\\UserResource;
use App\\Filament\\Resources\\UserResource\\Pages\\ListUsers;
use App\\Models\\User;
use function Pest\\Livewire\\livewire;

/**
 * Test user resource table filters
 */
test('can filter users by active status', function () {
    // Arrange
    $activeUsers = User::factory()->count(3)->create(['status' => 'active']);
    $inactiveUsers = User::factory()->count(2)->create(['status' => 'inactive']);
    
    // Act & Assert
    livewire(ListUsers::class)
        ->assertCanSeeTableRecords($activeUsers)
        ->assertCanSeeTableRecords($inactiveUsers)
        ->filterTable('status', 'active')
        ->assertCanSeeTableRecords($activeUsers)
        ->assertCanNotSeeTableRecords($inactiveUsers);
});
""",
            tags=["table_test", "filament", "pest"]
        )
        
        # Dashboard test template
        templates["dashboard_test"] = TestTemplate(
            name="Filament Dashboard Test",
            description="Template for testing a FilamentPHP dashboard.",
            template="""<?php

use {page_namespace}\\{page_class};
{use_statements}

/**
 * {test_description}
 */
test('{test_name}', function () {
    // Arrange
{arrange}
    
    // Act
{act}
    
    // Assert
{assertions}
});
""",
            example="""<?php

use App\\Filament\\Pages\\Dashboard;
use function Pest\\Livewire\\livewire;

/**
 * Test dashboard page
 */
test('can view dashboard page', function () {
    // Arrange
    $this->actingAs(User::factory()->create());
    
    // Act
    $response = livewire(Dashboard::class);
    
    // Assert
    $response->assertSuccessful();
    $response->assertSee('Dashboard');
    $response->assertSee('Stats Overview');
});
""",
            tags=["dashboard_test", "filament", "pest"]
        )
        
        return templates
    
    def _load_test_patterns(self) -> Dict[str, Dict[str, str]]:
        """Load the test patterns."""
        return {
            "authentication": {
                "act_as_admin": """$this->actingAs(User::factory()->create([
    'email' => 'admin@example.com',
    'password' => bcrypt('password'),
    'is_admin' => true,
]));""",
                "act_as_user": """$this->actingAs(User::factory()->create());""",
                "login_as_admin": """$this->post(route('filament.auth.login'), [
    'email' => 'admin@example.com',
    'password' => 'password',
])->assertRedirect(route('filament.pages.dashboard'));""",
                "access_denied": """$response = $this->get(route('filament.resources.{resource}.index'));
$response->assertForbidden();""",
            },
            "resource_testing": {
                "list_page_load": """$response = livewire({resource_name}Resource\\Pages\\List{resource_name}::class);
$response->assertSuccessful();""",
                "create_page_load": """$response = livewire({resource_name}Resource\\Pages\\Create{resource_name}::class);
$response->assertSuccessful();""",
                "edit_page_load": """${model_var} = {model_name}::factory()->create();
$response = livewire({resource_name}Resource\\Pages\\Edit{resource_name}::class, ['record' => ${model_var}->id]);
$response->assertSuccessful();""",
                "view_page_load": """${model_var} = {model_name}::factory()->create();
$response = livewire({resource_name}Resource\\Pages\\View{resource_name}::class, ['record' => ${model_var}->id]);
$response->assertSuccessful();""",
            },
            "form_testing": {
                "fill_form": """$response = livewire({page_class}::class)
    ->fillForm([
{form_data}
    ]);""",
                "assert_form_exists": """$response->assertFormExists();""",
                "assert_form_field_exists": """$response->assertFormFieldExists('{field_name}');""",
                "assert_form_field_is_hidden": """$response->assertFormFieldIsHidden('{field_name}');""",
                "assert_form_field_is_visible": """$response->assertFormFieldIsVisible('{field_name}');""",
                "assert_form_field_has_error": """$response->assertHasFormErrors(['{field_name}']);""",
                "assert_form_field_has_no_error": """$response->assertHasNoFormErrors(['{field_name}']);""",
                "assert_has_no_form_errors": """$response->assertHasNoFormErrors();""",
                "save_form": """$response = $response->call('{save_method}');""",
                "assert_record_count": """$this->assertDatabaseCount('{table}', {count});""",
                "assert_record_exists": """$this->assertDatabaseHas('{table}', [
{columns}
]);""",
            },
            "table_testing": {
                "assert_can_see_table_records": """$response->assertCanSeeTableRecords(${collection});""",
                "assert_can_not_see_table_records": """$response->assertCanNotSeeTableRecords(${collection});""",
                "search_table": """$response = $response->searchTable('{search_term}');""",
                "filter_table": """$response = $response->filterTable('{filter_name}', '{filter_value}');""",
                "sort_table": """$response = $response->sortTable('{column_name}', '{direction}');""",
                "assert_table_action_visible": """$response->assertTableActionVisible('{action_name}', ${record});""",
                "assert_table_action_hidden": """$response->assertTableActionHidden('{action_name}', ${record});""",
                "assert_bulk_action_visible": """$response->assertTableBulkActionVisible('{action_name}');""",
                "assert_bulk_action_hidden": """$response->assertTableBulkActionHidden('{action_name}');""",
                "select_table_records": """$response = $response->selectTableRecords([${record}->id]);""",
                "call_table_action": """$response = $response->callTableAction('{action_name}', ${record}{action_data});""",
                "call_bulk_action": """$response = $response->callTableBulkAction('{action_name}'{action_data});""",
            },
        }
    
    def get_template(self, template_name: str) -> Optional[TestTemplate]:
        """Get a specific test template."""
        return self.templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, TestTemplate]:
        """Get all test templates."""
        return self.templates
    
    def get_test_pattern(self, category: str, pattern_name: str) -> Optional[str]:
        """Get a specific test pattern."""
        category_patterns = self.test_patterns.get(category)
        if category_patterns:
            return category_patterns.get(pattern_name)
        return None
    
    def get_category_patterns(self, category: str) -> Dict[str, str]:
        """Get all patterns for a specific category."""
        return self.test_patterns.get(category, {})
    
    def get_all_test_patterns(self) -> Dict[str, Dict[str, str]]:
        """Get all test patterns."""
        return self.test_patterns
    
    def generate_resource_test(self, test_name: str, resource_name: str, 
                              model_name: str, test_type: str = "list",
                              resource_namespace: str = "App\\Filament\\Resources", 
                              model_namespace: str = "App\\Models", 
                              test_description: str = None,
                              arrange: str = None, act: str = None, 
                              assertions: str = None, 
                              use_statements: List[str] = None) -> str:
        """
        Generate a FilamentPHP resource test.
        
        Args:
            test_name: The name of the test
            resource_name: The resource name
            model_name: The model name
            test_type: The type of test (list, create, edit, view)
            resource_namespace: The namespace of the resource
            model_namespace: The namespace of the model
            test_description: The description of the test
            arrange: Code for the arrange section
            act: Code for the act section
            assertions: Code for the assertions section
            use_statements: Additional use statements
            
        Returns:
            The generated resource test as a string
        """
        template = self.get_template("resource_test")
        if not template:
            return "Error: Resource test template not found"
            
        if not test_description:
            test_description = f"Test for {resource_name} resource {test_type} page"
            
        use_statements_str = ""
        if use_statements:
            use_statements_str = "\n".join(use_statements)
        else:
            use_statements_str = "use function Pest\\Livewire\\livewire;"
            
        page_class_mapping = {
            "list": f"List{resource_name}",
            "create": f"Create{resource_name}",
            "edit": f"Edit{resource_name}",
            "view": f"View{resource_name}",
        }
        
        page_class = page_class_mapping.get(test_type, f"List{resource_name}")
            
        return template.template.format(
            test_name=test_name,
            resource_name=resource_name,
            resource_namespace=resource_namespace,
            page_class=page_class,
            model_name=model_name,
            model_namespace=model_namespace,
            test_description=test_description,
            arrange=arrange or "    // Your arrange code here",
            act=act or "    // Your act code here",
            assertions=assertions or "    // Your assertions here",
            use_statements=use_statements_str
        )
    
    def generate_form_test(self, test_name: str, resource_name: str, 
                          model_name: str, form_type: str = "create",
                          resource_namespace: str = "App\\Filament\\Resources", 
                          model_namespace: str = "App\\Models", 
                          test_description: str = None,
                          arrange: str = None, act: str = None, 
                          assertions: str = None, 
                          use_statements: List[str] = None) -> str:
        """
        Generate a FilamentPHP form test.
        
        Args:
            test_name: The name of the test
            resource_name: The resource name
            model_name: The model name
            form_type: The type of form (create or edit)
            resource_namespace: The namespace of the resource
            model_namespace: The namespace of the model
            test_description: The description of the test
            arrange: Code for the arrange section
            act: Code for the act section
            assertions: Code for the assertions section
            use_statements: Additional use statements
            
        Returns:
            The generated form test as a string
        """
        template = self.get_template("form_test")
        if not template:
            return "Error: Form test template not found"
            
        if not test_description:
            test_description = f"Test for {resource_name} resource {form_type} form"
            
        use_statements_str = ""
        if use_statements:
            use_statements_str = "\n".join(use_statements)
        else:
            use_statements_str = "use function Pest\\Livewire\\livewire;"
            
        page_class_mapping = {
            "create": f"Create{resource_name}",
            "edit": f"Edit{resource_name}",
        }
        
        page_class = page_class_mapping.get(form_type, f"Create{resource_name}")
            
        return template.template.format(
            test_name=test_name,
            resource_name=resource_name,
            resource_namespace=resource_namespace,
            page_class=page_class,
            model_name=model_name,
            model_namespace=model_namespace,
            test_description=test_description,
            arrange=arrange or "    // Your arrange code here",
            act=act or "    // Your act code here",
            assertions=assertions or "    // Your assertions here",
            use_statements=use_statements_str
        )
    
    def generate_table_test(self, test_name: str, resource_name: str, 
                           model_name: str,
                           resource_namespace: str = "App\\Filament\\Resources", 
                           model_namespace: str = "App\\Models", 
                           test_description: str = None,
                           arrange: str = None, act: str = None, 
                           assertions: str = None, 
                           use_statements: List[str] = None) -> str:
        """
        Generate a FilamentPHP table test.
        
        Args:
            test_name: The name of the test
            resource_name: The resource name
            model_name: The model name
            resource_namespace: The namespace of the resource
            model_namespace: The namespace of the model
            test_description: The description of the test
            arrange: Code for the arrange section
            act: Code for the act section
            assertions: Code for the assertions section
            use_statements: Additional use statements
            
        Returns:
            The generated table test as a string
        """
        template = self.get_template("table_test")
        if not template:
            return "Error: Table test template not found"
            
        if not test_description:
            test_description = f"Test for {resource_name} resource table"
            
        use_statements_str = ""
        if use_statements:
            use_statements_str = "\n".join(use_statements)
        else:
            use_statements_str = "use function Pest\\Livewire\\livewire;"
            
        page_class = f"List{resource_name}"
            
        return template.template.format(
            test_name=test_name,
            resource_name=resource_name,
            resource_namespace=resource_namespace,
            page_class=page_class,
            model_name=model_name,
            model_namespace=model_namespace,
            test_description=test_description,
            arrange=arrange or "    // Your arrange code here",
            act=act or "    // Your act code here",
            assertions=assertions or "    // Your assertions here",
            use_statements=use_statements_str
        )
    
    def generate_dashboard_test(self, test_name: str, page_class: str,
                              page_namespace: str = "App\\Filament\\Pages", 
                              test_description: str = None,
                              arrange: str = None, act: str = None, 
                              assertions: str = None, 
                              use_statements: List[str] = None) -> str:
        """
        Generate a FilamentPHP dashboard test.
        
        Args:
            test_name: The name of the test
            page_class: The page class name
            page_namespace: The namespace of the page
            test_description: The description of the test
            arrange: Code for the arrange section
            act: Code for the act section
            assertions: Code for the assertions section
            use_statements: Additional use statements
            
        Returns:
            The generated dashboard test as a string
        """
        template = self.get_template("dashboard_test")
        if not template:
            return "Error: Dashboard test template not found"
            
        if not test_description:
            test_description = f"Test for {page_class} page"
            
        use_statements_str = ""
        if use_statements:
            use_statements_str = "\n".join(use_statements)
        else:
            use_statements_str = "use function Pest\\Livewire\\livewire;"
            
        return template.template.format(
            test_name=test_name,
            page_class=page_class,
            page_namespace=page_namespace,
            test_description=test_description,
            arrange=arrange or "    // Your arrange code here",
            act=act or "    // Your act code here",
            assertions=assertions or "    // Your assertions here",
            use_statements=use_statements_str
        )
    
    def suggest_test_strategy(self, resource_type: str, resource_elements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest an appropriate test strategy for Filament components.
        
        Args:
            resource_type: The type of resource (resource, widget, page, etc.)
            resource_elements: The extracted resource elements
            
        Returns:
            A dictionary with suggested test strategies
        """
        strategies = {
            "resource": {
                "type": "resource",
                "templates": ["resource_test", "form_test", "table_test"],
                "patterns": ["resource_testing", "form_testing", "table_testing"],
                "description": "Test resource pages, forms, and tables"
            },
            "widget": {
                "type": "widget",
                "templates": ["dashboard_test"],
                "patterns": ["authentication"],
                "description": "Test widget rendering and functionality"
            },
            "page": {
                "type": "page",
                "templates": ["dashboard_test"],
                "patterns": ["authentication", "form_testing"],
                "description": "Test custom page rendering and functionality"
            },
            "form": {
                "type": "form",
                "templates": ["form_test"],
                "patterns": ["form_testing"],
                "description": "Test form validation, submission, and error handling"
            },
            "table": {
                "type": "table",
                "templates": ["table_test"],
                "patterns": ["table_testing"],
                "description": "Test table filtering, sorting, and actions"
            }
        }
        
        return strategies.get(resource_type, {
            "type": "unknown",
            "templates": [],
            "patterns": [],
            "description": "Unknown resource type, unable to suggest specific test strategy"
        }) 