"""
Laravel knowledge base component.

This module provides a storage and retrieval mechanism for Laravel-specific
knowledge, best practices, and code snippets.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import json
import os
from pathlib import Path

class KnowledgeEntry(BaseModel):
    """Model representing an entry in the knowledge base."""
    title: str
    category: str
    content: str
    tags: List[str] = Field(default_factory=list)
    source: Optional[str] = None
    version: Optional[str] = None  # Laravel version this applies to

class LaravelKnowledgeBase(BaseModel):
    """
    Storage and retrieval mechanism for Laravel-specific knowledge.
    
    This class provides methods to store and retrieve Laravel best practices,
    common patterns, and code snippets to help the agent generate accurate
    Laravel code.
    """
    
    entries: Dict[str, KnowledgeEntry] = Field(default_factory=dict)
    
    def add_entry(self, title: str, category: str, content: str, 
                 tags: List[str] = None, source: Optional[str] = None,
                 version: Optional[str] = None):
        """
        Add a knowledge entry to the knowledge base.
        
        Args:
            title: The title of the knowledge entry
            category: The category (e.g., 'model', 'controller', 'migration')
            content: The actual knowledge content
            tags: List of tags for searching
            source: Source of the knowledge (e.g., docs URL)
            version: Laravel version this knowledge applies to
        """
        entry = KnowledgeEntry(
            title=title,
            category=category,
            content=content,
            tags=tags or [],
            source=source,
            version=version
        )
        
        # Use title as the key
        key = title.lower().replace(" ", "_")
        self.entries[key] = entry
    
    def get_entry(self, key: str) -> Optional[KnowledgeEntry]:
        """Get a knowledge entry by key."""
        return self.entries.get(key)
    
    def search_by_tags(self, tags: List[str]) -> List[KnowledgeEntry]:
        """
        Search knowledge entries by tags.
        
        Returns entries that match ANY of the provided tags.
        """
        results = []
        for entry in self.entries.values():
            if any(tag in entry.tags for tag in tags):
                results.append(entry)
        return results
    
    def search_by_category(self, category: str) -> List[KnowledgeEntry]:
        """Search knowledge entries by category."""
        return [entry for entry in self.entries.values() if entry.category == category]
    
    def search_by_version(self, version: str) -> List[KnowledgeEntry]:
        """Search knowledge entries by Laravel version."""
        return [
            entry for entry in self.entries.values() 
            if entry.version and entry.version == version
        ]
    
    def save(self, path: str = "knowledge_base.json"):
        """Save the knowledge base to a JSON file."""
        with open(path, "w") as f:
            # Convert to dict representation
            data = {key: entry.dict() for key, entry in self.entries.items()}
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls, path: str = "knowledge_base.json") -> "LaravelKnowledgeBase":
        """Load the knowledge base from a JSON file."""
        instance = cls()
        
        if not os.path.exists(path):
            # If file doesn't exist, initialize with default knowledge
            instance.initialize_default_knowledge()
            return instance
            
        with open(path, "r") as f:
            data = json.load(f)
            
        # Convert dict back to KnowledgeEntry objects
        entries = {}
        for key, entry_data in data.items():
            entries[key] = KnowledgeEntry(**entry_data)
            
        instance.entries = entries
        return instance
    
    def initialize_default_knowledge(self):
        """
        Initialize the knowledge base with default Laravel knowledge.
        
        This method populates the knowledge base with fundamental Laravel
        best practices and patterns.
        """
        # Model conventions
        self.add_entry(
            title="Laravel Model Conventions",
            category="model",
            content="""
Laravel Eloquent models should follow these conventions:
1. Model names are singular and use PascalCase (e.g., `User`, `BlogPost`)
2. Table names are plural and snake_case (e.g., `users`, `blog_posts`)
3. Primary keys are named `id` by default
4. Models should define fillable or guarded properties
5. Use soft deletes when appropriate with `use SoftDeletes`
6. Define relationships using methods: hasOne, hasMany, belongsTo, etc.
7. Use model events in the boot method for hooks
8. Use scopes for common queries
9. Put models in the `App\\Models` namespace

Example:
```php
<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;
use Illuminate\\Database\\Eloquent\\SoftDeletes;

class Article extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'title', 'content', 'user_id', 'published_at'
    ];

    protected $casts = [
        'published_at' => 'datetime',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function tags()
    {
        return $this->belongsToMany(Tag::class);
    }

    public function scopePublished($query)
    {
        return $query->whereNotNull('published_at');
    }
}
```
            """,
            tags=["model", "eloquent", "conventions", "relationships"],
            source="https://laravel.com/docs/10.x/eloquent",
            version="10.x"
        )
        
        # Controller conventions
        self.add_entry(
            title="Laravel Controller Conventions",
            category="controller",
            content="""
Laravel controllers should follow these conventions:
1. Controllers are named in PascalCase with Controller suffix (e.g., `UserController`)
2. Use resource controllers for CRUD operations
3. Follow RESTful naming for methods (index, create, store, show, edit, update, destroy)
4. Use form requests for validation
5. Keep controllers thin - move business logic to services
6. Return responses with appropriate status codes
7. Use dependency injection for services

Example:
```php
<?php

namespace App\\Http\\Controllers;

use App\\Http\\Requests\\StoreArticleRequest;
use App\\Models\\Article;
use App\\Services\\ArticleService;
use Illuminate\\Http\\Request;

class ArticleController extends Controller
{
    protected $articleService;
    
    public function __construct(ArticleService $articleService)
    {
        $this->articleService = $articleService;
        $this->middleware('auth')->except(['index', 'show']);
    }

    public function index()
    {
        $articles = Article::published()->latest()->paginate(10);
        return view('articles.index', compact('articles'));
    }

    public function create()
    {
        return view('articles.create');
    }

    public function store(StoreArticleRequest $request)
    {
        $article = $this->articleService->createArticle($request->validated());
        return redirect()->route('articles.show', $article)
            ->with('success', 'Article created successfully');
    }

    public function show(Article $article)
    {
        return view('articles.show', compact('article'));
    }

    public function edit(Article $article)
    {
        $this->authorize('update', $article);
        return view('articles.edit', compact('article'));
    }

    public function update(StoreArticleRequest $request, Article $article)
    {
        $this->authorize('update', $article);
        $this->articleService->updateArticle($article, $request->validated());
        return redirect()->route('articles.show', $article)
            ->with('success', 'Article updated successfully');
    }

    public function destroy(Article $article)
    {
        $this->authorize('delete', $article);
        $article->delete();
        return redirect()->route('articles.index')
            ->with('success', 'Article deleted successfully');
    }
}
```
            """,
            tags=["controller", "crud", "restful", "conventions"],
            source="https://laravel.com/docs/10.x/controllers",
            version="10.x"
        )
        
        # Migration conventions
        self.add_entry(
            title="Laravel Migration Conventions",
            category="migration",
            content="""
Laravel migrations should follow these conventions:
1. Migration filenames are prefixed with timestamp and use snake_case
2. Table names are plural and snake_case
3. Include up() and down() methods for migration and rollback
4. Use appropriate column types and modifiers
5. Define foreign keys and indexes when needed
6. Use separate migrations for pivot tables
7. Keep migrations small and focused

Example:
```php
<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('articles', function (Blueprint $table) {
            $table->id();
            $table->string('title');
            $table->text('content');
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->timestamp('published_at')->nullable();
            $table->timestamps();
            $table->softDeletes();
            
            $table->index('published_at');
        });
    }

    public function down()
    {
        Schema::dropIfExists('articles');
    }
};
```
            """,
            tags=["migration", "database", "schema", "conventions"],
            source="https://laravel.com/docs/10.x/migrations",
            version="10.x"
        )

        # Add more knowledge entries for other Laravel concepts
        # [Additional entries would be added here]
        
        # Filament field conventions
        self.add_entry(
            title="FilamentPHP Field Conventions",
            category="filament",
            content="""
FilamentPHP form fields should follow these conventions:
1. Use descriptive labels that match your UI terminology
2. Group related fields with fieldsets or sections
3. Apply appropriate validation rules
4. Use hints for additional context
5. Configure appropriate field types for data types
6. Use relationships correctly
7. Add help text where needed

Example:
```php
public static function form(Form $form): Form
{
    return $form
        ->schema([
            Forms\\Components\\Section::make('Basic Information')
                ->schema([
                    Forms\\Components\\TextInput::make('title')
                        ->required()
                        ->maxLength(255)
                        ->unique(ignoreRecord: true)
                        ->placeholder('Enter article title')
                        ->columnSpan(2),
                        
                    Forms\\Components\\Select::make('status')
                        ->options([
                            'draft' => 'Draft',
                            'review' => 'Under Review',
                            'published' => 'Published',
                        ])
                        ->default('draft')
                        ->required(),
                        
                    Forms\\Components\\DateTimePicker::make('published_at')
                        ->label('Publish Date')
                        ->nullable(),
                ])
                ->columns(3),
                
            Forms\\Components\\Section::make('Content')
                ->schema([
                    Forms\\Components\\RichEditor::make('content')
                        ->required()
                        ->columnSpan('full'),
                        
                    Forms\\Components\\FileUpload::make('featured_image')
                        ->image()
                        ->directory('articles/images')
                        ->maxSize(2048)
                        ->nullable(),
                ]),
                
            Forms\\Components\\Section::make('SEO')
                ->schema([
                    Forms\\Components\\TextInput::make('meta_title')
                        ->maxLength(100),
                        
                    Forms\\Components\\Textarea::make('meta_description')
                        ->maxLength(160)
                        ->rows(2),
                ])
                ->collapsible(),
                
            Forms\\Components\\BelongsToSelect::make('category_id')
                ->relationship('category', 'name')
                ->searchable()
                ->required(),
                
            Forms\\Components\\BelongsToManyMultiSelect::make('tags')
                ->relationship('tags', 'name')
                ->preload(),
        ]);
}
```
            """,
            tags=["filament", "forms", "fields", "conventions"],
            source="https://filamentphp.com/docs/3.x/forms/fields/getting-started",
            version="3.x"
        )

def load_knowledge_base():
    """Helper function to load the knowledge base from file or create default."""
    try:
        # First try to load from project directory
        kb_path = Path("knowledge_base.json")
        
        # If not found, try to load from module directory
        if not kb_path.exists():
            module_dir = Path(__file__).parent
            kb_path = module_dir / "knowledge_base.json"
        
        # If still not found, create default
        if not kb_path.exists():
            kb = LaravelKnowledgeBase()
            kb.initialize_default_knowledge()
            
            # Save to module directory
            module_dir = Path(__file__).parent
            kb_path = module_dir / "knowledge_base.json"
            kb.save(str(kb_path))
            return kb
            
        return LaravelKnowledgeBase.load(str(kb_path))
    except Exception as e:
        # If any error occurs, return a new knowledge base with default knowledge
        print(f"Error loading knowledge base: {e}")
        kb = LaravelKnowledgeBase()
        kb.initialize_default_knowledge()
        return kb 