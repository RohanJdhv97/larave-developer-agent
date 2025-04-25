"""
FilamentPHP Plugins and Extensions Knowledge Base

This module contains comprehensive knowledge about FilamentPHP plugins and extensions,
including popular plugins, their features, integration approaches, and techniques for building custom plugins.
"""

from typing import Dict, List, Any

# Overview of FilamentPHP plugin system
PLUGINS_OVERVIEW = """
FilamentPHP's plugin system provides a flexible architecture for extending functionality through:

1. First-party plugins - Official plugins developed by the FilamentPHP team
2. Third-party plugins - Community-developed extensions available via Packagist
3. Custom plugins - Organization-specific extensions built for specific needs

Plugins can extend nearly any aspect of FilamentPHP, including:
- Adding new form fields, table columns, infolist entries, and actions
- Creating dedicated panel plugins that add new features to the admin panel
- Providing theme modifications and UI enhancements
- Integrating with other services and packages
- Offering pre-built resources for common models/features
"""

# Official Plugins
OFFICIAL_PLUGINS = {
    "filament/spatie-laravel-media-library-plugin": {
        "description": "Integration with Spatie's Media Library package for advanced file uploads and management",
        "features": [
            "Dedicated form fields for managing media collections",
            "Table columns for displaying media",
            "Infolist entries for media preview", 
            "Support for multiple collections",
            "Integration with Media Library's conversions and responsive images"
        ],
        "installation": """
        composer require filament/spatie-laravel-media-library-plugin
        """,
        "usage_example": """
        use Filament\\Forms\\Components\\SpatieMediaLibraryFileUpload;
        
        SpatieMediaLibraryFileUpload::make('avatar')
            ->collection('avatars')
            ->image()
            ->avatar()
            ->conversion('thumbnail')
            ->responsiveImages()
            ->preserveFilenames()
            ->maxFiles(1)
        """
    },
    "filament/spatie-laravel-tags-plugin": {
        "description": "Integration with Spatie's Laravel Tags package for managing tags",
        "features": [
            "Form fields for managing tags",
            "Table columns for displaying tag lists",
            "Support for tag types and custom tag models",
            "Tag creation and suggestions"
        ],
        "installation": """
        composer require filament/spatie-laravel-tags-plugin
        """,
        "usage_example": """
        use Filament\\Forms\\Components\\SpatieTagsInput;
        
        SpatieTagsInput::make('tags')
            ->type('categories')
            ->suggestions([
                'Laravel',
                'PHP',
                'Filament',
                'Livewire',
                'AlpineJS',
                'TailwindCSS',
            ])
        """
    },
    "filament/spatie-laravel-translatable-plugin": {
        "description": "Integration with Spatie's Laravel Translatable package for content localization",
        "features": [
            "Form fields for managing translatable content",
            "Multi-language content editing",
            "Locale switcher in the admin panel",
            "Validation for translatable fields"
        ],
        "installation": """
        composer require filament/spatie-laravel-translatable-plugin
        """,
        "usage_example": """
        use Filament\\Forms\\Components\\SpatieMediaLibraryFileUpload;
        use Filament\\Forms\\Components\\Tabs;
        use Filament\\Forms\\Components\\Tabs\\Tab;
        
        // Using translatable tabs approach
        Tabs::make('Translations')
            ->tabs([
                Tab::make('English')
                    ->schema([
                        TextInput::make('title')
                            ->label('Title'),
                        MarkdownEditor::make('content')
                            ->label('Content'),
                    ]),
                Tab::make('Spanish')
                    ->schema([
                        TextInput::make('title')
                            ->label('Title')
                            ->translateLabel(),
                        MarkdownEditor::make('content')
                            ->label('Content')
                            ->translateLabel(),
                    ])
                    ->locale('es'),
            ])
            ->columnSpanFull()
        """
    },
    "filament/notifications": {
        "description": "Global notifications system for FilamentPHP",
        "features": [
            "Toast notifications from anywhere in your app",
            "Success, warning, info, and danger notification types",
            "Persistent and auto-disappearing notifications",
            "Notification actions and links",
            "Database-backed notifications queue"
        ],
        "installation": """
        composer require filament/notifications
        php artisan notifications:install
        """,
        "usage_example": """
        use Filament\\Notifications\\Notification;
        
        // Basic notification
        Notification::make()
            ->title('Saved successfully')
            ->success()
            ->send();
            
        // Advanced notification with actions
        Notification::make()
            ->title('New user registered')
            ->body('John Doe has registered for an account.')
            ->actions([
                Action::make('view')
                    ->button()
                    ->url(route('filament.resources.users.edit', $user)),
                Action::make('approve')
                    ->button()
                    ->color('success')
                    ->action(fn () => $user->approve()),
            ])
            ->persistent()
            ->warning()
            ->send();
        """
    },
    "filament/actions": {
        "description": "Stand-alone package for creating Filament actions outside panel",
        "features": [
            "Use Filament-like actions in Livewire components",
            "Action modals, slideovers, and buttons",
            "Form actions with validation",
            "Action groups",
            "Confirmations and error handling"
        ],
        "installation": """
        composer require filament/actions
        """,
        "usage_example": """
        use Filament\\Actions\\Concerns\\InteractsWithActions;
        use Filament\\Actions\\Contracts\\HasActions;
        use Filament\\Actions\\Action;
        use Livewire\\Component;
        
        class ManageUsers extends Component implements HasActions
        {
            use InteractsWithActions;
            
            public function deleteAction(): Action
            {
                return Action::make('delete')
                    ->color('danger')
                    ->requiresConfirmation()
                    ->action(function () {
                        // Delete logic
                    });
            }
        }
        """
    }
}

# Popular Community Plugins
COMMUNITY_PLUGINS = {
    "filament-shield": {
        "package": "bezhansalleh/filament-shield",
        "description": "Role and permission management plugin for FilamentPHP",
        "features": [
            "GUI for managing roles and permissions",
            "Automatic detection of Filament resources",
            "Policy generation",
            "Fine-grained access control for panel features",
            "Super admin role configuration"
        ],
        "installation": """
        composer require bezhansalleh/filament-shield
        php artisan shield:install
        php artisan shield:generate
        """,
        "usage_example": """
        // In AppServiceProvider
        use Illuminate\\Support\\ServiceProvider;
        use BezhanSalleh\\FilamentShield\\FilamentShield;
        
        class AppServiceProvider extends ServiceProvider
        {
            public function boot()
            {
                FilamentShield::configurePermissionIdentifierUsing(
                    function ($resource) {
                        return $resource::getPermissionIdentifier();
                    }
                );
                
                // Configure super admin role name
                FilamentShield::setRoleName('super-admin');
            }
        }
        """
    },
    "filament-breezy": {
        "package": "jeffgreco13/filament-breezy",
        "description": "User profile and authentication features for FilamentPHP",
        "features": [
            "Two-factor authentication",
            "Profile management",
            "Password confirmation and reset",
            "Custom login/registration",
            "Sanctum API tokens",
            "Email verification"
        ],
        "installation": """
        composer require jeffgreco13/filament-breezy
        php artisan vendor:publish --tag=filament-breezy-config
        """,
        "usage_example": """
        // In config/filament-breezy.php
        return [
            'enable_2fa' => true,
            'enable_registration' => true,
            'auth_card_max_w' => 'md',
            'password_confirmation_auto_enable' => true,
            'password_confirmation_timeout' => 300, // seconds
            'enable_profile_page' => true,
            'profile_page_url' => 'profile',
            'enable_sanctum' => true,
            'sanctum_permissions' => ['create', 'read', 'update', 'delete'],
        ];
        """
    },
    "filament-export": {
        "package": "3x1io/filament-excel",
        "description": "Export data to Excel, CSV, and other formats in Filament",
        "features": [
            "Export Table data to Excel/CSV/PDF",
            "Configurable columns and formatting",
            "Custom headers and styling",
            "Filtering support"
        ],
        "installation": """
        composer require 3x1io/filament-excel
        """,
        "usage_example": """
        use Filament\\Tables\\Actions\\BulkAction;
        use AlperenErsoy\\FilamentExport\\Actions\\FilamentExportBulkAction;
        
        public static function table(Table $table): Table
        {
            return $table
                ->columns([
                    // Your columns...
                ])
                ->bulkActions([
                    FilamentExportBulkAction::make('export')
                        ->fileName('My Custom Export')
                        ->timeFormat('m d Y')
                        ->defaultFormat('xlsx')
                        ->disableAdditionalColumns()
                        ->disableFilterColumns()
                ])
        }
        """
    },
    "filament-charts": {
        "package": "leandrocfe/filament-apex-charts",
        "description": "ApexCharts integration for FilamentPHP with reactive charts",
        "features": [
            "Line, bar, pie, radar charts and more",
            "Real-time chart updates",
            "Widget integration",
            "Customizable styles and colors",
            "Data filters and date ranges"
        ],
        "installation": """
        composer require leandrocfe/filament-apex-charts
        """,
        "usage_example": """
        use Leandrocfe\FilamentApexCharts\\Widgets\\ApexChartWidget;
        
        class BlogPostsChart extends ApexChartWidget
        {
            protected static ?string $heading = 'Blog Posts';
            protected static string $chartId = 'blogPostsChart';
            protected static ?int $sort = 2;
            protected static ?string $filter = 'month';
            protected static ?array $filterOptions = [
                'day' => 'Daily',
                'week' => 'Weekly',
                'month' => 'Monthly',
                'year' => 'Yearly',
            ];
            
            protected function getOptions(): array
            {
                $data = $this->getData();
                return [
                    'chart' => [
                        'type' => 'bar',
                        'height' => 300,
                    ],
                    'series' => [
                        [
                            'name' => 'Blog Posts',
                            'data' => $data['visits'],
                        ],
                    ],
                    'xaxis' => [
                        'categories' => $data['dates'],
                        'labels' => [
                            'style' => [
                                'fontFamily' => 'inherit',
                            ],
                        ],
                    ],
                ];
            }
            
            protected function getData(): array
            {
                $filter = $this->filter;
                
                // Query your data based on the filter
                
                return [
                    'dates' => ['Jan', 'Feb', 'Mar'],
                    'visits' => [150, 320, 280],
                ];
            }
        }
        """
    },
    "filament-map": {
        "package": "cheesegrits/filament-google-maps",
        "description": "Google Maps integration for Filament with geocoding",
        "features": [
            "Map field for forms",
            "Map column for tables",
            "Geocoding support",
            "Multiple map styles",
            "Custom markers and infowindows"
        ],
        "installation": """
        composer require cheesegrits/filament-google-maps
        php artisan vendor:publish --tag=filament-google-maps-config
        """,
        "usage_example": """
        use Cheesegrits\\FilamentGoogleMaps\\Fields\\Map;
        
        Map::make('location')
            ->autocomplete('address')
            ->autocompleteReverse()
            ->defaultZoom(15)
            ->defaultLocation([51.5074, -0.1278])
            ->mapControls([
                'mapTypeControl' => true,
                'scaleControl' => true,
                'streetViewControl' => true,
                'rotateControl' => true,
                'fullscreenControl' => true,
                'searchBoxControl' => false,
                'zoomControl' => true,
            ])
            ->height('400px')
        """
    }
}

# Custom Plugin Development
CUSTOM_PLUGIN_DEVELOPMENT = {
    "Plugin Components": {
        "description": "Core components that can be included in FilamentPHP plugins",
        "components": [
            "Form fields",
            "Table columns",
            "Table filters",
            "Actions",
            "Widgets",
            "Pages",
            "Infolist entries",
            "Panel plugin providers",
            "Assets (CSS, JS, images)"
        ]
    },
    "Plugin Structure": {
        "description": "Recommended structure for FilamentPHP plugins",
        "structure": """
        your-plugin/
        ├── composer.json
        ├── LICENSE.md
        ├── README.md
        ├── config/
        │   └── your-plugin.php
        ├── resources/
        │   ├── css/
        │   ├── js/
        │   └── views/
        ├── routes/
        │   └── web.php (optional)
        ├── src/
        │   ├── Commands/ (console commands)
        │   ├── Facades/ (optional)
        │   ├── Forms/ (form components)
        │   │   └── Components/
        │   ├── Tables/ (table components)
        │   │   ├── Actions/
        │   │   ├── Columns/
        │   │   └── Filters/
        │   ├── Infolists/ (infolist components)
        │   │   └── Components/
        │   ├── Pages/ (plugin pages)
        │   ├── Widgets/ (dashboard widgets)
        │   ├── YourPluginServiceProvider.php
        │   └── Providers/
        └── tests/
        """,
        "service_provider_example": """
        <?php
        
        namespace YourNamespace\\YourPlugin;
        
        use Illuminate\\Support\\ServiceProvider;
        use Filament\\Support\\Assets\\AlpineComponent;
        use Filament\\Support\\Assets\\Asset;
        use Filament\\Support\\Assets\\Css;
        use Filament\\Support\\Assets\\Js;
        use Filament\\Support\\Facades\\FilamentAsset;
        use Filament\\Support\\Facades\\FilamentIcon;
        use Spatie\\LaravelPackageTools\\Commands\\InstallCommand;
        use Spatie\\LaravelPackageTools\\Package;
        use Spatie\\LaravelPackageTools\\PackageServiceProvider;
        
        class YourPluginServiceProvider extends PackageServiceProvider
        {
            public static string $name = 'your-plugin';
            
            public function configurePackage(Package $package): void
            {
                $package
                    ->name(static::$name)
                    ->hasConfigFile()
                    ->hasViews()
                    ->hasTranslations()
                    ->hasCommand(YourCommand::class)
                    ->hasInstallCommand(function (InstallCommand $command) {
                        $command
                            ->publishConfigFile()
                            ->publishMigrations()
                            ->askToRunMigrations()
                            ->askToStarRepoOnGitHub('you/your-plugin');
                    });
            }
            
            public function packageRegistered(): void
            {
                // Register your services
            }
            
            public function packageBooted(): void
            {
                // Register assets
                FilamentAsset::register([
                    Css::make('your-plugin-styles', __DIR__ . '/../resources/dist/your-plugin.css'),
                    Js::make('your-plugin-scripts', __DIR__ . '/../resources/dist/your-plugin.js'),
                ], package: 'you/your-plugin');
                
                // Register icons
                FilamentIcon::register([
                    'your-plugin' => __DIR__ . '/../resources/icons/custom-icon.svg',
                ]);
                
                // Register plugin with Filament
                $this->app->booted(function () {
                    if (class_exists('\\\\Filament\\Panel')) {
                        $panels = app(\\Filament\\Panel::class);
                        
                        foreach ($panels as $panel) {
                            // Register plugin with each panel
                            $panel->plugin(new YourPluginPanelProvider());
                        }
                    }
                });
            }
        }
        """
    },
    "Custom Form Field": {
        "description": "Steps to create a custom form field component",
        "example": """
        <?php
        
        namespace YourNamespace\\YourPlugin\\Forms\\Components;
        
        use Filament\\Forms\\Components\\Field;
        
        class CustomField extends Field
        {
            protected string $view = 'your-plugin::forms.components.custom-field';
            
            // Properties
            protected string $customProperty = '';
            
            // Methods
            public function customProperty(string $value): static
            {
                $this->customProperty = $value;
                
                return $this;
            }
            
            public function getCustomProperty(): string
            {
                return $this->customProperty;
            }
        }
        """
    },
    "Panel Plugin": {
        "description": "Creating a plugin that integrates with Filament panels",
        "example": """
        <?php
        
        namespace YourNamespace\\YourPlugin;
        
        use Filament\\Contracts\\Plugin;
        use Filament\\Panel;
        use Filament\\Support\\Concerns\\EvaluatesClosures;
        
        class YourPluginPanelProvider implements Plugin
        {
            use EvaluatesClosures;
            
            public function getId(): string
            {
                return 'your-plugin';
            }
            
            public function register(Panel $panel): void
            {
                // Register plugin resources
                $panel
                    ->resources([
                        Resources\\YourResource::class,
                    ])
                    ->pages([
                        Pages\\YourPage::class,
                    ])
                    ->widgets([
                        Widgets\\YourWidget::class,
                    ]);
            }
            
            public function boot(Panel $panel): void
            {
                // Additional setup after all plugins are registered
            }
        }
        """
    },
    "Publishing Your Plugin": {
        "description": "Steps to publish a Filament plugin to Packagist",
        "steps": [
            "Prepare your package with a complete composer.json file",
            "Ensure proper documentation in README.md",
            "Set up tests and ensure they pass",
            "Create a GitHub repository for your plugin",
            "Push your code to GitHub",
            "Create a release/tag",
            "Register your package on Packagist.org",
            "Maintain and update your plugin"
        ],
        "composer_example": """
        {
            "name": "you/your-plugin",
            "description": "A custom plugin for FilamentPHP",
            "keywords": [
                "filament",
                "laravel",
                "your-plugin"
            ],
            "homepage": "https://github.com/you/your-plugin",
            "license": "MIT",
            "authors": [
                {
                    "name": "Your Name",
                    "email": "your.email@example.com",
                    "role": "Developer"
                }
            ],
            "require": {
                "php": "^8.1",
                "filament/filament": "^3.0",
                "illuminate/contracts": "^10.0",
                "spatie/laravel-package-tools": "^1.15.0"
            },
            "require-dev": {
                "laravel/pint": "^1.0",
                "nunomaduro/collision": "^7.9",
                "nunomaduro/larastan": "^2.0.1",
                "orchestra/testbench": "^8.0",
                "pestphp/pest": "^2.0",
                "pestphp/pest-plugin-laravel": "^2.0",
                "phpstan/extension-installer": "^1.1",
                "phpstan/phpstan-deprecation-rules": "^1.0"
            },
            "autoload": {
                "psr-4": {
                    "YourNamespace\\\\YourPlugin\\\\": "src"
                }
            },
            "autoload-dev": {
                "psr-4": {
                    "YourNamespace\\\\YourPlugin\\\\Tests\\\\": "tests"
                }
            },
            "scripts": {
                "post-autoload-dump": "@php ./vendor/bin/testbench package:discover --ansi",
                "analyse": "vendor/bin/phpstan analyse",
                "test": "vendor/bin/pest",
                "test-coverage": "vendor/bin/pest --coverage",
                "format": "vendor/bin/pint"
            },
            "config": {
                "sort-packages": true,
                "allow-plugins": {
                    "pestphp/pest-plugin": true,
                    "phpstan/extension-installer": true
                }
            },
            "extra": {
                "laravel": {
                    "providers": [
                        "YourNamespace\\\\YourPlugin\\\\YourPluginServiceProvider"
                    ]
                }
            },
            "minimum-stability": "dev",
            "prefer-stable": true
        }
        """
    }
}

# Plugin Integration
PLUGIN_INTEGRATION = {
    "Installation Best Practices": {
        "description": "Best practices for integrating plugins in FilamentPHP projects",
        "steps": [
            "Read the plugin documentation thoroughly before installation",
            "Install plugins one at a time to isolate any issues",
            "Check compatibility with your Filament version",
            "Always publish and review config files before customization",
            "Run migrations in development first before production",
            "Test plugin functionality in a development environment",
            "Consider impact on existing features before integration"
        ]
    },
    "Plugin Configuration": {
        "description": "Common configuration patterns for Filament plugins",
        "example": """
        // In config/filament.php
        
        'plugins' => [
            // Register and configure plugins
            App\\Filament\\Plugins\\CustomPlugin::make([
                'option1' => 'value1',
                'option2' => 'value2',
            ]),
            
            // Some plugins have their own config files
            // e.g., config/filament-shield.php
        ],
        
        // Common plugin configurations
        'middleware' => [
            'auth' => [
                // Add plugin middleware
                \\BezhanSalleh\\FilamentShield\\Http\\Middleware\\EnsureHasPermission::class,
            ],
        ],
        
        // Panel configuration
        'panels' => [
            'app' => [
                'plugin_overrides' => [
                    // Override plugin settings for specific panel
                ],
            ],
        ],
        """
    },
    "Extending Existing Plugins": {
        "description": "How to extend or customize existing plugins",
        "example": """
        <?php
        
        namespace App\\Filament\\Plugins;
        
        use Vendor\\Plugin\\ExistingPlugin;
        
        class CustomizedPlugin extends ExistingPlugin
        {
            // Override methods to customize behavior
            public function getId(): string
            {
                return 'customized-' . parent::getId();
            }
            
            public function register(Panel $panel): void
            {
                // Custom registration logic
                parent::register($panel);
                
                // Additional registration
                $panel->widgets([
                    YourWidget::class,
                ]);
            }
            
            // Extend with new features
            public function withCustomFeature(): static
            {
                // Add custom functionality
                return $this;
            }
        }
        
        // Register customized plugin in config/filament.php
        'plugins' => [
            App\\Filament\\Plugins\\CustomizedPlugin::make(),
        ],
        """
    },
    "Plugin Conflicts": {
        "description": "Common plugin conflicts and how to resolve them",
        "issues": [
            {
                "problem": "Multiple plugins registering resources with the same slugs",
                "solution": "Override navigation group or label to differentiate resources"
            },
            {
                "problem": "Asset conflicts (JS, CSS)",
                "solution": "Use namespaced selectors and check for global variables"
            },
            {
                "problem": "Incompatible plugin versions",
                "solution": "Check GitHub issues and ensure all plugins support your Filament version"
            },
            {
                "problem": "Plugins competing for the same hook/position",
                "solution": "Use plugin priority settings or customize plugin loading order"
            }
        ],
        "example": """
        // Resolving navigation conflicts
        public static function getNavigationGroup(): string
        {
            return 'Custom Plugin Section';
        }
        
        // Resolving asset conflicts by namespacing
        FilamentAsset::register([
            Css::make('your-plugin-styles', __DIR__ . '/../resources/dist/your-plugin.css')
                ->loadedOnRequest()
                ->setAttributes([
                    'data-plugin' => 'your-plugin', // Add data attribute
                ]),
        ]);
        
        // JS namespace example
        (function() {
            // Your plugin code in a closure to avoid global namespace pollution
            window.YourPluginNamespace = window.YourPluginNamespace || {};
            // Plugin code here
        })();
        """
    }
}

# Function to get all the plugins and extensions knowledge
def get_plugins_and_extensions_knowledge() -> Dict[str, Any]:
    """
    Returns the comprehensive FilamentPHP plugins and extensions knowledge base
    """
    return {
        "overview": PLUGINS_OVERVIEW,
        "official_plugins": OFFICIAL_PLUGINS,
        "community_plugins": COMMUNITY_PLUGINS,
        "custom_plugin_development": CUSTOM_PLUGIN_DEVELOPMENT,
        "plugin_integration": PLUGIN_INTEGRATION
    } 