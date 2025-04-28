"""
Larecipe Documentation Patterns Knowledge Base.

This module provides a knowledge base of common Larecipe documentation patterns
and structures for Laravel applications.
"""

from typing import Dict, List, Any


class LarecipeDocumentationPatterns:
    """Knowledge base for Larecipe documentation patterns."""
    
    @staticmethod
    def get_patterns() -> Dict[str, Any]:
        """
        Get all Larecipe documentation patterns.
        
        Returns:
            Dictionary of documentation patterns categorized by type
        """
        return {
            "page_structure": {
                "basic_page": {
                    "description": "Basic documentation page structure",
                    "pattern": """# {page_title}

{page_description}

---

<a name="section-{section_anchor}"></a>
## {section_title}

{section_content}

<a name="section-{section_anchor_2}"></a>
## {section_title_2}

{section_content_2}""",
                    "when_to_use": "For standard documentation pages with multiple sections"
                },
                "api_page": {
                    "description": "API documentation page structure",
                    "pattern": """# API Reference

{api_description}

---

<a name="section-{endpoint_anchor}"></a>
## {endpoint_name}

{endpoint_description}

<larecipe-badge type="{http_method_color}">{http_method}</larecipe-badge>

```
{endpoint_url}
```

{endpoint_parameters}

### Request
<larecipe-badge type="info">HEADERS</larecipe-badge>

```json
{
{headers}
}
```

<larecipe-badge type="info">BODY</larecipe-badge>

```json
{
{request_body}
}
```

### Response
<larecipe-badge type="success">{response_code}</larecipe-badge>

```json
{
{response_body}
}
```

{example_usage}""",
                    "when_to_use": "For documenting API endpoints with request/response examples"
                },
                "guide_page": {
                    "description": "Step-by-step guide page structure",
                    "pattern": """# {guide_title}

{guide_description}

---

<a name="section-{section_anchor}"></a>
## {section_title}

{section_content}

<a name="section-prerequisites"></a>
## Prerequisites

{prerequisites}

<a name="section-steps"></a>
## Steps

{steps}

<a name="section-conclusion"></a>
## Conclusion

{conclusion}""",
                    "when_to_use": "For creating tutorials and how-to guides"
                }
            },
            "components": {
                "badges": {
                    "description": "Colored badges for visual highlighting",
                    "pattern": """<larecipe-badge type="primary">Primary</larecipe-badge>
<larecipe-badge type="secondary">Secondary</larecipe-badge>
<larecipe-badge type="success">Success</larecipe-badge>
<larecipe-badge type="danger">Danger</larecipe-badge>
<larecipe-badge type="warning">Warning</larecipe-badge>
<larecipe-badge type="info">Info</larecipe-badge>
<larecipe-badge type="light">Light</larecipe-badge>
<larecipe-badge type="dark">Dark</larecipe-badge>""",
                    "when_to_use": "For highlighting important information or statuses"
                },
                "cards": {
                    "description": "Card components for grouping related content",
                    "pattern": """<larecipe-card>
    <larecipe-badge type="success" circle class="mr-3" icon="fa fa-book"></larecipe-badge>
    <div>
        <h3 class="text-primary">{card_title}</h3>
        <p class="text-gray-700">{card_description}</p>
    </div>
    <template slot="footer">
        <a href="{link}" class="text-primary font-bold">Read More &rarr;</a>
    </template>
</larecipe-card>""",
                    "when_to_use": "For creating visually appealing content cards with call-to-actions"
                },
                "tabs": {
                    "description": "Tab components for organizing related content",
                    "pattern": """<larecipe-tabs>
    <larecipe-tab name="{tab_1_name}">
        {tab_1_content}
    </larecipe-tab>
    
    <larecipe-tab name="{tab_2_name}">
        {tab_2_content}
    </larecipe-tab>
    
    <larecipe-tab name="{tab_3_name}">
        {tab_3_content}
    </larecipe-tab>
</larecipe-tabs>""",
                    "when_to_use": "For displaying alternative approaches or examples"
                },
                "accordions": {
                    "description": "Accordion components for collapsible content",
                    "pattern": """<larecipe-accordions>
    <larecipe-accordion name="{accordion_1_title}">
        {accordion_1_content}
    </larecipe-accordion>
    
    <larecipe-accordion name="{accordion_2_title}">
        {accordion_2_content}
    </larecipe-accordion>
</larecipe-accordions>""",
                    "when_to_use": "For FAQ sections or content that can be collapsed"
                },
                "alerts": {
                    "description": "Alert components for important notifications",
                    "pattern": """<larecipe-alert type="primary">
    {alert_content}
</larecipe-alert>

<larecipe-alert type="secondary">
    {alert_content}
</larecipe-alert>

<larecipe-alert type="success">
    {alert_content}
</larecipe-alert>

<larecipe-alert type="danger">
    {alert_content}
</larecipe-alert>

<larecipe-alert type="warning">
    {alert_content}
</larecipe-alert>

<larecipe-alert type="info">
    {alert_content}
</larecipe-alert>

<larecipe-alert type="light">
    {alert_content}
</larecipe-alert>

<larecipe-alert type="dark">
    {alert_content}
</larecipe-alert>""",
                    "when_to_use": "For highlighting important information, warnings, or notices"
                }
            },
            "elements": {
                "code_blocks": {
                    "description": "Code block examples",
                    "pattern": """```php
// PHP code example
public function example()
{
    return 'Hello World';
}
```

```js
// JavaScript code example
function example() {
    return 'Hello World';
}
```

```bash
# Shell command example
php artisan make:model Post --migration
```""",
                    "when_to_use": "For showing code examples in different languages"
                },
                "tables": {
                    "description": "Markdown tables for structured data",
                    "pattern": """| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1    | Value    | Value    |
| Row 2    | Value    | Value    |
| Row 3    | Value    | Value    |""",
                    "when_to_use": "For displaying structured data in a tabular format"
                },
                "lists": {
                    "description": "Ordered and unordered lists",
                    "pattern": """- Unordered list item 1
- Unordered list item 2
  - Nested item 2.1
  - Nested item 2.2
- Unordered list item 3

1. Ordered list item 1
2. Ordered list item 2
   1. Nested item 2.1
   2. Nested item 2.2
3. Ordered list item 3""",
                    "when_to_use": "For sequential steps or itemized information"
                },
                "links": {
                    "description": "Internal and external links",
                    "pattern": """[Link to internal page](/docs/{version}/page)

[Link to section](#section-name)

[Link to external site](https://example.com)""",
                    "when_to_use": "For navigational elements and references"
                },
                "images": {
                    "description": "Image inclusion examples",
                    "pattern": """![Alt text](/storage/docs/{image})

<img src="/storage/docs/{image}" alt="Alt text" class="w-full">""",
                    "when_to_use": "For including screenshots, diagrams, or illustrations"
                }
            },
            "api_documentation": {
                "endpoint_doc": {
                    "description": "API endpoint documentation",
                    "pattern": """<a name="endpoint-{endpoint_anchor}"></a>
### {endpoint_name}

{endpoint_description}

<larecipe-badge type="{http_method_color}">{http_method}</larecipe-badge>

```
{endpoint_url}
```

#### URL Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
{url_parameters}

#### Request Headers

```json
{
{headers}
}
```

#### Request Body

```json
{
{request_body}
}
```

#### Response

<larecipe-badge type="success">{response_code}</larecipe-badge>

```json
{
{response_body}
}
```

#### Example

```php
{example_code}
```""",
                    "when_to_use": "For documenting individual API endpoints"
                },
                "response_codes": {
                    "description": "API response codes documentation",
                    "pattern": """## Response Codes

| Code | Description |
|------|-------------|
| 200  | OK - The request was successful |
| 201  | Created - The resource was created successfully |
| 204  | No Content - The request was successful but returns no content |
| 400  | Bad Request - The request could not be understood or was missing required parameters |
| 401  | Unauthorized - Authentication failed or user does not have permissions |
| 403  | Forbidden - Access denied |
| 404  | Not Found - Resource was not found |
| 422  | Unprocessable Entity - Validation failed |
| 429  | Too Many Requests - Rate limit exceeded |
| 500  | Internal Server Error - Server encountered an error |""",
                    "when_to_use": "For explaining API response status codes"
                },
                "authentication_doc": {
                    "description": "API authentication documentation",
                    "pattern": """## Authentication

{auth_description}

### Obtaining API Tokens

{token_instructions}

### Using API Tokens

Include your API token in the `Authorization` header for all requests:

```
Authorization: Bearer {your_token}
```

### Token Scopes

| Scope | Description |
|-------|-------------|
{scopes}

### Revoking Tokens

{revoke_instructions}""",
                    "when_to_use": "For documenting API authentication methods"
                }
            },
            "configuration": {
                "env_variables": {
                    "description": "Environment variables documentation",
                    "pattern": """## Environment Variables

The following environment variables can be configured in your `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
{variables}

### Example Configuration

```
{example_env}
```""",
                    "when_to_use": "For documenting available environment variables"
                },
                "config_files": {
                    "description": "Configuration files documentation",
                    "pattern": """## Configuration Files

### {config_name}

The `config/{config_file}.php` file contains the following options:

| Option | Type | Description | Default |
|--------|------|-------------|---------|
{options}

### Custom Configuration

{custom_config_instructions}""",
                    "when_to_use": "For documenting application configuration files"
                }
            },
            "navigation": {
                "sidebar": {
                    "description": "Documentation sidebar navigation",
                    "pattern": """- ## Getting Started
  - [Introduction](/docs/{version}/introduction)
  - [Installation](/docs/{version}/installation)
  - [Configuration](/docs/{version}/configuration)
  - [Directory Structure](/docs/{version}/structure)

- ## The Basics
  - [Routing](/docs/{version}/routing)
  - [Middleware](/docs/{version}/middleware)
  - [Controllers](/docs/{version}/controllers)
  - [Requests](/docs/{version}/requests)
  - [Responses](/docs/{version}/responses)
  - [Views](/docs/{version}/views)
  - [Blade Templates](/docs/{version}/blade)

- ## Database
  - [Models](/docs/{version}/models)
  - [Migrations](/docs/{version}/migrations)
  - [Seeders](/docs/{version}/seeders)
  - [Factories](/docs/{version}/factories)
  - [Query Builder](/docs/{version}/queries)
  - [Relationships](/docs/{version}/relationships)

- ## API
  - [Authentication](/docs/{version}/api-auth)
  - [Resources](/docs/{version}/api-resources)
  - [Endpoints](/docs/{version}/api-endpoints)""",
                    "when_to_use": "For creating the main documentation navigation sidebar"
                },
                "versioning": {
                    "description": "Documentation version configuration",
                    "pattern": """<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Documentation Versions
    |--------------------------------------------------------------------------
    |
    | Here you may specify and set the versions and the default (latest) one.
    | Just create a new folder in /resources/docs directory, give it a version number
    | as a name (use numeric values for better sorting) and update the default value.
    */

    'versions' => [
        '1.0',
        '2.0'
    ],

    'default' => '2.0',
];""",
                    "when_to_use": "For configuring multiple documentation versions"
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
        patterns = LarecipeDocumentationPatterns.get_patterns()
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
        return list(LarecipeDocumentationPatterns.get_patterns().keys())
    
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
        patterns = LarecipeDocumentationPatterns.get_patterns()
        
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