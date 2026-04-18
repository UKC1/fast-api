# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Start development server with auto-reload
uv run uvicorn app.main:app --reload --port 8080

# Alternative: run directly
python -m uvicorn app.main:app --reload --port 8080
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_json_performance.py

# Run with verbose output
uv run pytest -v
```

### JSON Performance Testing
```bash
# Run JSON performance benchmarks
uv run python tests/test_json_performance.py

# Run benchmark report
uv run python benchmarks/benchmark_report.py

# Run serialization demo
uv run python examples/serialization_demo.py
```

### Installing Dependencies
```bash
# Add a new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Install from pyproject.toml
uv install
```

## Architecture Overview

This is a FastAPI application focused on JSON serialization performance optimization and observability. The project compares different JSON libraries (standard json, orjson, ujson) and includes comprehensive logging.

### Key Components

**Core Application Structure:**
- `app/main.py` - FastAPI application entry point with middleware setup
- `app/config.py` - Environment-based configuration settings
- `app/routers/todos.py` - Todo CRUD API endpoints
- `app/models/todo.py` - Pydantic data models
- `app/api/json_comparison.py` - JSON library performance comparison endpoints

**Observability System:**
- `app/observability/` - Complete monitoring and logging framework
- `app/observability/logger.py` - Structured JSON logging with rotation
- `app/observability/middleware.py` - Request tracking middleware with unique request IDs
- `app/observability/context.py` - Request context management for tracing
- Logs are stored in `logs/` directory with time-based rotation (hourly, 7-day retention)

**Performance Testing:**
- `tests/test_json_performance.py` - Automated performance tests
- `benchmarks/` - Performance benchmarking tools
- `examples/` - Demonstration scripts for optimization techniques

### JSON Library Integration

The application uses orjson as the default JSON serializer for maximum performance. Key files:
- Standard JSON, orjson, and ujson are all supported
- Performance endpoints available at `/json/{library}/{count}`
- Comprehensive comparison endpoint at `/json/compare/{count}`

### Configuration

Environment variables are managed through `app/config.py`:
- `ENV` - Environment (local/dev/prod)
- `LOG_LEVEL` - Logging verbosity
- `API_HOST`/`API_PORT` - Server configuration
- Performance monitoring thresholds are configurable

### Request Tracing

Every request gets a unique `request_id` that flows through:
1. RequestTrackerMiddleware generates UUID for each request
2. Context manager maintains request_id throughout request lifecycle
3. All logs include request_id for end-to-end tracing
4. Performance metrics are automatically captured and logged

### Development Notes

- Uses UV package manager for dependency management
- Korean comments and documentation present in some files (todo tutorial)
- CORS is configured to allow all origins (should be restricted in production)
- Static files are served from `frontend/src` directory
- Pytest configuration is set up with proper Python path