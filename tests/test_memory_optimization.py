"""
Test Memory Optimization

This script tests the memory optimization components to verify they work correctly
and provide the expected token savings.
"""

import sys
import os
import time
import json
from datetime import datetime

# Add the parent directory to the Python path to make imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.memory.optimized_memory import OptimizedMemorySystem
from src.memory.dual_memory import DualMemorySystem
from src.memory.memory_search import MemorySearchEngine
from src.memory.relevance_scoring import RelevanceScorer
from src.memory.memory_compression import MemoryCompressor

def test_memory_optimization():
    """Test memory optimization components and measure performance."""
    print("\n=== Testing Memory Optimization System ===\n")
    
    # Initialize the optimized memory system
    print("Initializing system...")
    memory_system = OptimizedMemorySystem(
        auto_compress=True,
        compression_threshold=500,  # Lower threshold for testing
        enable_analytics=True
    )
    
    # Add some test messages
    print("\nAdding test messages...")
    
    # Short message
    memory_system.add_message({
        "role": "user",
        "content": "What's the best way to handle Laravel validation?",
        "id": "msg1",
        "timestamp": datetime.now().isoformat()
    })
    
    # Medium message
    memory_system.add_message({
        "role": "assistant",
        "content": """Laravel provides several ways to validate incoming data. 
        
        1. Controller Validation: You can use the validate() method in your controller to quickly validate incoming requests.
        
        ```php
        public function store(Request $request)
        {
            $validated = $request->validate([
                'title' => 'required|string|max:255',
                'body' => 'required',
                'publish_at' => 'nullable|date',
            ]);
            
            // The validated data is now available
        }
        ```
        
        2. Form Request Validation: For more complex validation scenarios, you can create dedicated Form Request classes.
        
        ```php
        php artisan make:request StorePostRequest
        ```
        
        3. Manual Validation: You can also create a Validator instance manually.
        
        Choose the approach based on your specific needs and the complexity of the validation rules.""",
        "id": "msg2",
        "timestamp": datetime.now().isoformat()
    })
    
    # Long message (should trigger compression in permanent memory)
    memory_system.add_message({
        "role": "user",
        "content": "I'm trying to implement a complex database schema with Laravel for a blog system. I need to have users, posts, categories, tags, and comments. Can you help me design this and provide migration files?",
        "id": "msg3",
        "timestamp": datetime.now().isoformat()
    })
    
    memory_system.add_message({
        "role": "assistant",
        "content": """# Laravel Blog System Database Schema

Here's a comprehensive database schema design for a blog system with migrations and model relationships:

## Database Schema Overview

1. **Users Table**: Store user information
2. **Posts Table**: Store blog posts
3. **Categories Table**: Store post categories 
4. **Tags Table**: Store post tags
5. **Comments Table**: Store post comments
6. **Post_Tag Table**: Many-to-many relationship between posts and tags
7. **Post_Category Table**: Many-to-many relationship between posts and categories

## Migration Files

Let's create the migration files for each table:

### Users Table
```php
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email')->unique();
    $table->timestamp('email_verified_at')->nullable();
    $table->string('password');
    $table->boolean('is_admin')->default(false);
    $table->rememberToken();
    $table->timestamps();
});
```

### Posts Table
```php
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->string('title');
    $table->string('slug')->unique();
    $table->text('excerpt')->nullable();
    $table->longText('content');
    $table->string('featured_image')->nullable();
    $table->enum('status', ['draft', 'published'])->default('draft');
    $table->timestamp('published_at')->nullable();
    $table->timestamps();
});
```

### Categories Table
```php
Schema::create('categories', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('slug')->unique();
    $table->text('description')->nullable();
    $table->timestamps();
});
```

### Tags Table
```php
Schema::create('tags', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('slug')->unique();
    $table->timestamps();
});
```

### Comments Table
```php
Schema::create('comments', function (Blueprint $table) {
    $table->id();
    $table->foreignId('post_id')->constrained()->onDelete('cascade');
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->foreignId('parent_id')->nullable()->constrained('comments')->onDelete('cascade');
    $table->text('content');
    $table->boolean('is_approved')->default(false);
    $table->timestamps();
});
```

### Post_Tag Pivot Table
```php
Schema::create('post_tag', function (Blueprint $table) {
    $table->id();
    $table->foreignId('post_id')->constrained()->onDelete('cascade');
    $table->foreignId('tag_id')->constrained()->onDelete('cascade');
    $table->timestamps();
});
```

### Post_Category Pivot Table
```php
Schema::create('category_post', function (Blueprint $table) {
    $table->id();
    $table->foreignId('post_id')->constrained()->onDelete('cascade');
    $table->foreignId('category_id')->constrained()->onDelete('cascade');
    $table->timestamps();
});
```

## Model Relationships

### User Model
```php
class User extends Authenticatable
{
    // Relations
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
    
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

### Post Model
```php
class Post extends Model
{
    // Relations
    public function user()
    {
        return $this->belongsTo(User::class);
    }
    
    public function categories()
    {
        return $this->belongsToMany(Category::class);
    }
    
    public function tags()
    {
        return $this->belongsToMany(Tag::class);
    }
    
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

### Category Model
```php
class Category extends Model
{
    // Relations
    public function posts()
    {
        return $this->belongsToMany(Post::class);
    }
}
```

### Tag Model
```php
class Tag extends Model
{
    // Relations
    public function posts()
    {
        return $this->belongsToMany(Post::class);
    }
}
```

### Comment Model
```php
class Comment extends Model
{
    // Relations
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
    
    public function user()
    {
        return $this->belongsTo(User::class);
    }
    
    public function replies()
    {
        return $this->hasMany(Comment::class, 'parent_id');
    }
    
    public function parent()
    {
        return $this->belongsTo(Comment::class, 'parent_id');
    }
}
```

This schema provides a solid foundation for a blog system with all the essential features. You can run these migrations and set up your models as shown. The relationships are defined to make querying data efficient and intuitive.

Would you like me to elaborate on any specific part of this schema design?""",
        "id": "msg4",
        "timestamp": datetime.now().isoformat()
    })
    
    # Analyze and extract knowledge
    print("\nAnalyzing temporary memory to extract knowledge...")
    knowledge_entries = memory_system.analyze_and_extract_knowledge()
    print(f"Extracted {len(knowledge_entries)} knowledge entries")
    
    # Store knowledge in permanent memory
    print("\nStoring knowledge in permanent memory...")
    memory_system.store_knowledge(knowledge_entries)
    
    # Test search functionality
    print("\nTesting search functionality...")
    search_queries = [
        "Laravel validation",
        "blog database schema",
        "pivot tables",
        "model relationships"
    ]
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        start_time = time.time()
        results = memory_system.search_memory(query, max_results=2)
        elapsed_ms = (time.time() - start_time) * 1000
        
        print(f"Found {len(results)} results in {elapsed_ms:.2f}ms")
        for i, result in enumerate(results):
            confidence = result.get('confidence', 'unknown')
            score = result.get('final_score', 0.0)
            source = result.get('source', 'unknown')
            
            print(f"Result {i+1}: Confidence: {confidence}, Score: {score:.2f}, Source: {source}")
            
            # Show snippet of content
            content = result.get('content', '')
            snippet = content[:100] + "..." if len(content) > 100 else content
            print(f"Snippet: {snippet}")
    
    # Search again to test caching
    print("\nTesting search caching...")
    for query in search_queries[:2]:  # Rerun first two queries to test cache
        print(f"\nSearching again for: '{query}'")
        start_time = time.time()
        results = memory_system.search_memory(query, max_results=2)
        elapsed_ms = (time.time() - start_time) * 1000
        
        print(f"Found {len(results)} results in {elapsed_ms:.2f}ms (should be faster if cached)")
    
    # Test optimization of all permanent memory
    print("\nOptimizing all permanent memory...")
    optimization_stats = memory_system.optimize_all_permanent_memory()
    
    # Display optimization stats
    print("\n=== Optimization Statistics ===")
    stats = memory_system.get_optimization_stats()
    print(f"Estimated tokens saved: {stats['token_usage']['estimated_tokens_saved']:.2f}")
    print(f"Cache hit rate: {stats['search_engine']['cache_hit_rate']:.2f}")
    
    print("\nCompression stats:")
    for key, value in stats['compression'].items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    print("\nPerformance (average times in ms):")
    for key, value in stats['performance'].items():
        print(f"  {key}: {value:.2f}")
    
    # Save and load test
    print("\nTesting save and load functionality...")
    save_path = os.path.join(os.path.dirname(__file__), "test_optimized_memory.json")
    
    print(f"Saving memory state to {save_path}")
    memory_system.save_memory_state(save_path)
    
    print("Loading memory state")
    new_memory_system = OptimizedMemorySystem()
    new_memory_system.load_memory_state(save_path)
    
    # Verify loaded system works
    print("\nVerifying loaded system...")
    verification_results = new_memory_system.search_memory("database schema", max_results=1)
    if verification_results:
        print("Load successful: Search returned results from loaded memory")
    else:
        print("Load may have failed: No search results returned")
    
    print("\n=== Memory Optimization Test Complete ===")

if __name__ == "__main__":
    test_memory_optimization() 