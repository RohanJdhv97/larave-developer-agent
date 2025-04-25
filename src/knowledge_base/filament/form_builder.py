"""
FilamentPHP Form Builder Knowledge Base

This module contains comprehensive knowledge about FilamentPHP form builder components,
including field types, layouts, validation, and advanced usage patterns.
"""

from typing import Dict, List, Any

# Form Builder Overview
FORM_BUILDER_OVERVIEW = """
The FilamentPHP Form Builder is a powerful tool for creating dynamic, responsive forms with
minimal code. It provides a wide range of field types, layouts, and validation options that
make it easy to build complex forms quickly.

Key features of the Form Builder:
- Rich collection of form field components
- Responsive layouts with grid support
- Real-time validation
- Conditional form logic
- File uploads with preview
- Multi-step forms with wizard interface
- Form actions and button customization
- Internationalization support
- Custom field types
- Dark mode support
"""

# Form Fields
FORM_FIELDS = {
    "Text Inputs": {
        "TextInput": {
            "description": "Standard text input field for single-line text entry",
            "common_options": [
                "required()", "maxLength()", "minLength()", "email()", "tel()", 
                "url()", "numeric()", "password()", "autocomplete()", "placeholder()",
                "prefix()", "suffix()", "mask()"
            ],
            "example": """
            TextInput::make('name')
                ->required()
                ->maxLength(255)
                ->placeholder('John Doe')
                ->label('Full Name')
                ->helperText('Enter your full name as it appears on your ID')
            """
        },
        "Textarea": {
            "description": "Multi-line text input for longer content",
            "common_options": [
                "required()", "maxLength()", "minLength()", "placeholder()", 
                "autosize()", "rows()", "cols()"
            ],
            "example": """
            Textarea::make('description')
                ->required()
                ->maxLength(65535)
                ->rows(5)
                ->placeholder('Enter a detailed description...')
                ->columnSpanFull()
            """
        },
        "MarkdownEditor": {
            "description": "Rich markdown editor with preview support",
            "common_options": [
                "required()", "toolbarButtons()", "fileAttachmentsDirectory()",
                "disableToolbarButtons()", "enableToolbarButtons()"
            ],
            "example": """
            MarkdownEditor::make('content')
                ->required()
                ->fileAttachmentsDirectory('attachments')
                ->toolbarButtons([
                    'bold', 'italic', 'strike', 'link', 'heading', 'bulletList', 
                    'orderedList', 'codeBlock', 'attachFiles'
                ])
                ->columnSpanFull()
            """
        }
    },
    "Selection Inputs": {
        "Select": {
            "description": "Dropdown select input with search capability",
            "common_options": [
                "required()", "options()", "searchable()", "multiple()", 
                "preload()", "relationship()", "allowHtml()", "placeholder()"
            ],
            "example": """
            Select::make('status')
                ->required()
                ->options([
                    'draft' => 'Draft',
                    'reviewing' => 'Reviewing',
                    'published' => 'Published',
                    'archived' => 'Archived',
                ])
                ->default('draft')
                ->searchable()
            """
        },
        "Checkbox": {
            "description": "Single checkbox for boolean values",
            "common_options": [
                "required()", "inline()", "afterStateUpdated()"
            ],
            "example": """
            Checkbox::make('is_featured')
                ->label('Featured article')
                ->helperText('Featured articles appear on the homepage')
                ->default(false)
            """
        },
        "CheckboxList": {
            "description": "Multiple checkboxes grouped together",
            "common_options": [
                "required()", "options()", "columns()", "inline()",
                "bulkToggleable()", "gridDirection()"
            ],
            "example": """
            CheckboxList::make('roles')
                ->required()
                ->options([
                    'admin' => 'Administrator',
                    'editor' => 'Editor',
                    'viewer' => 'Viewer',
                ])
                ->columns(3)
                ->bulkToggleable()
                ->helperText('Select all applicable roles')
            """
        },
        "Radio": {
            "description": "Radio button group for single selection",
            "common_options": [
                "required()", "options()", "boolean()", "inline()"
            ],
            "example": """
            Radio::make('publish_status')
                ->required()
                ->options([
                    'publish_now' => 'Publish now',
                    'scheduled' => 'Schedule for later',
                    'draft' => 'Save as draft',
                ])
                ->default('draft')
                ->inline(false)
            """
        },
        "Toggle": {
            "description": "Toggle switch for boolean values",
            "common_options": [
                "required()", "onColor()", "offColor()", "inline()", "icons()"
            ],
            "example": """
            Toggle::make('is_active')
                ->label('Active')
                ->helperText('Inactive users cannot log in')
                ->onColor('success')
                ->offColor('danger')
                ->default(true)
            """
        }
    },
    "Date and Time": {
        "DatePicker": {
            "description": "Calendar interface for selecting dates",
            "common_options": [
                "required()", "format()", "displayFormat()", "minDate()", 
                "maxDate()", "disabledDates()", "timezone()"
            ],
            "example": """
            DatePicker::make('publication_date')
                ->required()
                ->label('Publication Date')
                ->format('Y-m-d')
                ->displayFormat('F j, Y')
                ->minDate(now())
                ->default(now())
            """
        },
        "DateTimePicker": {
            "description": "Calendar with time selection",
            "common_options": [
                "required()", "format()", "displayFormat()", "minDate()", 
                "maxDate()", "disabledDates()", "timezone()", "seconds()"
            ],
            "example": """
            DateTimePicker::make('published_at')
                ->required()
                ->label('Publish At')
                ->format('Y-m-d H:i')
                ->displayFormat('F j, Y H:i')
                ->timezone('UTC')
                ->seconds(false)
                ->default(now())
            """
        },
        "TimePicker": {
            "description": "Time selection input",
            "common_options": [
                "required()", "format()", "hoursStep()", "minutesStep()",
                "seconds()", "timezone()"
            ],
            "example": """
            TimePicker::make('start_time')
                ->required()
                ->label('Start Time')
                ->format('H:i')
                ->hoursStep(1)
                ->minutesStep(15)
                ->seconds(false)
            """
        }
    },
    "File Uploads": {
        "FileUpload": {
            "description": "File upload field with drag and drop support",
            "common_options": [
                "required()", "disk()", "directory()", "maxSize()", "minSize()",
                "acceptedFileTypes()", "maxFiles()", "multiple()", "image()"
            ],
            "example": """
            FileUpload::make('attachment')
                ->required()
                ->label('Document')
                ->disk('public')
                ->directory('attachments')
                ->maxSize(5120) // 5MB
                ->acceptedFileTypes(['application/pdf', 'application/msword'])
                ->downloadable()
            """
        },
        "FileUpload (Images)": {
            "description": "Image upload with preview",
            "common_options": [
                "required()", "disk()", "directory()", "maxSize()", "image()",
                "imageResizeMode()", "imageCropAspectRatio()", "imageResizeTargetWidth()"
            ],
            "example": """
            FileUpload::make('avatar')
                ->required()
                ->image()
                ->disk('public')
                ->directory('avatars')
                ->maxSize(2048) // 2MB
                ->imageResizeMode('cover')
                ->imageCropAspectRatio('1:1')
                ->imageResizeTargetWidth('300')
                ->imageResizeTargetHeight('300')
            """
        }
    },
    "Relationship Fields": {
        "Select (Relationship)": {
            "description": "Select input for Eloquent relationships",
            "common_options": [
                "required()", "relationship()", "searchable()", "preload()",
                "multiple()", "createOptionForm()", "editOptionForm()"
            ],
            "example": """
            Select::make('author_id')
                ->relationship('author', 'name')
                ->searchable()
                ->preload()
                ->createOptionForm([
                    TextInput::make('name')
                        ->required()
                        ->maxLength(255),
                    TextInput::make('email')
                        ->required()
                        ->email()
                        ->maxLength(255),
                ])
                ->required()
            """
        },
        "CheckboxList (Relationship)": {
            "description": "Multiple checkboxes for many-to-many relationships",
            "common_options": [
                "required()", "relationship()", "columns()", "bulkToggleable()"
            ],
            "example": """
            CheckboxList::make('categories')
                ->relationship('categories', 'name')
                ->columns(3)
                ->bulkToggleable()
            """
        },
        "Repeater": {
            "description": "Repeatable form sections for has-many relationships",
            "common_options": [
                "required()", "schema()", "itemLabel()", "maxItems()", "minItems()",
                "collapsible()", "collapsed()", "reorderable()"
            ],
            "example": """
            Repeater::make('educations')
                ->relationship()
                ->schema([
                    TextInput::make('institution')
                        ->required()
                        ->maxLength(255),
                    TextInput::make('degree')
                        ->required()
                        ->maxLength(255),
                    DatePicker::make('start_date')
                        ->required(),
                    DatePicker::make('end_date'),
                ])
                ->itemLabel(fn (array $state): ?string => $state['institution'] ?? null)
                ->collapsible()
                ->reorderable()
                ->maxItems(5)
            """
        }
    },
    "Advanced Components": {
        "KeyValue": {
            "description": "Dynamic key-value pair inputs for metadata",
            "common_options": [
                "required()", "keyLabel()", "valueLabel()", "reorderable()",
                "keyPlaceholder()", "valuePlaceholder()"
            ],
            "example": """
            KeyValue::make('meta')
                ->keyLabel('Property')
                ->valueLabel('Value')
                ->keyPlaceholder('Property name')
                ->valuePlaceholder('Property value')
                ->reorderable()
                ->columnSpanFull()
            """
        },
        "RichEditor": {
            "description": "WYSIWYG rich text editor",
            "common_options": [
                "required()", "toolbarButtons()", "fileAttachmentsDirectory()",
                "disableToolbarButtons()"
            ],
            "example": """
            RichEditor::make('content')
                ->required()
                ->fileAttachmentsDirectory('rich-text-attachments')
                ->toolbarButtons([
                    'bold', 'italic', 'underline', 'link', 'strike', 'blockquote',
                    'h2', 'h3', 'orderedList', 'bulletList', 'redo', 'undo',
                ])
                ->columnSpanFull()
            """
        },
        "TagsInput": {
            "description": "Input for entering multiple tags",
            "common_options": [
                "required()", "separator()", "suggestions()", "placeholder()"
            ],
            "example": """
            TagsInput::make('tags')
                ->separator(',')
                ->suggestions([
                    'tailwind', 'alpine', 'laravel', 'livewire',
                ])
                ->placeholder('Add a tag')
            """
        },
        "ColorPicker": {
            "description": "Color selection input",
            "common_options": [
                "required()", "rgba()", "hexColor()"
            ],
            "example": """
            ColorPicker::make('brand_color')
                ->required()
                ->hexColor() // or ->rgba()
            """
        }
    }
}

# Form Layouts
FORM_LAYOUTS = {
    "Grid Layout": {
        "description": "Responsive grid layout system for form fields",
        "features": [
            "Customizable column spans",
            "Responsive behavior at different breakpoints",
            "Automatic responsive adaptations"
        ],
        "example": """
        public static function form(Form $form): Form
        {
            return $form
                ->schema([
                    TextInput::make('first_name')
                        ->required()
                        ->maxLength(255)
                        ->columnSpan(6),
                    TextInput::make('last_name')
                        ->required()
                        ->maxLength(255)
                        ->columnSpan(6),
                    Textarea::make('bio')
                        ->columnSpanFull(),
                ]);
        }
        """
    },
    "Fieldset": {
        "description": "Group related fields with a border and label",
        "features": [
            "Visual grouping of related fields",
            "Custom labels",
            "Optional collapsible behavior"
        ],
        "example": """
        Fieldset::make('Personal Information')
            ->schema([
                TextInput::make('first_name')->required(),
                TextInput::make('last_name')->required(),
                DatePicker::make('date_of_birth'),
            ])
            ->columns(3)
        """
    },
    "Section": {
        "description": "Group fields with a heading and description",
        "features": [
            "Custom headings and descriptions",
            "Optional collapsible behavior",
            "Icon support"
        ],
        "example": """
        Section::make('User Information')
            ->description('Basic information about the user')
            ->icon('heroicon-o-user')
            ->schema([
                TextInput::make('name')->required(),
                TextInput::make('email')->email()->required(),
                Select::make('role')
                    ->options([
                        'admin' => 'Administrator',
                        'editor' => 'Editor',
                        'user' => 'User',
                    ])
                    ->required(),
            ])
            ->columns(3)
            ->collapsible()
        """
    },
    "Tabs": {
        "description": "Organize form into tabbed sections",
        "features": [
            "Multiple tabs for complex forms",
            "Icon support for tabs",
            "Custom tab labels",
            "Validation across tabs"
        ],
        "example": """
        Tabs::make('Form')
            ->tabs([
                Tab::make('Personal Information')
                    ->icon('heroicon-o-user')
                    ->schema([
                        TextInput::make('name')->required(),
                        TextInput::make('email')->email()->required(),
                        DatePicker::make('date_of_birth'),
                    ]),
                Tab::make('Address')
                    ->icon('heroicon-o-map-pin')
                    ->schema([
                        TextInput::make('address_line_1')->required(),
                        TextInput::make('address_line_2'),
                        TextInput::make('city')->required(),
                        TextInput::make('state')->required(),
                        TextInput::make('postal_code')->required(),
                    ]),
                Tab::make('Settings')
                    ->icon('heroicon-o-cog')
                    ->schema([
                        Toggle::make('is_active')->default(true),
                        Toggle::make('email_notifications')->default(true),
                        Select::make('theme')
                            ->options([
                                'light' => 'Light',
                                'dark' => 'Dark',
                                'system' => 'System',
                            ])
                            ->default('system'),
                    ]),
            ])
            ->columnSpanFull()
        """
    },
    "Card": {
        "description": "Display fields in a card with header and footer",
        "features": [
            "Visual container for form fields",
            "Optional header and footer",
            "Custom styling options"
        ],
        "example": """
        Card::make()
            ->schema([
                TextInput::make('username')->required(),
                TextInput::make('password')
                    ->password()
                    ->required()
                    ->confirmed(),
                TextInput::make('password_confirmation')
                    ->password()
                    ->required(),
            ])
            ->columns(1)
        """
    },
    "Wizard": {
        "description": "Multi-step form with progress tracking",
        "features": [
            "Step-by-step form process",
            "Progress indicator",
            "Validation per step",
            "Navigation between steps"
        ],
        "example": """
        Wizard::make([
            Step::make('Personal Information')
                ->icon('heroicon-o-user')
                ->schema([
                    TextInput::make('first_name')->required(),
                    TextInput::make('last_name')->required(),
                    DatePicker::make('date_of_birth'),
                ]),
            Step::make('Contact Information')
                ->icon('heroicon-o-phone')
                ->schema([
                    TextInput::make('email')->email()->required(),
                    TextInput::make('phone')->tel(),
                ]),
            Step::make('Account Settings')
                ->icon('heroicon-o-cog')
                ->schema([
                    TextInput::make('username')->required(),
                    TextInput::make('password')
                        ->password()
                        ->required()
                        ->confirmed(),
                    TextInput::make('password_confirmation')
                        ->password()
                        ->required(),
                ]),
        ])
        ->skippable() // Allow skipping non-required steps
        ->persistStepInQueryString('step') // Remember the current step in the URL
        ->columnSpanFull()
        """
    }
}

# Validation
VALIDATION = {
    "Basic Validation": {
        "required": "Makes the field required",
        "nullable": "Allows the field to be null",
        "email": "Validates the field as an email address",
        "url": "Validates the field as a URL",
        "max": "Specifies the maximum value or length",
        "min": "Specifies the minimum value or length",
        "numeric": "Validates the field as a numeric value",
        "alpha": "Validates the field contains only alphabetic characters"
    },
    "Advanced Validation": {
        "rules": "Apply custom Laravel validation rules",
        "unique": "Validate uniqueness against a database table",
        "exists": "Validate existence in a database table",
        "after": "Validates a date is after another date",
        "before": "Validates a date is before another date",
        "confirmed": "Validates a confirmation field matches (e.g., password)",
        "dimensions": "Validates image dimensions",
        "in": "Validates the value is in a given list",
        "not_in": "Validates the value is not in a given list"
    },
    "Complex Validation Example": """
    TextInput::make('username')
        ->required()
        ->unique(table: User::class, column: 'username', ignorable: fn ($record) => $record)
        ->regex('/^[a-z0-9_-]{3,16}$/')
        ->validationAttribute('Username')
        ->validationMessages([
            'required' => 'Please enter a username',
            'unique' => 'This username is already taken',
            'regex' => 'Username must be 3-16 characters long and only contain letters, numbers, dashes and underscores',
        ])
    """
}

# Conditional Logic
CONDITIONAL_LOGIC = {
    "Visibility Conditions": {
        "visible": "Control field visibility based on a condition",
        "hidden": "Hide field based on a condition",
        "example": """
        Select::make('payment_type')
            ->options([
                'credit_card' => 'Credit Card',
                'bank_transfer' => 'Bank Transfer',
                'paypal' => 'PayPal',
            ])
            ->live()
            ->required(),
        
        Grid::make(3)
            ->schema([
                TextInput::make('card_number')
                    ->label('Card Number')
                    ->required()
                    ->visible(fn (Get $get) => $get('payment_type') === 'credit_card'),
                
                TextInput::make('expiration_date')
                    ->label('Expiration Date')
                    ->mask('99/99')
                    ->required()
                    ->visible(fn (Get $get) => $get('payment_type') === 'credit_card'),
                
                TextInput::make('security_code')
                    ->label('CVC/CVV')
                    ->required()
                    ->visible(fn (Get $get) => $get('payment_type') === 'credit_card'),
            ])
        """
    },
    "Required Conditions": {
        "required": "Make field required conditionally",
        "example": """
        Toggle::make('has_existing_address')
            ->label('I have an existing address')
            ->live(),
        
        TextInput::make('address_id')
            ->label('Address ID')
            ->required(fn (Get $get) => $get('has_existing_address'))
            ->disabled(fn (Get $get) => ! $get('has_existing_address'))
        """
    },
    "Complex Logic": {
        "description": "Combine multiple conditions for complex form behaviors",
        "example": """
        Radio::make('employment_status')
            ->options([
                'employed' => 'Employed',
                'self_employed' => 'Self-employed',
                'unemployed' => 'Unemployed',
                'retired' => 'Retired',
            ])
            ->live()
            ->required(),
        
        TextInput::make('employer_name')
            ->required(fn (Get $get) => $get('employment_status') === 'employed')
            ->visible(fn (Get $get) => $get('employment_status') === 'employed'),
        
        TextInput::make('business_name')
            ->required(fn (Get $get) => $get('employment_status') === 'self_employed')
            ->visible(fn (Get $get) => $get('employment_status') === 'self_employed'),
        
        DatePicker::make('retirement_date')
            ->required(fn (Get $get) => $get('employment_status') === 'retired')
            ->visible(fn (Get $get) => $get('employment_status') === 'retired'),
        
        // More complex condition combining multiple fields
        Section::make('Additional Information')
            ->schema([
                TextInput::make('additional_details'),
            ])
            ->visible(fn (Get $get): bool => 
                in_array($get('employment_status'), ['employed', 'self_employed']) && 
                $get('annual_income') > 50000
            )
        """
    }
}

# Function to get the form builder knowledge
def get_form_builder_knowledge() -> Dict[str, Any]:
    """
    Returns the comprehensive FilamentPHP form builder knowledge base
    """
    return {
        "overview": FORM_BUILDER_OVERVIEW,
        "form_fields": FORM_FIELDS,
        "form_layouts": FORM_LAYOUTS,
        "validation": VALIDATION,
        "conditional_logic": CONDITIONAL_LOGIC
    } 