"""
FilamentPHP Advanced Features Knowledge Base

This module contains comprehensive knowledge about FilamentPHP advanced features,
including Infolists, Lifecycle hooks, input/output modification, and multitenancy.
"""

from typing import Dict, List, Any

# Infolists Overview
INFOLISTS_OVERVIEW = """
FilamentPHP Infolists are powerful components used to display detailed information about a record
in a structured, readable format. Unlike forms which are used for input, Infolists are specifically
designed for output and presentation of data.

Key features of Infolists:
- Rich collection of entry types for displaying various data formats
- Customizable layouts with responsive design
- Conditional display logic
- Integration with relationships and computed attributes
- Dark mode support
- Action support for interactive elements
- Icon and badge support
- Grid and tab layout options
- Custom entry types
"""

# Infolist Entries
INFOLIST_ENTRIES = {
    "Text Entries": {
        "TextEntry": {
            "description": "Display text content with formatting options",
            "common_options": [
                "badge()", "color()", "icon()", "markdown()",
                "limit()", "listWithLineBreaks()", "money()", "date()"
            ],
            "example": """
            TextEntry::make('title')
                ->label('Article Title')
                ->weight('bold')
                ->copyable()
                ->icon('heroicon-o-document-text')
                ->color(fn ($record) => $record->is_featured ? 'success' : 'gray')
            """
        },
        "MarkdownEntry": {
            "description": "Render markdown content with proper formatting",
            "common_options": [
                "prose()", "extraAttributes()"
            ],
            "example": """
            MarkdownEntry::make('content')
                ->label('Article Content')
                ->prose()  // Apply prose styling for better readability
                ->extraAttributes([
                    'class' => 'text-sm',
                ])
            """
        }
    },
    "Image and Media Entries": {
        "ImageEntry": {
            "description": "Display images with formatting options",
            "common_options": [
                "circular()", "visibility()", "height()", "width()",
                "extraImgAttributes()", "defaultImageUrl()"
            ],
            "example": """
            ImageEntry::make('avatar')
                ->label('User Avatar')
                ->circular()
                ->height(100)
                ->width(100)
                ->defaultImageUrl(asset('images/default-avatar.jpg'))
                ->extraImgAttributes([
                    'alt' => 'User profile image',
                ])
            """
        },
        "ColorEntry": {
            "description": "Display color values as a swatch",
            "common_options": [
                "copyable()", "tooltip()", "schema()"
            ],
            "example": """
            ColorEntry::make('brand_color')
                ->label('Brand Color')
                ->copyable()
                ->tooltip(fn ($state) => $state)
            """
        }
    },
    "Icon Entries": {
        "IconEntry": {
            "description": "Display icons based on record data",
            "common_options": [
                "color()", "size()", "boolean()", "stacked()",
                "extraAttributes()"
            ],
            "example": """
            IconEntry::make('status')
                ->label('Status')
                ->icon(fn (string $state): string => match ($state) {
                    'completed' => 'heroicon-o-check-circle',
                    'processing' => 'heroicon-o-clock',
                    'failed' => 'heroicon-o-x-circle',
                    default => 'heroicon-o-question-mark-circle',
                })
                ->color(fn (string $state): string => match ($state) {
                    'completed' => 'success',
                    'processing' => 'warning',
                    'failed' => 'danger',
                    default => 'gray',
                })
                ->size('lg')
            """
        },
        "Badge Entry": {
            "description": "Display data as a colored badge",
            "common_options": [
                "color()", "icon()", "size()", "tooltip()"
            ],
            "example": """
            BadgeEntry::make('status')
                ->label('Status')
                ->color(fn (string $state): string => match ($state) {
                    'published' => 'success',
                    'draft' => 'gray',
                    'scheduled' => 'warning',
                    default => 'gray',
                })
                ->icon(fn (string $state): string => match ($state) {
                    'published' => 'heroicon-o-check-circle',
                    'draft' => 'heroicon-o-pencil',
                    'scheduled' => 'heroicon-o-clock',
                    default => null,
                })
            """
        }
    },
    "Relationship Entries": {
        "TextEntry for Relationships": {
            "description": "Display data from related models",
            "common_options": [
                "listWithLineBreaks()", "bulleted()", "limitList()",
                "expandableLimitedList()"
            ],
            "example": """
            // Display a single related model's attribute
            TextEntry::make('author.name')
                ->label('Author')
                ->badge()
                ->color('primary')
                
            // Display multiple related models
            TextEntry::make('categories.name')
                ->label('Categories')
                ->listWithLineBreaks()
                ->bulleted()
                ->limitList(3)
                ->expandableLimitedList()
            """
        },
        "RepeatableEntry": {
            "description": "Display repeatable entries for has-many relationships",
            "common_options": [
                "schema()", "collapsible()", "contained()",
                "label()", "grid()"
            ],
            "example": """
            RepeatableEntry::make('comments')
                ->schema([
                    TextEntry::make('author.name')
                        ->label('Author'),
                    TextEntry::make('content')
                        ->label('Comment')
                        ->markdown(),
                    TextEntry::make('created_at')
                        ->label('Posted')
                        ->date('F j, Y H:i'),
                ])
                ->grid(2)
                ->label('Recent Comments')
                ->collapsible()
            """
        }
    },
    "Action Entries": {
        "ActionEntry": {
            "description": "Display clickable actions within an infolist",
            "common_options": [
                "action()", "url()", "visible()", "hidden()",
                "modalContent()", "form()", "color()", "extraAttributes()"
            ],
            "example": """
            ActionEntry::make('view')
                ->label('View on Website')
                ->icon('heroicon-o-arrow-top-right-on-square')
                ->url(fn ($record): string => route('posts.show', $record))
                ->openUrlInNewTab()
                ->button()
                ->color('primary')
                ->size('sm')
                ->visible(fn ($record) => $record->is_published)
            """
        }
    }
}

# Infolist Layouts
INFOLIST_LAYOUTS = {
    "Grid Layout": {
        "description": "Responsive grid layout for entries",
        "example": """
        Infolist::make()
            ->schema([
                Grid::make(2)
                    ->schema([
                        TextEntry::make('title')
                            ->columnSpan(1),
                        TextEntry::make('slug')
                            ->columnSpan(1),
                        TextEntry::make('content')
                            ->columnSpanFull(),
                    ]),
            ])
        """
    },
    "Section": {
        "description": "Group related entries with a heading",
        "example": """
        Infolist::make()
            ->schema([
                Section::make('Post Information')
                    ->description('Basic information about the post')
                    ->schema([
                        TextEntry::make('title'),
                        TextEntry::make('slug'),
                        TextEntry::make('created_at')
                            ->dateTime(),
                    ]),
                Section::make('Content')
                    ->schema([
                        TextEntry::make('content')
                            ->markdown()
                            ->columnSpanFull(),
                    ])
                    ->collapsible(),
            ])
        """
    },
    "Tabs": {
        "description": "Organize entries into tabbed sections",
        "example": """
        Infolist::make()
            ->schema([
                Tabs::make('Content')
                    ->tabs([
                        Tab::make('Basic Information')
                            ->icon('heroicon-o-information-circle')
                            ->schema([
                                TextEntry::make('title'),
                                TextEntry::make('slug'),
                                TextEntry::make('status'),
                            ]),
                        Tab::make('Content')
                            ->icon('heroicon-o-document-text')
                            ->schema([
                                TextEntry::make('content')
                                    ->markdown()
                                    ->columnSpanFull(),
                            ]),
                        Tab::make('SEO')
                            ->icon('heroicon-o-magnifying-glass')
                            ->schema([
                                TextEntry::make('meta_title'),
                                TextEntry::make('meta_description'),
                                TextEntry::make('keywords'),
                            ]),
                    ]),
            ])
        """
    },
    "Card": {
        "description": "Display entries in a card container",
        "example": """
        Infolist::make()
            ->schema([
                Card::make()
                    ->schema([
                        TextEntry::make('title'),
                        TextEntry::make('author.name'),
                        TextEntry::make('published_at')
                            ->dateTime(),
                    ])
                    ->columns(3),
            ])
        """
    }
}

# Lifecycle Hooks
LIFECYCLE_HOOKS = {
    "Form Hooks": {
        "description": "Lifecycle hooks for form operations",
        "hooks": {
            "beforeFill": "Called before a form is filled with data",
            "afterFill": "Called after a form is filled with data",
            "beforeValidate": "Called before form data is validated",
            "afterValidate": "Called after form data is validated",
            "beforeSave": "Called before the form data is saved to the database",
            "afterSave": "Called after the form data is saved to the database",
            "beforeCreate": "Called before a record is created",
            "afterCreate": "Called after a record is created",
            "beforeEdit": "Called before a record is edited",
            "afterEdit": "Called after a record is edited",
        },
        "example": """
        protected function beforeCreate(): void
        {
            // Add the current user as the author
            $this->data['user_id'] = auth()->id();
        }
        
        protected function afterCreate(): void
        {
            // Generate a slug based on the title
            $this->record->update([
                'slug' => Str::slug($this->record->title),
            ]);
            
            // Log the creation
            Activity::create([
                'description' => "Created post: {$this->record->title}",
                'user_id' => auth()->id(),
            ]);
        }
        
        protected function beforeSave(): void
        {
            // Add metadata
            if ($this->record) {
                $this->data['updated_by'] = auth()->id();
            }
            
            // Format content if needed
            if (isset($this->data['content'])) {
                $this->data['content'] = clean($this->data['content']);
            }
        }
        
        protected function afterSave(): void
        {
            // Clear cache
            Cache::forget('posts');
            
            // Send notification if published
            if (isset($this->data['status']) && $this->data['status'] === 'published') {
                if ($this->record->wasChanged('status') || $this->record->wasRecentlyCreated) {
                    PublishNotification::dispatch($this->record);
                }
            }
        }
        """
    },
    "Table Action Hooks": {
        "description": "Lifecycle hooks for table actions",
        "hooks": {
            "beforeAction": "Called before an action is executed",
            "afterAction": "Called after an action is executed",
            "beforeFormFilled": "Called before an action form is filled",
            "afterFormFilled": "Called after an action form is filled",
            "beforeFormValidated": "Called before an action form is validated",
            "afterFormValidated": "Called after an action form is validated",
        },
        "example": """
        Actions::make([
            Action::make('approve')
                ->action(function (Model $record, array $data): void {
                    $record->update(['status' => 'approved']);
                })
                ->beforeAction(function () {
                    // Check permissions
                    if (! auth()->user()->can('approve_posts')) {
                        Notification::make()
                            ->title('Permission denied')
                            ->danger()
                            ->send();
                            
                        $this->halt();
                    }
                })
                ->afterAction(function (Model $record) {
                    // Send notification
                    Notification::make()
                        ->title('Post approved')
                        ->success()
                        ->send();
                        
                    // Log activity
                    Activity::create([
                        'description' => "Approved post: {$record->title}",
                        'user_id' => auth()->id(),
                    ]);
                }),
        ])
        """
    },
    "Resource Hooks": {
        "description": "Lifecycle hooks for resource pages",
        "hooks": {
            "beforeCreate": "Called before creating a record from a resource",
            "afterCreate": "Called after creating a record from a resource",
            "beforeEdit": "Called before editing a record from a resource",
            "afterEdit": "Called after editing a record from a resource",
            "beforeDelete": "Called before deleting a record from a resource",
            "afterDelete": "Called after deleting a record from a resource",
        },
        "example": """
        public static function afterCreate(Post $record): void
        {
            // Send notification to admins
            User::whereHas('roles', fn ($query) => $query->where('name', 'admin'))
                ->each(function ($admin) use ($record) {
                    $admin->notify(new PostCreatedNotification($record));
                });
                
            // Create default categories if none selected
            if ($record->categories()->count() === 0) {
                $record->categories()->attach(Category::where('slug', 'uncategorized')->first()->id);
            }
        }
        
        public static function beforeDelete(Post $record): void
        {
            // Check if post has comments
            if ($record->comments()->count() > 0) {
                Notification::make()
                    ->title('Cannot delete post with comments')
                    ->body('This post has comments and cannot be deleted.')
                    ->danger()
                    ->persistent()
                    ->send();
                    
                // Prevent deletion
                static::$isDeleting = false;
                
                // Redirect
                return redirect()->back();
            }
            
            // Archive content instead of permanently deleting
            $record->update([
                'status' => 'archived',
                'archived_at' => now(),
                'archived_by' => auth()->id(),
            ]);
        }
        """
    }
}

# Input/Output Modification
INPUT_OUTPUT_MODIFICATION = {
    "Form Data Modification": {
        "description": "Manipulate form data before and after processing",
        "methods": {
            "mutateFormDataBeforeFill": "Modify data before it fills a form",
            "mutateFormDataBeforeSave": "Modify data before it's saved to the database",
            "afterStateUpdated": "Perform actions when a specific field's state changes",
            "dehydrateFormData": "Transform data before it's saved to the database",
            "hydrateFormData": "Transform data after it's loaded from the database",
        },
        "example": """
        protected function mutateFormDataBeforeFill(array $data): array
        {
            // Convert timestamps to local timezone
            if (isset($data['published_at'])) {
                $data['published_at'] = Carbon::parse($data['published_at'])
                    ->setTimezone(auth()->user()->timezone);
            }
            
            // Decrypt sensitive data
            if (isset($data['api_key'])) {
                $data['api_key'] = Crypt::decrypt($data['api_key']);
            }
            
            return $data;
        }
        
        protected function mutateFormDataBeforeSave(array $data): array
        {
            // Handle password fields
            if (isset($data['password']) && blank($data['password'])) {
                unset($data['password']);
            }
            
            // Convert back to UTC
            if (isset($data['published_at'])) {
                $data['published_at'] = Carbon::parse($data['published_at'], auth()->user()->timezone)
                    ->setTimezone('UTC');
            }
            
            // Ensure slugs are unique
            if (isset($data['slug'])) {
                $slug = Str::slug($data['slug'] ?: $data['title']);
                $count = 0;
                
                while (static::getModel()::where('slug', $slug)
                    ->where('id', '!=', $this->record?->id ?: null)
                    ->exists()) {
                    $slug = Str::slug($data['slug'] ?: $data['title']) . '-' . ++$count;
                }
                
                $data['slug'] = $slug;
            }
            
            return $data;
        }
        """
    },
    "Field State Updates": {
        "description": "Handle field state changes",
        "example": """
        public static function form(Form $form): Form
        {
            return $form
                ->schema([
                    Select::make('type')
                        ->options([
                            'standard' => 'Standard',
                            'premium' => 'Premium',
                            'enterprise' => 'Enterprise',
                        ])
                        ->reactive() // Mark as reactive
                        ->afterStateUpdated(function ($state, callable $set) {
                            if ($state === 'premium') {
                                $set('price', 99.99);
                                $set('features', ['Feature 1', 'Feature 2', 'Feature 3']);
                            } elseif ($state === 'enterprise') {
                                $set('price', 199.99);
                                $set('features', ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4', 'Feature 5']);
                                $set('has_support', true);
                            } else {
                                $set('price', 49.99);
                                $set('features', ['Feature 1']);
                                $set('has_support', false);
                            }
                        }),
                    TextInput::make('price')
                        ->numeric()
                        ->prefix('$')
                        ->disabled(), // Disable direct editing
                    TagsInput::make('features')
                        ->disabled(), // Disable direct editing
                    Toggle::make('has_support')
                        ->label('Includes Support')
                        ->disabled(), // Disable direct editing
                ]);
        }
        """
    },
    "Custom State Transformations": {
        "description": "Custom transformations for field state",
        "example": """
        public static function form(Form $form): Form
        {
            return $form
                ->schema([
                    TextInput::make('price')
                        ->numeric()
                        ->prefix('$')
                        ->dehydrateStateUsing(fn ($state) => $state * 100) // Convert to cents for storage
                        ->hydrateStateUsing(fn ($state) => $state / 100) // Convert back to dollars for display
                        ->formatStateUsing(fn ($state) => number_format($state, 2)), // Format for display
                        
                    KeyValue::make('meta')
                        ->dehydrateStateUsing(fn ($state) => json_encode($state)) // Convert to JSON
                        ->hydrateStateUsing(fn ($state) => is_string($state) ? json_decode($state, true) : $state), // Parse JSON
                ])
                ->columns(1);
        }
        """
    },
    "Complex State Handling": {
        "description": "Handle complex state transformations",
        "example": """
        public static function form(Form $form): Form
        {
            return $form
                ->schema([
                    Select::make('roles')
                        ->relationship('roles', 'name')
                        ->multiple()
                        ->preload()
                        ->dehydrated(false) // Don't save directly
                        ->afterStateHydrated(function (Select $component, $state, $record) {
                            // Set the initial state from the relationship
                            $component->state(
                                $record ? $record->roles->pluck('id')->toArray() : []
                            );
                        })
                        ->afterStateUpdated(function ($state, $record) use ($form) {
                            // When roles change, update the permissions field
                            $permissions = Permission::whereHas('roles', function ($query) use ($state) {
                                $query->whereIn('id', $state ?: []);
                            })->pluck('id')->toArray();
                            
                            $form->fill(['permissions' => $permissions]);
                        }),
                        
                    CheckboxList::make('permissions')
                        ->relationship('permissions', 'name')
                        ->searchable()
                        ->bulkToggleable()
                        ->dehydrated(false), // Don't save directly
                ])
                ->saveRelationships(false) // Handle relationships manually
                ->statePath('data')
                ->afterSave(function ($record, array $data) {
                    // Sync the relationships manually
                    if (isset($data['roles'])) {
                        $record->roles()->sync($data['roles']);
                    }
                    
                    if (isset($data['permissions'])) {
                        $record->permissions()->sync($data['permissions']);
                    }
                });
        }
        """
    }
}

# Multitenancy
MULTITENANCY = {
    "Basic Concepts": {
        "description": "Fundamental concepts of multitenancy in Filament",
        "tenancy_modes": [
            "Single Database" - "Multiple tenants share one database with a tenant_id column",
            "Multiple Database" - "Each tenant has their own separate database",
            "Multiple Domain" - "Each tenant has their own domain name"
        ],
        "overview": """
        FilamentPHP provides first-class support for multitenancy through a simple yet powerful API.
        It allows you to scope all database queries to the current tenant automatically and customize
        the behavior per tenant. 
        
        The most common multitenancy model in Filament involves:
        1. Implementing a "tenant" model (like Team, Organization, Company)
        2. Configuring panel registration with tenant awareness
        3. Setting up tenant-specific customization (colors, logos, etc.)
        4. Implementing middleware to determine the current tenant
        """
    },
    "Panel Configuration": {
        "description": "Configure a Filament panel for multitenancy",
        "example": """
        use App\\Models\\Team;
        use Filament\\Http\\Middleware\\Authenticate;
        use Filament\\Panel;
        
        public function boot(): void
        {
            Filament::registerPanel(
                Panel::make()
                    ->id('tenant')
                    ->path('app')
                    ->tenant(Team::class, function (Team $team) {
                        // Only authenticated users with access to this team can access the panel
                        if (! auth()->user()->belongsToTeam($team)) {
                            return false;
                        }
                        
                        return true;
                    })
                    ->tenantSlug(function (Team $team): string {
                        // How to identify the tenant in the URL path
                        return $team->slug;
                    })
                    ->tenantProfile(function (Team $team): array {
                        // Information about the tenant that can be used in navigation or context
                        return [
                            'name' => $team->name,
                            'description' => $team->description,
                            'url' => route('teams.show', ['team' => $team]),
                            'avatar' => $team->logo_url,
                        ];
                    })
                    ->colors([
                        'primary' => fn (Team $team) => $team->primary_color ?? 'rgb(var(--primary))',
                    ])
                    ->discoverResources(in: app_path('Filament/Resources'), for: 'App\\Filament\\Resources')
                    ->authMiddleware([
                        Authenticate::class,
                    ])
            );
        }
        """
    },
    "Tenant Middleware": {
        "description": "Handle tenant resolution in the middleware",
        "example": """
        namespace App\\Http\\Middleware;
        
        use Closure;
        use Illuminate\\Http\\Request;
        use App\\Models\\Team;
        
        class ResolveTenant
        {
            public function handle(Request $request, Closure $next)
            {
                $teamSlug = $request->route('tenant');
                
                if (! $teamSlug) {
                    return $next($request);
                }
                
                $team = Team::where('slug', $teamSlug)->first();
                
                if (! $team) {
                    abort(404);
                }
                
                // Check if the user has access to this team
                if (! $request->user() || ! $request->user()->belongsToTeam($team)) {
                    abort(403);
                }
                
                // Store the resolved tenant in the container for later use
                app()->instance('current-team', $team);
                
                // Set up the tenant context for the rest of the request
                tenancy()->initialize($team);
                
                return $next($request);
            }
        }
        """
    },
    "Tenant-Aware Resources": {
        "description": "Create resources that are scoped to tenants",
        "example": """
        namespace App\\Filament\\Resources;
        
        use App\\Filament\\Resources\\ProjectResource\\Pages;
        use App\\Models\\Project;
        use Filament\\Resources\\Resource;
        use Illuminate\\Database\\Eloquent\\Builder;
        
        class ProjectResource extends Resource
        {
            protected static ?string $model = Project::class;
            
            // Override the eloquent query to scope to the current tenant
            public static function getEloquentQuery(): Builder
            {
                return parent::getEloquentQuery()
                    ->whereBelongsTo(tenant());
            }
            
            public static function form(Form $form): Form
            {
                return $form
                    ->schema([
                        // Hide the team field as it will be set automatically
                        Hidden::make('team_id')
                            ->default(fn () => tenant()->id),
                            
                        TextInput::make('name')
                            ->required(),
                            
                        // Other fields...
                    ]);
            }
            
            // Rest of resource definition...
        }
        """
    },
    "Tenant Switching": {
        "description": "Allow users to switch between tenants",
        "example": """
        // In the navigation service provider
        use Filament\\Navigation\\MenuItem;
        
        class AppServiceProvider extends ServiceProvider
        {
            public function boot(): void
            {
                Filament::serving(function () {
                    // Add tenant switcher to user menu
                    Filament::registerUserMenuItems([
                        'tenant-switcher' => MenuItem::make()
                            ->label('Switch Team')
                            ->url(route('tenant-switcher'))
                            ->icon('heroicon-o-arrow-right-on-rectangle'),
                    ]);
                    
                    // Or add to the navigation as a menu item
                    Filament::registerNavigationItems([
                        NavigationItem::make('Switch Team')
                            ->url(route('tenant-switcher'))
                            ->icon('heroicon-o-switch-horizontal')
                            ->group('Settings')
                            ->sort(10),
                    ]);
                });
            }
        }
        
        // In a controller
        public function switcherPage()
        {
            $teams = auth()->user()->teams;
            
            return view('tenant-switcher', [
                'teams' => $teams,
                'currentTeam' => tenant(),
            ]);
        }
        
        public function switchTenant(Request $request, Team $team)
        {
            if (! $request->user()->belongsToTeam($team)) {
                abort(403);
            }
            
            // Set as current team
            $request->user()->switchTeam($team);
            
            // Redirect to the tenant dashboard
            return redirect()->route('filament.tenant.pages.dashboard', ['tenant' => $team->slug]);
        }
        """
    },
    "Global vs Tenant Resources": {
        "description": "Manage resources that are global vs tenant-specific",
        "example": """
        // Register resources differently for multi-tenant panel vs admin panel
        public function boot(): void
        {
            // Multi-tenant panel for team members
            Filament::registerPanel(
                Panel::make()
                    ->id('tenant')
                    ->path('app')
                    ->tenant(Team::class)
                    // Only discover tenant-specific resources
                    ->discoverResources(in: app_path('Filament/Tenant/Resources'), for: 'App\\Filament\\Tenant\\Resources')
                    // ... other configuration
            );
            
            // Admin panel for super admins
            Filament::registerPanel(
                Panel::make()
                    ->id('admin')
                    ->path('admin')
                    // Discover admin-specific resources (global, not tenant-scoped)
                    ->discoverResources(in: app_path('Filament/Admin/Resources'), for: 'App\\Filament\\Admin\\Resources')
                    // ... other configuration
            );
        }
        
        // Example of resource organization:
        // app/
        //   Filament/
        //     Tenant/
        //       Resources/  # Tenant-scoped resources
        //         ProjectResource.php
        //         TaskResource.php
        //     Admin/
        //       Resources/  # Global resources
        //         TeamResource.php  # Manages all teams
        //         UserResource.php  # Manages all users
        """
    }
}

# Function to get the advanced features knowledge
def get_advanced_features_knowledge() -> Dict[str, Any]:
    """
    Returns the comprehensive FilamentPHP advanced features knowledge base
    """
    return {
        "infolists": {
            "overview": INFOLISTS_OVERVIEW,
            "entries": INFOLIST_ENTRIES,
            "layouts": INFOLIST_LAYOUTS
        },
        "lifecycle_hooks": LIFECYCLE_HOOKS,
        "input_output_modification": INPUT_OUTPUT_MODIFICATION,
        "multitenancy": MULTITENANCY
    } 