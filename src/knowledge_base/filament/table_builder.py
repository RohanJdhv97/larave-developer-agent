"""
FilamentPHP Table Builder Knowledge Base

This module contains comprehensive knowledge about FilamentPHP table builder components,
including column types, filters, actions, and advanced usage patterns.
"""

from typing import Dict, List, Any

# Table Builder Overview
TABLE_BUILDER_OVERVIEW = """
The FilamentPHP Table Builder is a powerful system for creating dynamic, interactive tables
with advanced filtering, sorting, and action capabilities. It integrates seamlessly with 
Eloquent models and provides a rich set of components for displaying and manipulating data.

Key features of the Table Builder:
- Rich collection of column types for various data formats
- Advanced filtering system with custom filter forms
- Sortable and searchable columns
- Bulk actions for multiple record operations
- Row and cell actions with modals and forms
- Pagination with configurable options
- Responsive design for all screen sizes
- Sticky headers and columns
- Bulk selection with checkboxes
- Record reordering with drag and drop
- Customizable empty states and loading indicators
- Export capabilities (CSV, Excel, etc.)
"""

# Table Columns
TABLE_COLUMNS = {
    "Text Columns": {
        "TextColumn": {
            "description": "Standard column for displaying text or numeric data",
            "common_options": [
                "sortable()", "searchable()", "toggleable()", "copyable()",
                "wrap()", "limit()", "badge()", "color()", "formatStateUsing()"
            ],
            "example": """
            TextColumn::make('title')
                ->sortable()
                ->searchable()
                ->limit(50)
                ->tooltip(fn ($record) => $record->title)
                ->description(fn ($record) => $record->subtitle)
            """
        },
        "TextInputColumn": {
            "description": "Editable text column with inline editing capabilities",
            "common_options": [
                "sortable()", "searchable()", "rules()", "type()",
                "disabled()", "visible()", "afterStateUpdated()"
            ],
            "example": """
            TextInputColumn::make('name')
                ->sortable()
                ->searchable()
                ->rules(['required', 'max:255'])
                ->label('Full Name')
            """
        }
    },
    "Date and Time Columns": {
        "DateColumn": {
            "description": "Display dates in various formats",
            "common_options": [
                "sortable()", "searchable()", "toggleable()", "date()",
                "since()", "timezone()", "default()"
            ],
            "example": """
            DateColumn::make('published_at')
                ->label('Published')
                ->sortable()
                ->date('F j, Y')
                ->default(now())
            """
        },
        "DateTimeColumn": {
            "description": "Display dates with time information",
            "common_options": [
                "sortable()", "searchable()", "toggleable()", "dateTime()",
                "since()", "timezone()", "default()", "withoutTime()"
            ],
            "example": """
            DateTimeColumn::make('created_at')
                ->label('Created')
                ->sortable()
                ->dateTime('F j, Y H:i:s')
                ->timezone('UTC')
                ->since() // displays as "2 hours ago"
            """
        },
        "TimeColumn": {
            "description": "Display only time information",
            "common_options": [
                "sortable()", "searchable()", "toggleable()", "time()",
                "timezone()"
            ],
            "example": """
            TimeColumn::make('opening_time')
                ->sortable()
                ->time('H:i A')
                ->timezone('America/New_York')
            """
        }
    },
    "Special Format Columns": {
        "IconColumn": {
            "description": "Display icon based on the state of a record",
            "common_options": [
                "sortable()", "toggleable()", "boolean()", "options()",
                "size()", "color()"
            ],
            "example": """
            IconColumn::make('is_featured')
                ->label('Featured')
                ->boolean()
                ->trueIcon('heroicon-o-star')
                ->falseIcon('heroicon-o-x-mark')
                ->trueColor('warning')
                ->falseColor('danger')
            """
        },
        "ImageColumn": {
            "description": "Display images in the table",
            "common_options": [
                "toggleable()", "circular()", "height()", "width()",
                "disk()", "visibility()", "defaultImageUrl()"
            ],
            "example": """
            ImageColumn::make('avatar')
                ->label('Profile Picture')
                ->disk('public')
                ->circular()
                ->height(40)
                ->defaultImageUrl(asset('images/default-avatar.jpg'))
            """
        },
        "ColorColumn": {
            "description": "Display color swatches based on hex values",
            "common_options": [
                "sortable()", "searchable()", "toggleable()",
                "copyable()", "tooltip()"
            ],
            "example": """
            ColorColumn::make('brand_color')
                ->sortable()
                ->copyable()
                ->tooltip(fn ($record) => "RGB: " . implode(', ', sscanf($record->brand_color, "#%02x%02x%02x")))
            """
        },
        "BadgeColumn": {
            "description": "Display values as colored badges",
            "common_options": [
                "sortable()", "searchable()", "toggleable()", "enum()",
                "colors()", "icons()", "extraAttributes()"
            ],
            "example": """
            BadgeColumn::make('status')
                ->sortable()
                ->searchable()
                ->colors([
                    'primary' => 'pending',
                    'success' => 'approved',
                    'danger' => 'rejected',
                ])
                ->icons([
                    'heroicon-o-clock' => 'pending',
                    'heroicon-o-check' => 'approved',
                    'heroicon-o-x-mark' => 'rejected',
                ])
            """
        }
    },
    "Numeric and Currency Columns": {
        "TextColumn with formatters": {
            "description": "TextColumn with numeric formatting options",
            "common_options": [
                "sortable()", "searchable()", "toggleable()", "numeric()",
                "money()", "percentage()", "prefix()", "suffix()"
            ],
            "example": """
            // Numeric formatting
            TextColumn::make('views')
                ->sortable()
                ->numeric(
                    decimalPlaces: 0,
                    decimalSeparator: '.',
                    thousandsSeparator: ',',
                )
                ->suffix(' views')
                
            // Currency formatting
            TextColumn::make('price')
                ->sortable()
                ->money('usd')
                
            // Percentage formatting
            TextColumn::make('completion_rate')
                ->sortable()
                ->percentage(
                    decimalPlaces: 1,
                )
            """
        }
    },
    "Relationship Columns": {
        "Relationship Display": {
            "description": "Display data from related models",
            "common_options": [
                "sortable()", "searchable()", "toggleable()", "listWithLineBreaks()",
                "bulleted()", "limitList()"
            ],
            "example": """
            // Display a single related model's attribute
            TextColumn::make('author.name')
                ->sortable()
                ->searchable()
                
            // Display multiple related models with list formatting
            TextColumn::make('categories.name')
                ->label('Categories')
                ->listWithLineBreaks()
                ->bulleted()
                ->limitList(3)
                ->expandableLimitedList()
            """
        }
    },
    "Toggle Columns": {
        "ToggleColumn": {
            "description": "Toggle switch for boolean values that can be changed directly in the table",
            "common_options": [
                "sortable()", "disabled()", "onColor()", "offColor()",
                "afterStateUpdated()"
            ],
            "example": """
            ToggleColumn::make('is_active')
                ->label('Active')
                ->sortable()
                ->disabled(fn ($record) => $record->is_locked)
                ->onColor('success')
                ->offColor('danger')
                ->afterStateUpdated(function ($record, $state) {
                    // Perform action after toggle is updated
                    if ($state) {
                        ActivityLog::create([
                            'description' => "Activated user {$record->name}",
                            'user_id' => auth()->id(),
                        ]);
                    }
                })
            """
        }
    },
    "Select Columns": {
        "SelectColumn": {
            "description": "Dropdown select input directly in the table",
            "common_options": [
                "sortable()", "options()", "disabled()", "placeholder()",
                "afterStateUpdated()", "selectablePlaceholder()"
            ],
            "example": """
            SelectColumn::make('status')
                ->label('Status')
                ->options([
                    'pending' => 'Pending',
                    'processing' => 'Processing',
                    'completed' => 'Completed',
                    'canceled' => 'Canceled',
                ])
                ->sortable()
                ->placeholder('Select status')
                ->disabled(fn ($record) => $record->is_locked)
                ->afterStateUpdated(function ($record, $state) {
                    // Perform action after status is updated
                    ActivityLog::create([
                        'description' => "Updated order {$record->id} status to {$state}",
                        'user_id' => auth()->id(),
                    ]);
                })
            """
        }
    }
}

# Table Filters
TABLE_FILTERS = {
    "Basic Filters": {
        "SelectFilter": {
            "description": "Filter records based on a dropdown selection",
            "options": [
                "options()", "multiple()", "default()", "placeholder()",
                "query()", "indicateUsing()"
            ],
            "example": """
            SelectFilter::make('status')
                ->options([
                    'pending' => 'Pending',
                    'processing' => 'Processing',
                    'completed' => 'Completed',
                    'canceled' => 'Canceled',
                ])
                ->multiple()
                ->label('Order Status')
                ->placeholder('All Statuses')
                ->default('pending')
                ->indicateUsing(function (array $state): array {
                    if (blank($state['value'] ?? null)) {
                        return [];
                    }
                    
                    return [
                        'Status: ' . collect($this->getOptions())
                            ->get($state['value']),
                    ];
                })
            """
        },
        "TernaryFilter": {
            "description": "Three-state filter for boolean values (yes/no/all)",
            "options": [
                "placeholder()", "trueLabel()", "falseLabel()",
                "queries()", "default()"
            ],
            "example": """
            TernaryFilter::make('is_featured')
                ->label('Featured')
                ->placeholder('All Products')
                ->trueLabel('Featured Products')
                ->falseLabel('Non-Featured Products')
                ->queries(
                    true: fn (Builder $query) => $query->where('is_featured', true),
                    false: fn (Builder $query) => $query->where('is_featured', false),
                    blank: fn (Builder $query) => $query,
                )
            """
        },
        "Filter (Custom)": {
            "description": "Create a custom filter with form components",
            "options": [
                "form()", "query()", "indicateUsing()"
            ],
            "example": """
            Filter::make('created_at')
                ->form([
                    DatePicker::make('created_from'),
                    DatePicker::make('created_until'),
                ])
                ->query(function (Builder $query, array $data): Builder {
                    return $query
                        ->when(
                            $data['created_from'],
                            fn (Builder $query, $date): Builder => $query->whereDate('created_at', '>=', $date),
                        )
                        ->when(
                            $data['created_until'],
                            fn (Builder $query, $date): Builder => $query->whereDate('created_at', '<=', $date),
                        );
                })
                ->indicateUsing(function (array $data): array {
                    $indicators = [];
                    
                    if ($data['created_from'] ?? null) {
                        $indicators[] = 'Created from ' . Carbon::parse($data['created_from'])->toFormattedDate();
                    }
                    
                    if ($data['created_until'] ?? null) {
                        $indicators[] = 'Created until ' . Carbon::parse($data['created_until'])->toFormattedDate();
                    }
                    
                    return $indicators;
                })
            """
        },
        "Relationship Filters": {
            "description": "Filter records based on related models",
            "options": [
                "relationship()", "multiple()", "preload()",
                "searchable()"
            ],
            "example": """
            SelectFilter::make('author')
                ->relationship('author', 'name')
                ->searchable()
                ->preload()
                ->label('Filter by Author')
                ->placeholder('All Authors')
                ->multiple()
            """
        }
    },
    "Advanced Filters": {
        "Tables Filters": {
            "description": "Apply multiple filters together",
            "example": """
            public static function table(Table $table): Table
            {
                return $table
                    ->columns([
                        // ...
                    ])
                    ->filters([
                        Tables\\Filters\\SelectFilter::make('status')
                            ->options([
                                'pending' => 'Pending',
                                'processing' => 'Processing',
                                'completed' => 'Completed',
                                'canceled' => 'Canceled',
                            ])
                            ->multiple(),
                        Tables\\Filters\\Filter::make('created_at')
                            ->form([
                                DatePicker::make('created_from'),
                                DatePicker::make('created_until'),
                            ])
                            ->query(function (Builder $query, array $data): Builder {
                                return $query
                                    ->when(
                                        $data['created_from'],
                                        fn (Builder $query, $date): Builder => $query->whereDate('created_at', '>=', $date),
                                    )
                                    ->when(
                                        $data['created_until'],
                                        fn (Builder $query, $date): Builder => $query->whereDate('created_at', '<=', $date),
                                    );
                            }),
                        Tables\\Filters\\TernaryFilter::make('is_featured'),
                    ])
                    ->filtersFormWidth('sm') // Adjusts filter form width
                    ->filtersLayout(FiltersLayout::AboveContent) // Position filters above content
                    ->persistFiltersInSession(); // Remember filters between requests
            }
            """
        },
        "Filter Presets": {
            "description": "Create predefined filter combinations",
            "example": """
            public static function table(Table $table): Table
            {
                return $table
                    ->columns([
                        // ...
                    ])
                    ->filters([
                        // ...
                    ])
                    ->filterPresets([
                        'recent-orders' => [
                            'status' => ['processing'],
                            'created_at' => [
                                'created_from' => now()->subWeek()->format('Y-m-d'),
                            ],
                        ],
                        'high-value-orders' => [
                            'total' => [
                                'min' => 1000,
                            ],
                        ],
                        'problematic-orders' => [
                            'status' => ['refunded', 'canceled'],
                        ],
                    ]);
            }
            """
        }
    }
}

# Table Actions
TABLE_ACTIONS = {
    "Row Actions": {
        "EditAction": {
            "description": "Opens a form to edit the record",
            "options": [
                "url()", "form()", "mutateFormDataUsing()",
                "fillForm()", "successRedirectUrl()"
            ],
            "example": """
            EditAction::make()
                ->url(fn ($record): string => route('posts.edit', $record))
                ->form([
                    TextInput::make('title')->required(),
                    MarkdownEditor::make('content'),
                ])
                ->fillForm(fn ($record) => [
                    'title' => $record->title,
                    'content' => $record->content,
                ])
                ->mutateFormDataUsing(function (array $data): array {
                    $data['user_id'] = auth()->id();
                    
                    return $data;
                })
                ->successRedirectUrl(route('posts.index'))
                ->successNotificationTitle('Post updated')
            """
        },
        "ViewAction": {
            "description": "Opens a modal or redirects to view record details",
            "options": [
                "url()", "modalContent()", "modalSubmitAction()",
                "modalFooterActions()", "modalWidth()"
            ],
            "example": """
            ViewAction::make()
                ->label('View Details')
                ->icon('heroicon-s-eye')
                ->modalContent(function ($record) {
                    return new HtmlString('
                        <div class="space-y-4">
                            <h2 class="text-xl font-bold">' . e($record->title) . '</h2>
                            <div class="prose">' . Str::markdown($record->content) . '</div>
                            <div class="text-sm">
                                Published: ' . $record->published_at->format('F j, Y') . '
                            </div>
                        </div>
                    ');
                })
                ->modalWidth('3xl')
                ->modalSubmitAction(false) // Hides the submit button
                ->modalFooterActions(function ($record) {
                    return [
                        Action::make('edit')
                            ->label('Edit Post')
                            ->url(route('posts.edit', $record))
                            ->color('primary'),
                    ];
                })
            """
        },
        "DeleteAction": {
            "description": "Delete a record with confirmation",
            "options": [
                "requiresConfirmation()", "modalDescription()",
                "modalHeading()", "successRedirectUrl()"
            ],
            "example": """
            DeleteAction::make()
                ->requiresConfirmation()
                ->modalHeading('Delete Post')
                ->modalDescription('Are you sure you want to delete this post? This action cannot be undone.')
                ->modalSubmitActionLabel('Yes, delete it')
                ->successNotificationTitle('Post deleted')
                ->successRedirectUrl(route('posts.index'))
                ->after(function ($record) {
                    // Additional actions after deletion
                    Activity::create([
                        'description' => "Deleted post {$record->title}",
                        'user_id' => auth()->id(),
                    ]);
                })
            """
        },
        "Custom Action": {
            "description": "Create a custom action with specific behavior",
            "options": [
                "action()", "form()", "fillForm()", "visible()",
                "hidden()", "link()", "button()"
            ],
            "example": """
            Action::make('approve')
                ->label('Approve')
                ->icon('heroicon-o-check')
                ->color('success')
                ->visible(fn ($record) => $record->status === 'pending')
                ->form([
                    Textarea::make('comment')
                        ->placeholder('Add an optional comment')
                        ->columnSpanFull(),
                ])
                ->action(function (array $data, $record): void {
                    $record->update([
                        'status' => 'approved',
                        'approved_at' => now(),
                        'approved_by' => auth()->id(),
                        'approval_comment' => $data['comment'],
                    ]);
                    
                    Notification::make()
                        ->title('Approved successfully')
                        ->success()
                        ->send();
                })
                ->requiresConfirmation()
                ->modalHeading('Approve Post')
                ->modalDescription('Are you sure you want to approve this post? It will be visible to all users.')
                ->modalSubmitActionLabel('Yes, approve')
            """
        }
    },
    "Bulk Actions": {
        "DeleteBulkAction": {
            "description": "Delete multiple records at once",
            "options": [
                "requiresConfirmation()", "modalDescription()",
                "modalHeading()", "deselectRecordsAfterCompletion()"
            ],
            "example": """
            DeleteBulkAction::make()
                ->requiresConfirmation()
                ->modalHeading('Delete Selected Posts')
                ->modalDescription('Are you sure you want to delete these posts? This action cannot be undone.')
                ->modalSubmitActionLabel('Yes, delete them')
                ->successNotificationTitle(fn (int $count) => "Deleted {$count} posts")
                ->deselectRecordsAfterCompletion()
                ->after(function ($records) {
                    // Additional actions after bulk deletion
                    Activity::create([
                        'description' => "Bulk deleted {$records->count()} posts",
                        'user_id' => auth()->id(),
                    ]);
                })
            """
        },
        "Custom Bulk Action": {
            "description": "Create a custom action for multiple records",
            "options": [
                "action()", "form()", "deselectRecordsAfterCompletion()",
                "modalContent()", "visible()", "hidden()"
            ],
            "example": """
            BulkAction::make('publish')
                ->label('Publish Selected')
                ->icon('heroicon-o-globe-alt')
                ->color('success')
                ->form([
                    DateTimePicker::make('published_at')
                        ->label('Publication Date')
                        ->default(now())
                        ->required(),
                    Toggle::make('notify_subscribers')
                        ->label('Notify Subscribers')
                        ->default(true),
                ])
                ->action(function (Collection $records, array $data): void {
                    $records->each(function ($record) use ($data): void {
                        $record->update([
                            'status' => 'published',
                            'published_at' => $data['published_at'],
                        ]);
                        
                        if ($data['notify_subscribers']) {
                            // Send notification logic here
                        }
                    });
                    
                    Notification::make()
                        ->title(fn () => "Published {$records->count()} posts")
                        ->success()
                        ->send();
                })
                ->requiresConfirmation()
                ->modalHeading('Publish Selected Posts')
                ->modalDescription('Are you sure you want to publish these posts? They will be visible to all users.')
                ->modalSubmitActionLabel('Yes, publish them')
                ->deselectRecordsAfterCompletion()
            """
        }
    },
    "Header Actions": {
        "CreateAction": {
            "description": "Create a new record",
            "options": [
                "url()", "form()", "mutateFormDataUsing()",
                "successRedirectUrl()"
            ],
            "example": """
            CreateAction::make()
                ->label('New Post')
                ->icon('heroicon-o-plus')
                ->form([
                    TextInput::make('title')->required(),
                    MarkdownEditor::make('content')->required(),
                    Select::make('category_id')
                        ->relationship('category', 'name')
                        ->required(),
                ])
                ->mutateFormDataUsing(function (array $data): array {
                    $data['user_id'] = auth()->id();
                    
                    return $data;
                })
                ->successRedirectUrl(fn ($record) => route('posts.edit', $record))
                ->successNotificationTitle('Post created')
            """
        },
        "Custom Header Action": {
            "description": "Create a custom action in the table header",
            "options": [
                "url()", "action()", "visible()", "hidden()",
                "modalContent()", "form()"
            ],
            "example": """
            // Export action
            Action::make('export')
                ->label('Export')
                ->icon('heroicon-o-document-arrow-down')
                ->color('gray')
                ->action(function (array $data): void {
                    // Export logic
                    Excel::download(new PostsExport($data['format']), "posts.{$data['format']}");
                    
                    Notification::make()
                        ->title('Export started')
                        ->body('Your export will be available in a few moments.')
                        ->success()
                        ->send();
                })
                ->form([
                    Select::make('format')
                        ->label('Export Format')
                        ->options([
                            'csv' => 'CSV',
                            'xlsx' => 'Excel (XLSX)',
                            'pdf' => 'PDF',
                        ])
                        ->default('csv')
                        ->required(),
                ])
            """
        }
    }
}

# Advanced Table Features
ADVANCED_TABLE_FEATURES = {
    "Table Configuration": {
        "description": "Configure advanced table behavior",
        "example": """
        public static function table(Table $table): Table
        {
            return $table
                ->columns([
                    // ... columns
                ])
                ->filters([
                    // ... filters
                ])
                ->actions([
                    // ... actions
                ])
                ->bulkActions([
                    // ... bulk actions
                ])
                ->defaultSort('created_at', 'desc') // Default sorting
                ->searchable() // Enable global search
                ->searchPlaceholder('Search posts...') // Custom search placeholder
                ->searchableColumns([ // Specific searchable columns
                    'title',
                    'content',
                    'author.name',
                ])
                ->paginated([10, 25, 50, 100, 'all']) // Pagination options
                ->defaultPaginationPageOption(25) // Default pagination
                ->poll('30s') // Auto-refresh table every 30 seconds
                ->deferLoading() // Defer loading until button click
                ->striped() // Striped rows
                ->reorderable('sort') // Enable drag-and-drop reordering
                ->persistSortInSession() // Remember sorting between requests
                ->persistColumnSearchesInSession() // Remember column searches
                ->selectablePlaceholder('Select item') // Custom selector text
                ->groups([ // Group records
                    'status',
                    'category.name',
                ])
                ->groupsOnly(true) // Only show grouped records
                ->contentGrid([
                    'md' => 2,
                    'xl' => 3,
                ]) // Grid layout for records
                ->emptyStateIcon('heroicon-o-document') // Empty state icon
                ->emptyStateHeading('No posts yet') // Empty state heading
                ->emptyStateDescription('Once you create a post, it will appear here.') // Description
                ->emptyStateActions([ // Empty state actions
                    Action::make('create')
                        ->label('Create post')
                        ->url(route('posts.create'))
                        ->icon('heroicon-o-plus')
                        ->button(),
                ]);
        }
        """
    },
    "Record URLs": {
        "description": "Configure clickable records in the table",
        "example": """
        public static function table(Table $table): Table
        {
            return $table
                ->columns([
                    // ... columns
                ])
                ->recordUrl(
                    fn ($record) => route('posts.edit', $record)
                )
                ->recordAction(
                    Tables\Actions\ViewAction::make()
                )
                ->recordClickAction(
                    function ($record) {
                        return Tables\Actions\ViewAction::make()
                            ->record($record);
                    }
                );
        }
        """
    },
    "Custom Views": {
        "description": "Customize how records are displayed (list, grid, etc.)",
        "example": """
        public static function table(Table $table): Table
        {
            return $table
                ->columns([
                    // ... columns
                ])
                ->defaultView('grid') // Default to grid view
                ->views([
                    Tables\Views\ListView::make()
                        ->icon('heroicon-m-list-bullet')
                        ->label('List')
                        ->columns([
                            // List-specific columns
                        ]),
                    Tables\Views\GridView::make()
                        ->icon('heroicon-m-squares-2x2')
                        ->label('Grid')
                        ->columns([
                            // Grid-specific columns
                        ])
                        ->defaultSort('created_at', 'desc'),
                    Tables\Views\KanbanView::make()
                        ->icon('heroicon-m-view-columns')
                        ->label('Kanban')
                        ->statusColumn('status')
                        ->columns([
                            // Kanban-specific columns
                        ]),
                ]);
        }
        """
    }
}

# Function to get the table builder knowledge
def get_table_builder_knowledge() -> Dict[str, Any]:
    """
    Returns the comprehensive FilamentPHP table builder knowledge base
    """
    return {
        "overview": TABLE_BUILDER_OVERVIEW,
        "columns": TABLE_COLUMNS,
        "filters": TABLE_FILTERS,
        "actions": TABLE_ACTIONS,
        "advanced_features": ADVANCED_TABLE_FEATURES
    } 