# Project Structure Documentation

## Current Project Layout

```
fast-api/
├── app/                          # Main FastAPI application
│   ├── api/                      # API endpoints
│   ├── models/                   # Data models
│   ├── routers/                  # Route handlers
│   ├── observability/            # Logging and monitoring
│   ├── config.py                 # Application configuration
│   └── main.py                   # Application entry point
│
├── fastapi-mastery/              # Learning framework (NEW)
│   ├── 01-fundamentals/          # Basic concepts and async programming
│   ├── 02-architecture/          # Design patterns and architecture
│   ├── 03-performance/           # Performance optimization
│   ├── 04-security/              # Security best practices
│   ├── 05-integrations/          # External system integrations
│   ├── 06-deployment/            # Deployment and DevOps
│   ├── 07-advanced-patterns/     # Advanced development patterns
│   ├── 08-real-world/            # Real-world scenarios
│   ├── templates/                # Reusable project templates
│   ├── claude-skills/            # Claude Code skills for automation
│   └── MASTER_PLAN.md            # Complete learning roadmap
│
├── tests/                        # Test files
├── docs/                         # Documentation
├── examples/                     # Code examples
├── benchmarks/                   # Performance benchmarks
├── logs/                         # Application logs
├── frontend/                     # Frontend assets (static)
│
├── pyproject.toml                # Project dependencies
├── CLAUDE.md                     # Claude Code guidance
└── README.md                     # Project overview
```

## Directory Purposes

### Core Application (`app/`)
- Production FastAPI application
- Observability and logging system
- JSON performance optimization examples
- Todo API implementation

### Learning Framework (`fastapi-mastery/`)
- Comprehensive FastAPI learning materials
- Progressive skill development from basics to advanced
- Reusable templates for different project types
- AI-powered development tools

### Supporting Directories
- `tests/`: Application and framework tests
- `docs/`: Technical documentation
- `examples/`: Standalone examples and demos
- `benchmarks/`: Performance measurement tools

## Branch Strategy

### Main Branches
- `main`: Stable, production-ready code
- `develop`: Integration branch for new features

### Feature Branches
- `feature/fastapi-mastery-framework`: Learning framework development
- `feature/performance-optimization`: Performance-related improvements
- `feature/security-enhancements`: Security features
- `hotfix/*`: Critical bug fixes

### Naming Conventions
- Feature branches: `feature/short-description`
- Bug fixes: `fix/issue-description`
- Hotfixes: `hotfix/critical-issue`
- Experimental: `experiment/feature-name`

## Development Workflow

1. **Feature Development**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/new-feature
   # ... develop feature
   git push origin feature/new-feature
   # Create PR to develop
   ```

2. **Release Process**
   ```bash
   git checkout main
   git merge develop
   git tag v1.0.0
   git push origin main --tags
   ```

3. **Hotfixes**
   ```bash
   git checkout main
   git checkout -b hotfix/critical-fix
   # ... fix issue
   git checkout main && git merge hotfix/critical-fix
   git checkout develop && git merge hotfix/critical-fix
   ```

## File Organization Principles

1. **Separation of Concerns**: Each directory has a specific purpose
2. **Progressive Complexity**: Learning materials go from basic to advanced
3. **Reusability**: Templates and examples for quick project bootstrap
4. **Documentation**: Every major component has its own README
5. **Automation**: Claude skills for repetitive development tasks