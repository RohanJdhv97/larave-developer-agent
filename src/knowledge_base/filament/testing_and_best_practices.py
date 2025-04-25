"""
FilamentPHP Testing and Best Practices Knowledge Base

This module contains comprehensive knowledge about testing FilamentPHP applications
and following best practices, including PestPHP integration, performance optimization,
deployment considerations, and more.
"""

from typing import Dict, List, Any

# Overview of Testing in FilamentPHP
TESTING_OVERVIEW = """
Testing FilamentPHP applications is critical for ensuring reliability and maintainability.
Key testing areas include:

1. Panel rendering and authentication
2. Resource operations (list, create, edit, view, delete)
3. Form submission and validation
4. Table filtering, sorting, and actions
5. Livewire component interactions
6. API endpoints (when using API resources)
7. Permissions and authorization
8. Custom widgets and components

FilamentPHP works well with both PHPUnit and PestPHP testing frameworks, though
PestPHP is generally preferred for its more expressive syntax and better support
for testing Livewire components.
"""

# PestPHP Integration
PESTPHP_INTEGRATION = {
    "overview": """
    PestPHP provides an elegant, expressive syntax for testing PHP applications,
    making it particularly well-suited for testing FilamentPHP. Integrating PestPHP
    with FilamentPHP involves setting up the necessary packages and creating
    specialized test cases for panel components, resources, and other features.
    """,
    
    "installation": """
    # Install Pest PHP and required plugins
    composer require pestphp/pest --dev
    composer require pestphp/pest-plugin-laravel --dev
    composer require pestphp/pest-plugin-livewire --dev
    
    # Initialize Pest
    php artisan pest:install
    """,
    
    "configuration": """
    // Pest.php
    use Illuminate\\Foundation\\Testing\\LazilyRefreshDatabase;
    use Tests\\TestCase;
    
    uses(TestCase::class, LazilyRefreshDatabase::class)
        ->in('Feature');
    
    // Create a Filament test case helper
    use Filament\\Facades\\Filament;
    use Filament\\Pages\\Page;
    use Illuminate\\Testing\\TestResponse;
    use Livewire\\Livewire;
    
    function filamentTest($componentClass, $parameters = [])
    {
        return test()->livewireTest($componentClass, $parameters);
    }
    """
}

# Testing Resources
TESTING_RESOURCES = {
    "list_pages": {
        "description": "Testing resource list (index) pages",
        "examples": [
            """
            use App\\Filament\\Resources\\UserResource;
            use App\\Filament\\Resources\\UserResource\\Pages\\ListUsers;
            use App\\Models\\User;
            
            it('can render list page', function () {
                $this->actingAs(User::factory()->create());
                
                $response = $this->get(UserResource::getUrl('index'));
                
                $response->assertSuccessful();
            });
            
            it('can list users', function () {
                $users = User::factory()->count(10)->create();
                
                $this->actingAs(User::factory()->create());
                
                Livewire::test(ListUsers::class)
                    ->assertCanSeeTableRecords($users);
            });
            
            it('can sort users', function () {
                $users = User::factory()->count(10)->create();
                
                $this->actingAs(User::factory()->create());
                
                Livewire::test(ListUsers::class)
                    ->assertCanSeeTableRecords($users)
                    ->sortTable('name')
                    ->assertCanSeeTableRecords($users->sortBy('name')->pluck('id')->toArray(), inOrder: true);
            });
            """
        ]
    },
    "create_pages": {
        "description": "Testing resource creation pages and functionality",
        "examples": [
            """
            use App\\Filament\\Resources\\UserResource;
            use App\\Filament\\Resources\\UserResource\\Pages\\CreateUser;
            use App\\Models\\User;
            
            it('can render create page', function () {
                $this->actingAs(User::factory()->create());
                
                $response = $this->get(UserResource::getUrl('create'));
                
                $response->assertSuccessful();
            });
            
            it('can create user', function () {
                $this->actingAs(User::factory()->create());
                
                $userData = [
                    'name' => 'Test User',
                    'email' => 'test@example.com',
                    'password' => 'password',
                    'password_confirmation' => 'password',
                ];
                
                Livewire::test(CreateUser::class)
                    ->fillForm($userData)
                    ->call('create')
                    ->assertHasNoFormErrors();
                
                $this->assertDatabaseHas('users', [
                    'name' => $userData['name'],
                    'email' => $userData['email'],
                ]);
            });
            
            it('validates input', function () {
                $this->actingAs(User::factory()->create());
                
                Livewire::test(CreateUser::class)
                    ->fillForm([
                        'name' => '',
                        'email' => 'not-an-email',
                    ])
                    ->call('create')
                    ->assertHasFormErrors(['name', 'email']);
            });
            """
        ]
    },
    "edit_pages": {
        "description": "Testing resource editing pages and functionality",
        "examples": [
            """
            use App\\Filament\\Resources\\UserResource;
            use App\\Filament\\Resources\\UserResource\\Pages\\EditUser;
            use App\\Models\\User;
            
            it('can render edit page', function () {
                $this->actingAs(User::factory()->create());
                
                $user = User::factory()->create();
                
                $response = $this->get(UserResource::getUrl('edit', ['record' => $user]));
                
                $response->assertSuccessful();
            });
            
            it('can retrieve form data', function () {
                $this->actingAs(User::factory()->create());
                
                $user = User::factory()->create();
                
                Livewire::test(EditUser::class, ['record' => $user->getKey()])
                    ->assertFormSet([
                        'name' => $user->name,
                        'email' => $user->email,
                    ]);
            });
            
            it('can update user', function () {
                $this->actingAs(User::factory()->create());
                
                $user = User::factory()->create();
                $newData = [
                    'name' => 'Updated Name',
                    'email' => 'updated@example.com',
                ];
                
                Livewire::test(EditUser::class, ['record' => $user->getKey()])
                    ->fillForm($newData)
                    ->call('save')
                    ->assertHasNoFormErrors();
                
                $this->assertDatabaseHas('users', [
                    'id' => $user->id,
                    'name' => $newData['name'],
                    'email' => $newData['email'],
                ]);
            });
            """
        ]
    },
    "view_pages": {
        "description": "Testing resource view pages",
        "examples": [
            """
            use App\\Filament\\Resources\\UserResource;
            use App\\Filament\\Resources\\UserResource\\Pages\\ViewUser;
            use App\\Models\\User;
            
            it('can render view page', function () {
                $this->actingAs(User::factory()->create());
                
                $user = User::factory()->create();
                
                $response = $this->get(UserResource::getUrl('view', ['record' => $user]));
                
                $response->assertSuccessful();
            });
            
            it('displays correct user information', function () {
                $this->actingAs(User::factory()->create());
                
                $user = User::factory()->create();
                
                Livewire::test(ViewUser::class, ['record' => $user->getKey()])
                    ->assertSee($user->name)
                    ->assertSee($user->email);
            });
            """
        ]
    },
    "delete_actions": {
        "description": "Testing resource deletion actions",
        "examples": [
            """
            use App\\Filament\\Resources\\UserResource\\Pages\\ListUsers;
            use App\\Models\\User;
            
            it('can delete user', function () {
                $this->actingAs(User::factory()->create());
                
                $userToDelete = User::factory()->create();
                
                Livewire::test(ListUsers::class)
                    ->callTableAction('delete', $userToDelete)
                    ->assertNotified();
                
                $this->assertDatabaseMissing('users', [
                    'id' => $userToDelete->id,
                ]);
            });
            
            it('can bulk delete users', function () {
                $this->actingAs(User::factory()->create());
                
                $usersToDelete = User::factory()->count(3)->create();
                
                Livewire::test(ListUsers::class)
                    ->callTableBulkAction('delete', $usersToDelete)
                    ->assertNotified();
                
                foreach ($usersToDelete as $user) {
                    $this->assertDatabaseMissing('users', [
                        'id' => $user->id,
                    ]);
                }
            });
            """
        ]
    },
    "table_features": {
        "description": "Testing table filtering, searching, and pagination",
        "examples": [
            """
            use App\\Filament\\Resources\\UserResource\\Pages\\ListUsers;
            use App\\Models\\User;
            
            it('can search users', function () {
                $this->actingAs(User::factory()->create());
                
                $userA = User::factory()->create(['name' => 'John Doe']);
                $userB = User::factory()->create(['name' => 'Jane Smith']);
                
                Livewire::test(ListUsers::class)
                    ->assertCanSeeTableRecords([$userA, $userB])
                    ->searchTable('John')
                    ->assertCanSeeTableRecords([$userA])
                    ->assertCanNotSeeTableRecords([$userB]);
            });
            
            it('can filter users', function () {
                $this->actingAs(User::factory()->create());
                
                $admin = User::factory()->create(['is_admin' => true]);
                $user = User::factory()->create(['is_admin' => false]);
                
                Livewire::test(ListUsers::class)
                    ->assertCanSeeTableRecords([$admin, $user])
                    ->filterTable('is_admin', true)
                    ->assertCanSeeTableRecords([$admin])
                    ->assertCanNotSeeTableRecords([$user]);
            });
            
            it('can paginate users', function () {
                $this->actingAs(User::factory()->create());
                
                // Creating 25 users (assuming 10 per page)
                $users = User::factory()->count(25)->create();
                
                Livewire::test(ListUsers::class)
                    ->assertCanSeeTableRecords($users->take(10))
                    ->assertCanNotSeeTableRecords($users->skip(10)->take(10))
                    ->goToTablePage(2)
                    ->assertCanSeeTableRecords($users->skip(10)->take(10))
                    ->assertCanNotSeeTableRecords($users->take(10));
            });
            """
        ]
    }
}

# Testing Custom Components
TESTING_CUSTOM_COMPONENTS = {
    "widgets": {
        "description": "Testing Filament dashboard widgets",
        "examples": [
            """
            use App\\Filament\\Widgets\\StatsOverview;
            use App\\Models\\Order;
            use App\\Models\\User;
            
            it('shows correct statistics', function () {
                $this->actingAs(User::factory()->create(['is_admin' => true]));
                
                // Create test data
                User::factory()->count(10)->create();
                Order::factory()->count(5)->create(['status' => 'completed']);
                Order::factory()->count(3)->create(['status' => 'processing']);
                
                Livewire::test(StatsOverview::class)
                    ->assertSee('10 Users')
                    ->assertSee('5 Completed Orders')
                    ->assertSee('3 Processing Orders');
            });
            """
        ]
    },
    "forms": {
        "description": "Testing custom Filament forms",
        "examples": [
            """
            use App\\Filament\\Pages\\Settings;
            use App\\Models\\User;
            
            it('can save settings', function () {
                $this->actingAs(User::factory()->create(['is_admin' => true]));
                
                Livewire::test(Settings::class)
                    ->fillForm([
                        'site_name' => 'My Test Site',
                        'site_description' => 'This is a test site',
                        'maintenance_mode' => true,
                    ])
                    ->call('save')
                    ->assertHasNoFormErrors();
                
                // Check settings were saved
                $this->assertEquals('My Test Site', setting('site_name'));
                $this->assertEquals('This is a test site', setting('site_description'));
                $this->assertTrue((bool) setting('maintenance_mode'));
            });
            """
        ]
    },
    "actions": {
        "description": "Testing custom actions and modals",
        "examples": [
            """
            use App\\Filament\\Resources\\OrderResource\\Pages\\ListOrders;
            use App\\Models\\Order;
            use App\\Models\\User;
            
            it('can process order action', function () {
                $this->actingAs(User::factory()->create(['is_admin' => true]));
                
                $order = Order::factory()->create(['status' => 'pending']);
                
                Livewire::test(ListOrders::class)
                    ->callTableAction('process', $order)
                    ->assertHasNoActionErrors();
                
                $this->assertDatabaseHas('orders', [
                    'id' => $order->id,
                    'status' => 'processing',
                ]);
            });
            
            it('can open and submit modal action', function () {
                $this->actingAs(User::factory()->create(['is_admin' => true]));
                
                $order = Order::factory()->create(['status' => 'pending']);
                
                Livewire::test(ListOrders::class)
                    ->callTableAction('add_note', $order, data: [
                        'note' => 'Test note for this order',
                    ])
                    ->assertHasNoActionErrors();
                
                $this->assertDatabaseHas('order_notes', [
                    'order_id' => $order->id,
                    'content' => 'Test note for this order',
                ]);
            });
            """
        ]
    }
}

# Authentication Testing
AUTHENTICATION_TESTING = {
    "login": {
        "description": "Testing the login process",
        "examples": [
            """
            use App\\Models\\User;
            use function Pest\\Laravel\\post;
            
            it('can login to admin panel', function () {
                $user = User::factory()->create();
                
                $response = post(route('filament.auth.login'), [
                    'email' => $user->email,
                    'password' => 'password',
                ]);
                
                $response->assertRedirect(route('filament.pages.dashboard'));
                $this->assertAuthenticated();
            });
            
            it('validates incorrect credentials', function () {
                User::factory()->create(['email' => 'correct@example.com']);
                
                $response = post(route('filament.auth.login'), [
                    'email' => 'correct@example.com',
                    'password' => 'wrong-password',
                ]);
                
                $response->assertSessionHasErrors(['email']);
                $this->assertGuest();
            });
            """
        ]
    },
    "authorization": {
        "description": "Testing authorization and permissions",
        "examples": [
            """
            use App\\Filament\\Resources\\UserResource;
            use App\\Models\\User;
            use Spatie\\Permission\\Models\\Role;
            use Spatie\\Permission\\Models\\Permission;
            
            it('enforces resource permissions', function () {
                // Set up permissions
                $role = Role::create(['name' => 'editor']);
                $permission = Permission::create(['name' => 'view users']);
                $role->givePermissionTo($permission);
                
                // User without permission
                $regularUser = User::factory()->create();
                
                // User with permission
                $editorUser = User::factory()->create();
                $editorUser->assignRole('editor');
                
                // Test user without permission
                $this->actingAs($regularUser);
                $this->get(UserResource::getUrl('index'))->assertForbidden();
                
                // Test user with permission
                $this->actingAs($editorUser);
                $this->get(UserResource::getUrl('index'))->assertSuccessful();
            });
            """
        ]
    }
}

# Performance Best Practices
PERFORMANCE_BEST_PRACTICES = {
    "queries_optimization": {
        "description": "Optimizing database queries in FilamentPHP",
        "best_practices": [
            "Use eager loading to avoid N+1 queries",
            "Add strategic database indexes for frequently queried columns",
            "Use withCount() for relationship counts instead of separate queries",
            "Implement caching strategies for expensive or repeated queries",
            "Use searchable() with callback for optimized search queries",
            "Implement appropriate select() clauses to limit the columns being fetched"
        ],
        "examples": [
            """
            // Eager loading in a resource
            public static function getRelations(): array
            {
                return [
                    RelationManagers\\OrdersRelationManager::class,
                    RelationManagers\\CommentsRelationManager::class,
                ];
            }
            
            // Optimized table query
            protected function getTableQuery(): Builder
            {
                return parent::getTableQuery()
                    ->withCount(['orders', 'comments'])
                    ->with(['country', 'role']);
            }
            
            // Optimized searchable columns
            public static function getGloballySearchableAttributes(): array
            {
                return ['name', 'email', 'country.name'];
            }
            
            // Custom search query
            public $searchQuery = '';
            
            protected function getTableQuery(): Builder
            {
                return User::query()
                    ->when($this->searchQuery, function ($query, $search) {
                        $query->where('name', 'like', "%{$search}%")
                              ->orWhere('email', 'like', "%{$search}%");
                    });
            }
            """
        ]
    },
    "caching_strategies": {
        "description": "Implementing caching in FilamentPHP applications",
        "best_practices": [
            "Cache expensive widget data with appropriate TTL",
            "Use Laravel's cache system for dashboard statistics",
            "Implement model caching for frequently accessed data",
            "Clear relevant caches in Filament lifecycle hooks",
            "Consider implementing a read/write-through cache pattern",
            "Use cache tags to group related cached items"
        ],
        "examples": [
            """
            // Caching widget data
            protected function getData(): array
            {
                return Cache::remember('stats-widget-data', now()->addMinutes(15), function () {
                    return [
                        'users_count' => User::count(),
                        'orders_count' => Order::count(),
                        'revenue' => Order::where('status', 'completed')->sum('total'),
                    ];
                });
            }
            
            // Clear cache in a resource lifecycle hook
            protected static function afterSave(Model $record, array $data): void
            {
                Cache::forget('stats-widget-data');
                Cache::tags(['user-data'])->flush();
            }
            
            // Cache tags in service class
            public function getUserData(User $user)
            {
                return Cache::tags(['user-data', "user-{$user->id}"])->remember(
                    "user-{$user->id}-dashboard", 
                    now()->addHour(), 
                    fn () => $this->computeUserData($user)
                );
            }
            """
        ]
    },
    "ui_optimization": {
        "description": "Optimizing UI performance in FilamentPHP",
        "best_practices": [
            "Use lazy loading for tables with many records",
            "Add pagination to all tables and relation managers",
            "Implement debouncing for search inputs",
            "Use deferLoading option for secondary widgets",
            "Minimize the use of heavy components in list views",
            "Optimize image delivery for avatar and image fields"
        ],
        "examples": [
            """
            // Lazy loading a table
            protected function getTableRecordsPerPageSelectOptions(): array
            {
                return [10, 25, 50, 100];
            }
            
            // Defer loading for a widget
            protected static function getOptions(): array
            {
                return [
                    'deferLoading' => true,
                    'loadingIndicator' => true,
                ];
            }
            
            // Optimized image field
            ->imageColumn('avatar')
                ->disk('public')
                ->conversion('thumbnail')
                ->defaultImageUrl(url('/images/default-avatar.png'))
                ->square()
                ->extraImgAttributes(['loading' => 'lazy']),
                
            // Debounced search
            protected function getTableSearchDebounce(): ?string
            {
                return '500ms';
            }
            """
        ]
    }
}

# Deployment Best Practices
DEPLOYMENT_BEST_PRACTICES = {
    "preparation": {
        "description": "Preparing FilamentPHP applications for deployment",
        "best_practices": [
            "Run php artisan filament:upgrade to ensure compatibility",
            "Run php artisan optimize to cache configuration and routes",
            "Ensure proper file permissions on storage and cache directories",
            "Verify proper environment configuration (.env file)",
            "Run database migrations in production with --force flag",
            "Consider using a deployment tool like Laravel Deployer or Envoyer",
            "Implement a CI/CD pipeline for automated testing before deployment",
            "Create a detailed deployment checklist specific to your application"
        ]
    },
    "production_settings": {
        "description": "Configuring FilamentPHP for production environment",
        "best_practices": [
            "Set APP_DEBUG=false to prevent exposing sensitive information",
            "Implement proper error logging (consider services like Sentry or Flare)",
            "Configure HTTPS for all traffic",
            "Implement proper user authentication and password policies",
            "Set up proper queue workers for background processing",
            "Configure database connection pooling",
            "Implement rate limiting for form submissions",
            "Set up proper backup strategies"
        ],
        "examples": [
            """
            // Production config in AppServiceProvider
            public function boot()
            {
                if ($this->app->environment('production')) {
                    URL::forceScheme('https');
                    
                    // Configure Filament for production
                    Filament::registerRenderHook(
                        'head.end',
                        fn (): string => '<meta name="robots" content="noindex,nofollow">'
                    );
                    
                    // Add rate limiting to panel
                    Filament::middleware([
                        'throttle:filament',
                    ]);
                }
            }
            
            // .env settings
            APP_ENV=production
            APP_DEBUG=false
            APP_URL=https://admin.yoursite.com
            
            # Queue configuration
            QUEUE_CONNECTION=redis
            
            # Mail configuration
            MAIL_MAILER=ses
            """
        ]
    },
    "optimization": {
        "description": "Optimizing FilamentPHP for production environment",
        "best_practices": [
            "Precompile assets with npm run build",
            "Configure asset versioning for better caching",
            "Set up a CDN for static assets",
            "Implement proper Redis caching in production",
            "Optimize database indexes based on production query patterns",
            "Configure opcache for PHP performance",
            "Consider implementing read replicas for database scaling",
            "Use a load balancer if deploying multiple instances"
        ],
        "examples": [
            """
            // Cache configuration in config/cache.php
            'redis' => [
                'client' => env('REDIS_CLIENT', 'phpredis'),
                'options' => [
                    'cluster' => env('REDIS_CLUSTER', 'redis'),
                    'prefix' => env('REDIS_PREFIX', 'filament_'),
                ],
                'default' => [
                    'url' => env('REDIS_URL'),
                    'host' => env('REDIS_HOST', '127.0.0.1'),
                    'password' => env('REDIS_PASSWORD'),
                    'port' => env('REDIS_PORT', '6379'),
                    'database' => env('REDIS_CACHE_DB', '1'),
                ],
            ],
            
            // Opcache settings in php.ini
            opcache.enable=1
            opcache.memory_consumption=256
            opcache.interned_strings_buffer=16
            opcache.max_accelerated_files=10000
            opcache.validate_timestamps=0
            opcache.save_comments=1
            opcache.fast_shutdown=1
            """
        ]
    },
}

# Security Best Practices
SECURITY_BEST_PRACTICES = {
    "authentication": {
        "description": "Authentication security in FilamentPHP",
        "best_practices": [
            "Implement strong password policies",
            "Add two-factor authentication for admin users",
            "Enforce session timeouts for inactive users",
            "Use SSL encryption for all authentication traffic",
            "Implement IP-based restrictions for admin panel access",
            "Use throttling to prevent brute force attacks",
            "Configure proper CORS policy",
            "Audit login attempts and suspicious activities"
        ],
        "examples": [
            """
            // In config/filament.php
            'auth' => [
                'guard' => env('FILAMENT_AUTH_GUARD', 'web'),
                'pages' => [
                    'login' => \\App\\Filament\\Pages\\Auth\\CustomLogin::class,
                ],
                'providers' => [
                    'users' => [
                        'driver' => 'eloquent',
                        'model' => User::class,
                    ],
                ],
                'middleware' => [
                    'base' => [
                        HandledErrorMiddleware::class,
                        DisableBladeIconComponents::class,
                        DispatchServingFilamentEvent::class,
                    ],
                    'auth' => [
                        Authenticate::class,
                        'throttle:filament',
                        '2fa', // Custom 2FA middleware
                    ],
                ],
            ],
            
            // Session timeout in config/session.php
            'lifetime' => env('SESSION_LIFETIME', 120),
            'expire_on_close' => true,
            """
        ]
    },
    "authorization": {
        "description": "Authorization and permissions in FilamentPHP",
        "best_practices": [
            "Use role-based access control (RBAC)",
            "Implement granular permissions for each resource and action",
            "Use Filament Shield or similar plugin for permission management",
            "Apply the principle of least privilege for all users",
            "Regular audit permissions assigned to each role",
            "Implement proper guards for API access",
            "Use policies for complex authorization logic",
            "Document permission requirements for custom features"
        ],
        "examples": [
            """
            // Implement role-based access control with Shield
            FilamentShield::configurePermissionIdentifierUsing(
                fn ($resource) => $resource::getPermissionIdentifier()
            );
            
            // Custom Filament authorization logic
            protected function getHeaderActions(): array
            {
                return [
                    Actions\\EditAction::make()
                        ->visible(fn (): bool => auth()->user()->can('update', $this->getRecord())),
                    Actions\\DeleteAction::make()
                        ->visible(fn (): bool => auth()->user()->can('delete', $this->getRecord())),
                ];
            }
            
            // Resource policy
            public static function canViewAny(): bool
            {
                return auth()->user()->hasPermissionTo('view users');
            }
            
            public static function canCreate(): bool
            {
                return auth()->user()->hasPermissionTo('create users');
            }
            """
        ]
    },
    "data_validation": {
        "description": "Data validation and sanitization in FilamentPHP",
        "best_practices": [
            "Implement thorough form validation",
            "Sanitize all user inputs, especially rich text content",
            "Use Laravel's validation rules consistently",
            "Implement custom validation rules for complex requirements",
            "Validate file uploads for type, size, and content",
            "Use policy-based validation for context-aware rules",
            "Validate data both on client and server sides",
            "Implement proper error handling for validation failures"
        ],
        "examples": [
            """
            // Form validation
            public static function form(Form $form): Form
            {
                return $form
                    ->schema([
                        TextInput::make('name')
                            ->required()
                            ->maxLength(255),
                        TextInput::make('email')
                            ->email()
                            ->required()
                            ->unique(ignoreRecord: true),
                        TextInput::make('password')
                            ->password()
                            ->dehydrateStateUsing(fn ($state) => Hash::make($state))
                            ->dehydrated(fn ($state) => filled($state))
                            ->required(fn (string $context): bool => $context === 'create'),
                        FileUpload::make('avatar')
                            ->disk('public')
                            ->directory('avatars')
                            ->image()
                            ->maxSize(1024)
                            ->imageCropAspectRatio('1:1')
                            ->imageResizeMode('cover'),
                        RichEditor::make('bio')
                            ->maxLength(1000)
                            ->sanitizeHtml(),
                    ]);
            }
            
            // Custom validation rule
            public function rules()
            {
                return [
                    'data.username' => [
                        'required',
                        'string',
                        'max:255',
                        new UsernameRule(),
                    ],
                ];
            }
            
            // Custom sanitizer
            protected function mutateFormDataBeforeCreate(array $data): array
            {
                $data['bio'] = Purify::clean($data['bio']);
                
                return $data;
            }
            """
        ]
    }
}

# Function to get all the testing and best practices knowledge
def get_testing_and_best_practices_knowledge() -> Dict[str, Any]:
    """
    Returns the comprehensive FilamentPHP testing and best practices knowledge base
    """
    return {
        "testing_overview": TESTING_OVERVIEW,
        "pestphp_integration": PESTPHP_INTEGRATION,
        "testing_resources": TESTING_RESOURCES,
        "testing_custom_components": TESTING_CUSTOM_COMPONENTS,
        "authentication_testing": AUTHENTICATION_TESTING,
        "performance_best_practices": PERFORMANCE_BEST_PRACTICES,
        "deployment_best_practices": DEPLOYMENT_BEST_PRACTICES,
        "security_best_practices": SECURITY_BEST_PRACTICES
    } 