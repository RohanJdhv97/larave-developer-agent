"""
FilamentPHP Core Concepts Knowledge Base

This module contains comprehensive knowledge about FilamentPHP core concepts,
including overview, key features, and architectural patterns.
"""

from typing import Dict, List, Any

# FilamentPHP Overview
FILAMENT_OVERVIEW = """
FilamentPHP is a collection of Laravel packages that helps developers quickly build TALL stack
(Tailwind CSS, Alpine.js, Laravel, and Livewire) applications. It provides a powerful admin panel,
form builder, table builder, and other tools to rapidly build beautiful applications.

Key aspects of FilamentPHP:
- Built on the TALL stack (Tailwind, Alpine.js, Laravel, Livewire)
- Modular architecture with separate packages that can be used independently
- Extensive component library for building admin interfaces
- Powerful form and table builders with advanced customization options
- Dark mode support out of the box
- Responsive design for all screen sizes
- Extensible plugin system
- Role and permission management
- Customizable themes
"""

# Installation and Setup
INSTALLATION_GUIDE = """
# FilamentPHP Installation Guide

## Requirements
- PHP 8.1+
- Laravel 9.0+
- Livewire 2.0+

## Installing the Admin Panel

```bash
# Create a new Laravel project if needed
composer create-project laravel/laravel example-app
cd example-app

# Install Filament
composer require filament/filament:"^3.0-stable" -W

# Create the first admin user
php artisan filament:user

# Run the migrations
php artisan migrate

# Publish the configuration
php artisan vendor:publish --tag=filament-config
```

## Configuring the Admin Panel

The main configuration file is located at `config/filament.php` and allows you to customize:
- Path to the admin panel (default: 'admin')
- Navigation structure and branding
- Authentication guards
- Middleware and layout options
- Default theme and dark mode settings
"""

# Core Components of FilamentPHP
CORE_COMPONENTS = {
    "Panels": {
        "description": "Panels are the entry points to your Filament applications. The admin panel is the most common, but you can create custom panels.",
        "key_features": [
            "Custom dashboard widgets",
            "Navigation management",
            "User authentication and registration",
            "Theme customization",
            "Role-based access control"
        ],
        "example": """
        // Register a new panel in a service provider
        public function boot(): void
        {
            Filament::registerPanel(
                Panel::make()
                    ->id('admin')
                    ->path('admin')
                    ->colors([
                        'primary' => Color::Amber,
                    ])
                    ->discoverResources(in: app_path('Filament/Resources'), for: 'App\\Filament\\Resources')
                    ->discoverPages(in: app_path('Filament/Pages'), for: 'App\\Filament\\Pages')
                    ->pages([
                        Dashboard::class,
                    ])
                    ->discoverWidgets(in: app_path('Filament/Widgets'), for: 'App\\Filament\\Widgets')
                    ->widgets([
                        AccountWidget::class,
                        FilamentInfoWidget::class,
                    ])
                    ->middleware([
                        EncryptCookies::class,
                        AddQueuedCookiesToResponse::class,
                        StartSession::class,
                        AuthenticateSession::class,
                        ShareErrorsFromSession::class,
                        VerifyCsrfToken::class,
                        SubstituteBindings::class,
                        DisableBladeIconComponents::class,
                        DispatchServingFilamentEvent::class,
                    ])
                    ->authMiddleware([
                        Authenticate::class,
                    ])
            );
        }
        """
    },
    "Resources": {
        "description": "Resources represent your Eloquent models in the admin panel, with built-in CRUD operations.",
        "key_features": [
            "Automatic CRUD interface for Eloquent models",
            "Custom form and table fields",
            "Built-in validation",
            "Custom actions and bulk actions",
            "Automatic breadcrumbs and navigation",
            "Relation managers for managing related models"
        ],
        "example": """
        // Example Resource for a Product model
        use App\\Models\\Product;
        use Filament\\Forms;
        use Filament\\Resources\\Resource;
        use Filament\\Tables;

        class ProductResource extends Resource
        {
            protected static ?string $model = Product::class;
            
            protected static ?string $navigationIcon = 'heroicon-o-rectangle-stack';
            
            public static function form(Forms\\Form $form): Forms\\Form
            {
                return $form
                    ->schema([
                        Forms\\Components\\TextInput::make('name')
                            ->required()
                            ->maxLength(255),
                        Forms\\Components\\TextInput::make('price')
                            ->required()
                            ->numeric()
                            ->prefix('$'),
                        Forms\\Components\\Textarea::make('description')
                            ->columnSpanFull(),
                    ]);
            }
            
            public static function table(Tables\\Table $table): Tables\\Table
            {
                return $table
                    ->columns([
                        Tables\\Columns\\TextColumn::make('name')
                            ->searchable(),
                        Tables\\Columns\\TextColumn::make('price')
                            ->money('usd')
                            ->sortable(),
                        Tables\\Columns\\TextColumn::make('created_at')
                            ->dateTime()
                            ->sortable()
                            ->toggleable(isToggledHiddenByDefault: true),
                    ])
                    ->filters([
                        //
                    ])
                    ->actions([
                        Tables\\Actions\\EditAction::make(),
                    ])
                    ->bulkActions([
                        Tables\\Actions\\DeleteBulkAction::make(),
                    ]);
            }
        }
        """
    },
    "Pages": {
        "description": "Custom admin pages that are not tied to a specific resource, like dashboards or settings pages.",
        "key_features": [
            "Custom layouts and forms",
            "Integration with Livewire for dynamic pages",
            "Custom actions and modals",
            "Widget support"
        ],
        "example": """
        // Example custom settings page
        use Filament\\Pages\\Page;
        use Filament\\Forms\\Components\\TextInput;
        use Filament\\Forms\\Form;
        use Filament\\Actions\\Action;

        class Settings extends Page
        {
            protected static ?string $navigationIcon = 'heroicon-o-cog';
            
            protected static string $view = 'filament.pages.settings';
            
            public ?array $data = [];
            
            public function mount(): void
            {
                $this->form->fill([
                    'site_name' => config('app.name'),
                    'site_description' => config('app.description'),
                ]);
            }
            
            public function form(Form $form): Form
            {
                return $form
                    ->schema([
                        TextInput::make('site_name')
                            ->required(),
                        TextInput::make('site_description'),
                    ]);
            }
            
            protected function getHeaderActions(): array
            {
                return [
                    Action::make('save')
                        ->action(function () {
                            // Save settings logic
                            $this->form->getState();
                        }),
                ];
            }
        }
        """
    },
    "Widgets": {
        "description": "Dashboard widgets to display statistics, charts, or other data visualizations.",
        "key_features": [
            "Stats widgets",
            "Chart widgets",
            "Table widgets",
            "Custom widget types",
            "Dynamic data loading"
        ],
        "example": """
        // Example stats widget
        use Filament\\Widgets\\StatsOverviewWidget as BaseWidget;
        use Filament\\Widgets\\StatsOverviewWidget\\Stat;
        use App\\Models\\Order;
        use App\\Models\\Customer;
        use App\\Models\\Product;

        class StatsOverview extends BaseWidget
        {
            protected function getStats(): array
            {
                return [
                    Stat::make('Total Customers', Customer::count())
                        ->description('Increased by 20%')
                        ->descriptionIcon('heroicon-m-arrow-trending-up')
                        ->chart([7, 2, 10, 3, 15, 4, 17])
                        ->color('success'),
                    Stat::make('Total Orders', Order::count())
                        ->description('32% success rate')
                        ->descriptionIcon('heroicon-m-arrow-trending-down')
                        ->chart([17, 16, 14, 15, 14, 13, 12])
                        ->color('danger'),
                    Stat::make('Average price', '$ ' . number_format(Product::avg('price'), 2))
                        ->description('3% increase')
                        ->descriptionIcon('heroicon-m-arrow-trending-up')
                        ->chart([15, 8, 12, 12, 13, 13, 15])
                        ->color('success'),
                ];
            }
        }
        """
    }
}

# Best Practices for FilamentPHP Development
BEST_PRACTICES = {
    "Code Organization": [
        "Keep resource classes in the app/Filament/Resources directory",
        "Organize relation managers within the resource's RelationManagers directory",
        "Place custom form fields and table columns in dedicated app/Filament/Forms and app/Filament/Tables directories",
        "Use form and table concerns for reusable schemas",
        "Create custom field and column classes for complex, reusable components"
    ],
    "Performance": [
        "Use eager loading for relation managers to avoid N+1 queries",
        "Cache expensive computation results with Laravel's caching system",
        "Implement pagination for large tables",
        "Use lazy loading for images and heavy components",
        "Consider implementing custom database indexing for frequently filtered columns"
    ],
    "Security": [
        "Implement proper authorization policies for resources",
        "Use form validation for all user inputs",
        "Implement rate limiting for form submissions",
        "Consider using custom form field sanitization for certain inputs",
        "Use Filament's built-in authentication and permission system"
    ],
    "UX Best Practices": [
        "Provide clear action labels and confirmations for destructive actions",
        "Use consistent icons throughout your application",
        "Implement proper form field validation messages",
        "Group related form fields into sections or tabs",
        "Use appropriate field types for different kinds of data",
        "Consider implementing progressive loading for large forms"
    ]
}

# Function to get the knowledge base
def get_filament_core_knowledge() -> Dict[str, Any]:
    """
    Returns the comprehensive FilamentPHP core knowledge base
    """
    return {
        "overview": FILAMENT_OVERVIEW,
        "installation": INSTALLATION_GUIDE,
        "core_components": CORE_COMPONENTS,
        "best_practices": BEST_PRACTICES
    } 