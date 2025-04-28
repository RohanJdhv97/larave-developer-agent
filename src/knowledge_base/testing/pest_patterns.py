"""
Laravel Pest Testing Patterns Knowledge Base.

This module provides a knowledge base of common Laravel Pest testing patterns
for different types of tests.
"""

from typing import Dict, List, Any


class LaravelPestPatterns:
    """Knowledge base for Laravel Pest testing patterns."""
    
    @staticmethod
    def get_patterns() -> Dict[str, Any]:
        """
        Get all Pest testing patterns.
        
        Returns:
            Dictionary of testing patterns categorized by test type
        """
        return {
            "feature_tests": {
                "http_tests": {
                    "basic_controller_test": {
                        "description": "Test a basic controller endpoint",
                        "pattern": """<?php

use App\\Models\\User;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

test('can view page', function () {
    // Arrange
    $user = User::factory()->create();
    
    // Act
    $response = $this->actingAs($user)->get('{route}');
    
    // Assert
    $response->assertStatus(200);
    $response->assertViewIs('{view}');
});""",
                        "when_to_use": "When testing basic controller endpoints that return views"
                    },
                    "api_endpoint_test": {
                        "description": "Test a JSON API endpoint",
                        "pattern": """<?php

use App\\Models\\User;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

test('can fetch data from API', function () {
    // Arrange
    $user = User::factory()->create();
    
    // Act
    $response = $this->actingAs($user)
                     ->getJson('{route}');
    
    // Assert
    $response->assertStatus(200)
             ->assertJsonStructure([
                 'data' => [
                     '*' => [
                         'id',
                         'name',
                         'created_at',
                     ]
                 ],
                 'meta' => [
                     'total'
                 ]
             ]);
});""",
                        "when_to_use": "When testing API endpoints that return JSON responses"
                    },
                    "form_submission_test": {
                        "description": "Test a form submission",
                        "pattern": """<?php

use App\\Models\\User;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

test('can submit form', function () {
    // Arrange
    $user = User::factory()->create();
    
    // Act
    $response = $this->actingAs($user)
                     ->post('{route}', [
                         'field1' => 'value1',
                         'field2' => 'value2',
                     ]);
    
    // Assert
    $response->assertRedirect('{redirect_route}');
    $this->assertDatabaseHas('{table}', [
        'field1' => 'value1',
        'field2' => 'value2',
    ]);
});""",
                        "when_to_use": "When testing form submissions that store data in the database"
                    },
                    "authentication_test": {
                        "description": "Test authentication requirements",
                        "pattern": """<?php

use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

test('guests cannot access protected page', function () {
    // Act
    $response = $this->get('{route}');
    
    // Assert
    $response->assertRedirect(route('login'));
});

test('authenticated users can access protected page', function () {
    // Arrange
    $user = User::factory()->create();
    
    // Act
    $response = $this->actingAs($user)
                     ->get('{route}');
    
    // Assert
    $response->assertStatus(200);
});""",
                        "when_to_use": "When testing routes that require authentication"
                    },
                    "authorization_test": {
                        "description": "Test authorization policies",
                        "pattern": """<?php

use App\\Models\\User;
use App\\Models\\{Model};
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

test('users can only access their own resources', function () {
    // Arrange
    $user1 = User::factory()->create();
    $user2 = User::factory()->create();
    
    $resource = {Model}::factory()->create([
        'user_id' => $user1->id
    ]);
    
    // Act - Authorized user
    $response1 = $this->actingAs($user1)
                      ->get(route('{route}', $resource->id));
    
    // Assert
    $response1->assertStatus(200);
    
    // Act - Unauthorized user
    $response2 = $this->actingAs($user2)
                      ->get(route('{route}', $resource->id));
                      
    // Assert
    $response2->assertStatus(403);
});""",
                        "when_to_use": "When testing routes that implement authorization policies"
                    },
                    "validation_test": {
                        "description": "Test request validation",
                        "pattern": """<?php

use App\\Models\\User;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

test('validation errors are returned', function () {
    // Arrange
    $user = User::factory()->create();
    
    // Act
    $response = $this->actingAs($user)
                     ->post('{route}', [
                         // Invalid data
                     ]);
    
    // Assert
    $response->assertStatus(302); // Redirects back with errors
    $response->assertSessionHasErrors(['{field}']);
});

test('validation passes with correct data', function () {
    // Arrange
    $user = User::factory()->create();
    
    // Act
    $response = $this->actingAs($user)
                     ->post('{route}', [
                         // Valid data
                         '{field}' => 'valid value',
                     ]);
    
    // Assert
    $response->assertSessionHasNoErrors();
    $response->assertRedirect();
});""",
                        "when_to_use": "When testing request validation rules"
                    }
                }
            },
            "unit_tests": {
                "service_tests": {
                    "basic_service_test": {
                        "description": "Test a service class method",
                        "pattern": """<?php

use App\\Services\\{Service};

test('{service} can perform action', function () {
    // Arrange
    $service = new {Service}();
    
    // Act
    $result = $service->{method}({parameters});
    
    // Assert
    expect($result)->toBe({expected});
});""",
                        "when_to_use": "When testing simple service methods without dependencies"
                    },
                    "service_with_dependencies_test": {
                        "description": "Test a service with dependencies",
                        "pattern": """<?php

use App\\Services\\{Service};
use App\\Contracts\\{DependencyInterface};
use Mockery;

test('{service} uses dependencies correctly', function () {
    // Arrange
    $dependency = Mockery::mock({DependencyInterface}::class);
    $dependency->shouldReceive('{method}')
               ->once()
               ->with({parameters})
               ->andReturn({return_value});
               
    $service = new {Service}($dependency);
    
    // Act
    $result = $service->{method}({parameters});
    
    // Assert
    expect($result)->toBe({expected});
});""",
                        "when_to_use": "When testing services that have dependencies which should be mocked"
                    }
                },
                "model_tests": {
                    "model_attributes_test": {
                        "description": "Test model attributes and casting",
                        "pattern": """<?php

use App\\Models\\{Model};

test('{model} has correct attributes', function () {
    // Arrange
    ${model} = {Model}::factory()->make([
        '{attribute}' => '{value}',
    ]);
    
    // Assert
    expect(${model}->{attribute})->toBe('{value}');
});

test('{model} casts attributes correctly', function () {
    // Arrange
    ${model} = {Model}::factory()->make([
        '{date_attribute}' => '2023-01-01',
        '{boolean_attribute}' => 1,
    ]);
    
    // Assert
    expect(${model}->{date_attribute})->toBeInstanceOf(\\Carbon\\Carbon::class);
    expect(${model}->{boolean_attribute})->toBeTrue();
});""",
                        "when_to_use": "When testing model attribute casting and accessors"
                    },
                    "model_relationships_test": {
                        "description": "Test model relationships",
                        "pattern": """<?php

use App\\Models\\{Model};
use App\\Models\\{RelatedModel};
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

test('{model} belongs to {related_model}', function () {
    // Arrange
    ${related_model} = {RelatedModel}::factory()->create();
    ${model} = {Model}::factory()->create([
        '{foreign_key}' => ${related_model}->id,
    ]);
    
    // Assert
    expect(${model}->{relationship}->id)->toBe(${related_model}->id);
});

test('{model} has many {related_models}', function () {
    // Arrange
    ${model} = {Model}::factory()->create();
    ${related_models} = {RelatedModel}::factory()->count(3)->create([
        '{foreign_key}' => ${model}->id,
    ]);
    
    // Assert
    expect(${model}->{relationship})->toHaveCount(3);
});""",
                        "when_to_use": "When testing model relationships like hasMany, belongsTo, etc."
                    },
                    "model_scopes_test": {
                        "description": "Test model query scopes",
                        "pattern": """<?php

use App\\Models\\{Model};
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

test('{model} scope filters correctly', function () {
    // Arrange
    {Model}::factory()->count(3)->create([
        '{field}' => '{value_1}',
    ]);
    
    {Model}::factory()->count(2)->create([
        '{field}' => '{value_2}',
    ]);
    
    // Act
    $filtered = {Model}::{scope}('{value_1}')->get();
    
    // Assert
    expect($filtered)->toHaveCount(3);
    expect($filtered->pluck('{field}')->all())
        ->each(fn ($item) => $item->toBe('{value_1}'));
});""",
                        "when_to_use": "When testing model query scopes that filter results"
                    }
                },
                "helper_tests": {
                    "helper_function_test": {
                        "description": "Test a helper function",
                        "pattern": """<?php

test('helper functions correctly', function () {
    // Arrange
    $input = {input};
    
    // Act
    $result = {helper_function}($input);
    
    // Assert
    expect($result)->toBe({expected});
});""",
                        "when_to_use": "When testing global helper functions"
                    }
                }
            },
            "integration_tests": {
                "queue_tests": {
                    "job_dispatched_test": {
                        "description": "Test a job is dispatched",
                        "pattern": """<?php

use App\\Jobs\\{Job};
use Illuminate\\Support\\Facades\\Queue;

test('job is dispatched', function () {
    // Arrange
    Queue::fake();
    
    // Act
    // Trigger action that should dispatch job
    
    // Assert
    Queue::assertPushed({Job}::class, function ($job) {
        return $job->{property} === {expected_value};
    });
});""",
                        "when_to_use": "When testing that a job is dispatched with the correct properties"
                    }
                },
                "event_tests": {
                    "event_dispatched_test": {
                        "description": "Test an event is dispatched",
                        "pattern": """<?php

use App\\Events\\{Event};
use Illuminate\\Support\\Facades\\Event;

test('event is dispatched', function () {
    // Arrange
    Event::fake();
    
    // Act
    // Trigger action that should dispatch event
    
    // Assert
    Event::assertDispatched({Event}::class, function ($event) {
        return $event->{property} === {expected_value};
    });
});""",
                        "when_to_use": "When testing that an event is dispatched with the correct properties"
                    }
                },
                "notification_tests": {
                    "notification_sent_test": {
                        "description": "Test a notification is sent",
                        "pattern": """<?php

use App\\Models\\User;
use App\\Notifications\\{Notification};
use Illuminate\\Support\\Facades\\Notification;

test('notification is sent', function () {
    // Arrange
    Notification::fake();
    $user = User::factory()->create();
    
    // Act
    // Trigger action that should send notification
    
    // Assert
    Notification::assertSentTo(
        $user,
        {Notification}::class,
        function ($notification, $channels) {
            return $notification->{property} === {expected_value};
        }
    );
});""",
                        "when_to_use": "When testing that a notification is sent to the correct users"
                    }
                },
                "mail_tests": {
                    "mail_sent_test": {
                        "description": "Test an email is sent",
                        "pattern": """<?php

use App\\Models\\User;
use App\\Mail\\{Mailable};
use Illuminate\\Support\\Facades\\Mail;

test('email is sent', function () {
    // Arrange
    Mail::fake();
    $user = User::factory()->create();
    
    // Act
    // Trigger action that should send email
    
    // Assert
    Mail::assertSent({Mailable}::class, function ($mail) use ($user) {
        return $mail->hasTo($user->email) &&
               $mail->{property} === {expected_value};
    });
});""",
                        "when_to_use": "When testing that an email is sent with the correct content"
                    }
                }
            },
            "test_setup": {
                "test_case_setup": {
                    "refresh_database": {
                        "description": "Set up tests with RefreshDatabase",
                        "pattern": """<?php

use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

// Your tests here
""",
                        "when_to_use": "When tests need a fresh database for each test"
                    },
                    "database_transactions": {
                        "description": "Set up tests with DatabaseTransactions",
                        "pattern": """<?php

use Illuminate\\Foundation\\Testing\\DatabaseTransactions;

uses(DatabaseTransactions::class);

// Your tests here
""",
                        "when_to_use": "When tests need database transactions that are rolled back after each test"
                    },
                    "with_faker": {
                        "description": "Set up tests with Faker data generator",
                        "pattern": """<?php

use Illuminate\\Foundation\\Testing\\WithFaker;

uses(WithFaker::class);

test('can use faker', function () {
    $name = $this->faker->name;
    $email = $this->faker->email;
    
    // Test with generated data
});
""",
                        "when_to_use": "When tests need randomly generated data"
                    },
                    "custom_test_case": {
                        "description": "Create a custom test case with shared setup",
                        "pattern": """<?php

use Tests\\TestCase;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(TestCase::class, RefreshDatabase::class)->beforeEach(function () {
    // Setup code to run before each test
    $this->user = User::factory()->create();
    $this->actingAs($this->user);
})->afterEach(function () {
    // Cleanup code to run after each test
})->in('Feature/Admin');

// Your tests here
""",
                        "when_to_use": "When several tests need the same setup and teardown logic"
                    }
                },
                "data_setup": {
                    "model_factories": {
                        "description": "Set up test data with model factories",
                        "pattern": """<?php

use App\\Models\\User;
use App\\Models\\Post;

test('example with factories', function () {
    // Create a user with 3 posts
    $user = User::factory()
        ->has(Post::factory()->count(3))
        ->create();
        
    expect($user->posts)->toHaveCount(3);
});
""",
                        "when_to_use": "When tests need complex model relationships"
                    },
                    "database_seeding": {
                        "description": "Seed the database for tests",
                        "pattern": """<?php

use Illuminate\\Foundation\\Testing\\RefreshDatabase;
use Database\\Seeders\\TestDatabaseSeeder;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->seed(TestDatabaseSeeder::class);
});

test('database has seeded data', function () {
    $this->assertDatabaseCount('users', 10);
    $this->assertDatabaseHas('roles', [
        'name' => 'Admin'
    ]);
});
""",
                        "when_to_use": "When tests need consistent seed data"
                    }
                }
            },
            "assertions": {
                "http_assertions": {
                    "status_assertions": {
                        "description": "Assert HTTP response status",
                        "pattern": """$response->assertStatus(200);
$response->assertOk();
$response->assertCreated();
$response->assertNoContent();
$response->assertForbidden();
$response->assertNotFound();
$response->assertUnauthorized();""",
                        "when_to_use": "When testing HTTP response status codes"
                    },
                    "redirect_assertions": {
                        "description": "Assert HTTP redirects",
                        "pattern": """$response->assertRedirect('/dashboard');
$response->assertRedirect(route('dashboard'));""",
                        "when_to_use": "When testing redirects after form submissions"
                    },
                    "view_assertions": {
                        "description": "Assert views and view data",
                        "pattern": """$response->assertViewIs('user.profile');
$response->assertViewHas('user');
$response->assertViewHas('user', $user);
$response->assertViewHasAll([
    'user' => $user,
    'posts' => $posts
]);
$response->assertViewMissing('admin');""",
                        "when_to_use": "When testing that the correct view is rendered with the right data"
                    },
                    "json_assertions": {
                        "description": "Assert JSON responses",
                        "pattern": """$response->assertJson([
    'name' => 'John Doe',
    'email' => 'john@example.com',
]);

$response->assertJsonPath('user.name', 'John Doe');

$response->assertJsonStructure([
    'data' => [
        '*' => [
            'id',
            'name',
            'email',
        ]
    ],
    'links',
    'meta',
]);

$response->assertJsonCount(3, 'data');""",
                        "when_to_use": "When testing API responses that return JSON"
                    }
                },
                "database_assertions": {
                    "database_has": {
                        "description": "Assert database records exist",
                        "pattern": """$this->assertDatabaseHas('users', [
    'email' => 'john@example.com',
]);

$this->assertDatabaseMissing('users', [
    'email' => 'nonexistent@example.com',
]);

$this->assertDatabaseCount('posts', 5);

$this->assertModelExists($user);

$this->assertSoftDeleted('posts', [
    'id' => 1,
]);""",
                        "when_to_use": "When testing that database operations succeeded"
                    }
                },
                "pest_expectations": {
                    "basic_expectations": {
                        "description": "Basic Pest expectations",
                        "pattern": """expect($value)->toBe(5);
expect($value)->toEqual($other);
expect($value)->toBeTrue();
expect($value)->toBeFalse();
expect($value)->toBeNull();
expect($value)->not->toBeNull();
expect($array)->toHaveCount(3);
expect($array)->toContain('value');
expect($array)->toContain(fn ($value) => $value > 3);""",
                        "when_to_use": "For basic value assertions"
                    },
                    "object_expectations": {
                        "description": "Object and collection expectations",
                        "pattern": """expect($object)->toBeInstanceOf(User::class);
expect($object)->toHaveProperty('name');
expect($object->name)->toBe('John');

expect($collection)->toHaveCount(3);
expect($collection->pluck('id'))->toContain(5);
expect($collection)->each(fn ($item) => $item->toBeInstanceOf(User::class));""",
                        "when_to_use": "When testing objects and collections"
                    },
                    "exception_expectations": {
                        "description": "Exception expectations",
                        "pattern": """expect(fn () => $service->process())->toThrow(\\Exception::class);
expect(fn () => $service->process())->toThrow(\\Exception::class, 'Error message');""",
                        "when_to_use": "When testing code that should throw exceptions"
                    }
                }
            }
        }
    
    @staticmethod
    def get_pattern_by_path(path: List[str]) -> Dict[str, Any]:
        """
        Get a specific pattern using a path of keys.
        
        Args:
            path: List of keys to traverse the patterns dictionary
            
        Returns:
            The pattern at the specified path or empty dict if not found
        """
        patterns = LaravelPestPatterns.get_patterns()
        current = patterns
        
        for key in path:
            if key in current:
                current = current[key]
            else:
                return {}
                
        return current
    
    @staticmethod
    def get_pattern_categories() -> List[str]:
        """
        Get all top-level pattern categories.
        
        Returns:
            List of pattern categories
        """
        return list(LaravelPestPatterns.get_patterns().keys())
    
    @staticmethod
    def search_patterns(query: str) -> List[Dict[str, Any]]:
        """
        Search patterns for a specific query.
        
        Args:
            query: Search term
            
        Returns:
            List of matching patterns with their paths
        """
        results = []
        patterns = LaravelPestPatterns.get_patterns()
        
        def search_recursive(current: Dict[str, Any], path: List[str] = None):
            if path is None:
                path = []
                
            for key, value in current.items():
                current_path = path + [key]
                
                if isinstance(value, dict):
                    if "description" in value and query.lower() in value["description"].lower():
                        results.append({
                            "path": current_path,
                            "pattern": value
                        })
                    elif "pattern" in value and query.lower() in value["pattern"].lower():
                        results.append({
                            "path": current_path,
                            "pattern": value
                        })
                    else:
                        search_recursive(value, current_path)
        
        search_recursive(patterns)
        return results 