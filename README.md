# Laravel Developer Agent

A sophisticated AI agent that simulates an expert Laravel developer using LangChain and LangGraph frameworks.

## Features

- **Technical Laravel Expertise**
  - Building optimal APIs with Laravel best practices
  - Database management (migrations, relations, seeders, factories)
  - FilamentPHP admin panel development and optimization
  - Integration capabilities (payment gateways, email, SMS)
  - Testing with Laravel Pest

- **Analytical and Planning Skills**
  - Requirement analysis and planning
  - Database schema design and optimization
  - API architecture planning
  - Task breakdown and management

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/laravel-developer-agent.git
   cd laravel-developer-agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env-example` and add your Anthropic API key.

## Usage

Run the CLI interface:

```bash
python -m src.cli.main
```

## Project Structure

- `src/` - Source code
  - `agent/` - Agent implementation with LangChain/LangGraph
  - `utils/` - Utility functions and helpers
  - `cli/` - Command-line interface
- `tests/` - Test files
- `docs/` - Documentation

## Development

This project is developed following a task-driven approach using task-master for task management.

## License

MIT 