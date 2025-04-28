"""
Laravel Pest testing expertise module.

This module provides templates and utilities for generating Laravel Pest tests
following best practices and coding standards.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class PestTestTemplate(BaseModel):
    """Template for Laravel Pest tests."""
    name: str
    description: str
    template: str
    example: str
    tags: List[str] = Field(default_factory=list)


class LaravelPestTestingExpertise:
    """
    Laravel Pest testing expertise.
    
    This class provides templates and utilities for generating Laravel Pest tests
    following best practices and coding standards.
    """
    
    def __init__(self):
        """Initialize the Laravel Pest testing expertise module."""
        self.templates = self._load_templates()
        self.test_patterns = self._load_test_patterns()
        
    def _load_templates(self) -> Dict[str, PestTestTemplate]:
        """Load the Pest test templates."""
        templates = {}
        
        # Feature test template
        templates["feature_test"] = PestTestTemplate(
            name="Pest Feature Test",
            description="Template for a Laravel Pest feature test.",
            template="""<?php

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

use App\\Models\\User;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

/**
 * Test user creation through API
 */
test('can create a user via API', function () {
    // Arrange
    $userData = [
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => 'password',
        'password_confirmation' => 'password',
    ];
    
    // Act
    $response = $this->postJson('/api/users', $userData);
    
    // Assert
    $response->assertStatus(201)
        ->assertJsonStructure(['id', 'name', 'email', 'created_at']);
        
    $this->assertDatabaseHas('users', [
        'email' => 'test@example.com',
    ]);
});
""",
            tags=["feature_test", "api", "http"]
        )
        
        # Unit test template
        templates["unit_test"] = PestTestTemplate(
            name="Pest Unit Test",
            description="Template for a Laravel Pest unit test.",
            template="""<?php

use {class_namespace}\\{class_name};
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

use App\\Services\\PaymentService;
use App\\Contracts\\PaymentGatewayInterface;
use App\\Models\\User;
use App\\Models\\Payment;
use Mockery;

/**
 * Test payment processing service
 */
test('processes payment successfully', function () {
    // Arrange
    $user = User::factory()->create();
    $amount = 100.00;
    $description = 'Test payment';
    
    $gateway = Mockery::mock(PaymentGatewayInterface::class);
    $gateway->shouldReceive('charge')
        ->once()
        ->with(Mockery::on(function ($args) use ($user, $amount, $description) {
            return $args['amount'] === $amount &&
                   $args['description'] === $description &&
                   $args['user_id'] === $user->id;
        }))
        ->andReturn(['transaction_id' => 'test_transaction']);
    
    $paymentService = new PaymentService($gateway);
    
    // Act
    $payment = $paymentService->processPayment($user, $amount, $description);
    
    // Assert
    expect($payment)->toBeInstanceOf(Payment::class);
    expect($payment->amount)->toBe($amount);
    expect($payment->user_id)->toBe($user->id);
    expect($payment->transaction_id)->toBe('test_transaction');
    expect($payment->status)->toBe('completed');
});
""",
            tags=["unit_test", "mocking", "service"]
        )
        
        # Test with dataset template
        templates["dataset_test"] = PestTestTemplate(
            name="Pest Test with Dataset",
            description="Template for a Laravel Pest test with multiple datasets.",
            template="""<?php

use {class_namespace}\\{class_name};
{use_statements}

/**
 * {test_description}
 */
test('{test_name}', function ({parameters}) {
    // Arrange
{arrange}
    
    // Act
{act}
    
    // Assert
{assertions}
})->with([
{datasets}
]);
""",
            example="""<?php

use App\\Services\\Calculator;

/**
 * Test calculator addition with different values
 */
test('calculator adds two numbers correctly', function ($a, $b, $expected) {
    // Arrange
    $calculator = new Calculator();
    
    // Act
    $result = $calculator->add($a, $b);
    
    // Assert
    expect($result)->toBe($expected);
})->with([
    [1, 1, 2],
    [2, 2, 4],
    [0, 5, 5],
    [-1, 1, 0],
    [0.5, 0.5, 1],
]);
""",
            tags=["dataset", "data_provider", "parameterized"]
        )
        
        return templates
    
    def _load_test_patterns(self) -> Dict[str, Dict[str, str]]:
        """Load the Pest test patterns."""
        return {
            "http_tests": {
                "get_request": """$response = $this->get('{route}');""",
                "post_request": """$response = $this->post('{route}', {data});""",
                "put_request": """$response = $this->put('{route}', {data});""",
                "patch_request": """$response = $this->patch('{route}', {data});""",
                "delete_request": """$response = $this->delete('{route}');""",
                "json_get_request": """$response = $this->getJson('{route}');""",
                "json_post_request": """$response = $this->postJson('{route}', {data});""",
                "json_put_request": """$response = $this->putJson('{route}', {data});""",
                "json_patch_request": """$response = $this->patchJson('{route}', {data});""",
                "json_delete_request": """$response = $this->deleteJson('{route}');""",
                "authenticate": """$this->actingAs({user});""",
                "assert_status": """$response->assertStatus({status});""",
                "assert_redirect": """$response->assertRedirect('{route}');""",
                "assert_json": """$response->assertJson({data});""",
                "assert_json_structure": """$response->assertJsonStructure({structure});""",
                "assert_view": """$response->assertViewIs('{view}');""",
                "assert_see": """$response->assertSee('{text}');""",
                "assert_db_has": """$this->assertDatabaseHas('{table}', {data});""",
                "assert_db_missing": """$this->assertDatabaseMissing('{table}', {data});""",
            },
            "model_assertions": {
                "expect_instance": """expect({variable})->toBeInstanceOf({class_name});""",
                "expect_equals": """expect({variable})->toBe({expected});""",
                "expect_not_equals": """expect({variable})->not->toBe({expected});""",
                "expect_true": """expect({variable})->toBeTrue();""",
                "expect_false": """expect({variable})->toBeFalse();""",
                "expect_null": """expect({variable})->toBeNull();""",
                "expect_not_null": """expect({variable})->not->toBeNull();""",
                "expect_empty": """expect({variable})->toBeEmpty();""",
                "expect_count": """expect({variable})->toHaveCount({count});""",
                "expect_contains": """expect({variable})->toContain({expected});""",
                "expect_key": """expect({variable})->toHaveKey('{key}');""",
                "expect_keys": """expect({variable})->toHaveKeys([{keys}]);""",
                "expect_property": """expect({variable})->{property}->toBe({expected});""",
            },
            "mock_patterns": {
                "mock_class": """$mock = Mockery::mock({class_name});""",
                "mock_spy": """$spy = Mockery::spy({class_name});""",
                "mock_should_receive": """$mock->shouldReceive('{method}')
    ->once()
    ->with({parameters})
    ->andReturn({return_value});""",
                "mock_spy_should_have_received": """$spy->shouldHaveReceived('{method}')->once()->with({parameters});""",
                "mock_injection": """$this->instance({class_name}::class, $mock);""",
                "mock_facade": """
{facade_name}::shouldReceive('{method}')
    ->once()
    ->with({parameters})
    ->andReturn({return_value});
""",
                "mock_event_fake": """Event::fake([{events}]);""",
                "mock_event_assert": """Event::assertDispatched({event}::class);""",
                "mock_notification_fake": """Notification::fake();""",
                "mock_notification_assert": """Notification::assertSentTo({user}, {notification}::class);""",
                "mock_mail_fake": """Mail::fake();""",
                "mock_mail_assert": """Mail::assertSent({mailable}::class);""",
                "mock_bus_fake": """Bus::fake();""",
                "mock_bus_assert": """Bus::assertDispatched({job}::class);""",
                "mock_storage_fake": """Storage::fake('public');""",
                "mock_storage_assert": """Storage::disk('public')->assertExists('{path}');""",
            },
            "test_setup": {
                "refresh_database": """use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);""",
                "transaction": """use Illuminate\\Foundation\\Testing\\WithFaker;
use Illuminate\\Foundation\\Testing\\DatabaseTransactions;

uses(DatabaseTransactions::class);""",
                "with_faker": """use Illuminate\\Foundation\\Testing\\WithFaker;

uses(WithFaker::class);""",
                "model_factory": """${model} = {model}::factory()->create({attributes});""",
                "model_factory_count": """${collection} = {model}::factory()->count({count})->create({attributes});""",
                "model_factory_state": """${model} = {model}::factory()->state({state})->create();""",
                "model_factory_for": """${model} = {parent}::factory()
    ->has({related}::factory()->count({count}), '{relationship}')
    ->create();""",
            }
        }
    
    def get_template(self, template_name: str) -> Optional[PestTestTemplate]:
        """Get a specific test template."""
        return self.templates.get(template_name)
    
    def get_all_templates(self) -> Dict[str, PestTestTemplate]:
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
    
    def generate_feature_test(self, test_name: str, model_name: str = None, 
                             model_namespace: str = "App\\Models", 
                             test_description: str = None,
                             arrange: str = None, act: str = None, 
                             assert_statements: str = None, 
                             use_statements: List[str] = None) -> str:
        """
        Generate a feature test for Laravel Pest.
        
        Args:
            test_name: The name of the test
            model_name: The model being tested
            model_namespace: The namespace of the model
            test_description: The description of the test
            arrange: Code for the arrange section
            act: Code for the act section
            assert_statements: Code for the assert section
            use_statements: Additional use statements
            
        Returns:
            The generated feature test as a string
        """
        template = self.get_template("feature_test")
        if not template:
            return "Error: Feature test template not found"
            
        if not test_description:
            test_description = f"Test for {test_name}"
            
        use_statements_str = ""
        if use_statements:
            use_statements_str = "\n".join(use_statements)
            
        return template.template.format(
            test_name=test_name,
            model_name=model_name or "Model",
            model_namespace=model_namespace,
            test_description=test_description,
            arrange=arrange or "    // Your arrange code here",
            act=act or "    // Your act code here",
            assertions=assert_statements or "    // Your assertions here",
            use_statements=use_statements_str
        )
    
    def generate_unit_test(self, test_name: str, class_name: str = None, 
                          class_namespace: str = "App\\Services", 
                          test_description: str = None,
                          arrange: str = None, act: str = None, 
                          assert_statements: str = None, 
                          use_statements: List[str] = None) -> str:
        """
        Generate a unit test for Laravel Pest.
        
        Args:
            test_name: The name of the test
            class_name: The class being tested
            class_namespace: The namespace of the class
            test_description: The description of the test
            arrange: Code for the arrange section
            act: Code for the act section
            assert_statements: Code for the assert section
            use_statements: Additional use statements
            
        Returns:
            The generated unit test as a string
        """
        template = self.get_template("unit_test")
        if not template:
            return "Error: Unit test template not found"
            
        if not test_description:
            test_description = f"Test for {test_name}"
            
        use_statements_str = ""
        if use_statements:
            use_statements_str = "\n".join(use_statements)
            
        return template.template.format(
            test_name=test_name,
            class_name=class_name or "Service",
            class_namespace=class_namespace,
            test_description=test_description,
            arrange=arrange or "    // Your arrange code here",
            act=act or "    // Your act code here",
            assertions=assert_statements or "    // Your assertions here",
            use_statements=use_statements_str
        )
    
    def generate_dataset_test(self, test_name: str, class_name: str = None, 
                             class_namespace: str = "App\\Services", 
                             test_description: str = None,
                             parameters: str = None,
                             arrange: str = None, act: str = None, 
                             assert_statements: str = None, 
                             datasets: List[str] = None,
                             use_statements: List[str] = None) -> str:
        """
        Generate a dataset test for Laravel Pest.
        
        Args:
            test_name: The name of the test
            class_name: The class being tested
            class_namespace: The namespace of the class
            test_description: The description of the test
            parameters: Parameters for the test function
            arrange: Code for the arrange section
            act: Code for the act section
            assert_statements: Code for the assert section
            datasets: List of dataset entries
            use_statements: Additional use statements
            
        Returns:
            The generated dataset test as a string
        """
        template = self.get_template("dataset_test")
        if not template:
            return "Error: Dataset test template not found"
            
        if not test_description:
            test_description = f"Test for {test_name} with different inputs"
            
        use_statements_str = ""
        if use_statements:
            use_statements_str = "\n".join(use_statements)
        
        datasets_str = ""
        if datasets:
            datasets_str = "\n".join([f"    {dataset}," for dataset in datasets])
            
        return template.template.format(
            test_name=test_name,
            class_name=class_name or "Service",
            class_namespace=class_namespace,
            test_description=test_description,
            parameters=parameters or "array $data",
            arrange=arrange or "    // Your arrange code here",
            act=act or "    // Your act code here",
            assertions=assert_statements or "    // Your assertions here",
            datasets=datasets_str or "    // Your datasets here",
            use_statements=use_statements_str
        )
    
    def analyze_code_for_test_generation(self, code: str) -> Dict[str, Any]:
        """
        Analyze Laravel code to extract testable components.
        
        Args:
            code: The Laravel code to analyze
            
        Returns:
            A dictionary with extracted testable elements
        """
        # This would be a more complex implementation to extract methods,
        # parameters, return types, etc. from code for test generation
        # Simplified implementation for now
        return {
            "class_name": "ExtractedClass",
            "namespace": "App\\ExtractedNamespace",
            "methods": [
                {"name": "extractedMethod", "params": [], "return_type": "void"}
            ],
            "properties": []
        }
    
    def suggest_test_strategy(self, file_type: str, code_elements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest an appropriate test strategy based on code analysis.
        
        Args:
            file_type: The type of file (controller, model, service, etc.)
            code_elements: The extracted code elements
            
        Returns:
            A dictionary with suggested test strategies
        """
        strategies = {
            "controller": {
                "type": "feature",
                "templates": ["feature_test"],
                "patterns": ["http_tests"],
                "assertions": ["assert_status", "assert_json"],
                "description": "Test controller endpoints with HTTP requests and response assertions"
            },
            "model": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["model_assertions", "test_setup"],
                "assertions": ["expect_instance", "expect_property"],
                "description": "Test model attributes, relationships, and scopes"
            },
            "service": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["mock_patterns", "model_assertions"],
                "assertions": ["expect_equals", "expect_instance"],
                "description": "Test service methods with mocked dependencies"
            },
            "repository": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["test_setup", "model_assertions"],
                "assertions": ["expect_count", "expect_instance"],
                "description": "Test repository query methods with database assertions"
            },
            "middleware": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["mock_patterns", "http_tests"],
                "assertions": ["assert_status", "expect_equals"],
                "description": "Test middleware behavior with request and response handling"
            },
            "job": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["mock_patterns", "model_assertions"],
                "assertions": ["expect_true", "expect_instance"],
                "description": "Test job execution with mocked dependencies"
            },
            "mail": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["mock_patterns"],
                "assertions": ["expect_instance", "expect_true"],
                "description": "Test mail content and delivery with mocked mailer"
            },
            "event": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["mock_patterns"],
                "assertions": ["expect_true", "expect_instance"],
                "description": "Test event dispatch and handling"
            },
            "listener": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["mock_patterns", "model_assertions"],
                "assertions": ["expect_true", "expect_instance"],
                "description": "Test event listener behavior"
            },
            "command": {
                "type": "unit",
                "templates": ["unit_test"],
                "patterns": ["mock_patterns", "model_assertions"],
                "assertions": ["expect_equals", "expect_true"],
                "description": "Test command execution with mocked dependencies"
            }
        }
        
        return strategies.get(file_type, {
            "type": "unknown",
            "templates": [],
            "patterns": [],
            "assertions": [],
            "description": "Unknown file type, unable to suggest specific test strategy"
        }) 