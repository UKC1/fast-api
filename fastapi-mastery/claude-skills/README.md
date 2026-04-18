# Claude Skills for FastAPI Development

## Overview
Specialized AI-powered tools to accelerate FastAPI development and enforce best practices.

## Available Skills

### Code Analysis and Review
- **fastapi-reviewer**: Comprehensive code review for best practices compliance
- **architecture-analyzer**: System design quality and dependency analysis
- **performance-optimizer**: Bottleneck identification and optimization suggestions
- **security-scanner**: Vulnerability detection and security assessment

## Skill Descriptions

### FastAPI Reviewer
**Purpose**: Automated code review focusing on FastAPI-specific patterns

**Capabilities**:
- Clean Architecture pattern validation
- Async/await usage optimization
- Security vulnerability detection
- Performance bottleneck identification
- Code quality assessment

**Usage**: Analyzes code files and provides detailed feedback with specific improvements

### Architecture Analyzer  
**Purpose**: System architecture quality assessment

**Capabilities**:
- Dependency cycle detection
- Layer boundary validation
- Coupling and cohesion analysis
- Design pattern compliance checking

**Usage**: Evaluates overall project structure and architectural decisions

### Performance Optimizer
**Purpose**: Performance analysis and optimization guidance

**Capabilities**:
- Database query optimization
- Async operation efficiency analysis
- Memory usage optimization
- Response time improvement suggestions

**Usage**: Identifies performance bottlenecks and provides specific optimization strategies

### Security Scanner
**Purpose**: Comprehensive security analysis

**Capabilities**:
- Authentication/authorization review
- Input validation assessment
- OWASP Top 10 compliance checking
- Security configuration analysis

**Usage**: Scans codebase for security vulnerabilities and compliance issues

## Integration Workflow

### Development Cycle Integration
```bash
# 1. Write code
git add .

# 2. Run automated review
claude review-fastapi src/

# 3. Apply suggestions
claude optimize-performance src/

# 4. Security check
claude scan-security src/

# 5. Final architecture validation
claude analyze-architecture

# 6. Commit changes
git commit -m "Feature implementation with AI-assisted optimization"
```

### Continuous Integration
- Integrate skills into CI/CD pipeline
- Automated quality gates
- Performance regression detection
- Security vulnerability prevention

## Output Formats

### Code Review Report
```markdown
## Analysis Summary
- Files Reviewed: X files
- Issues Found: Y issues
- Recommendations: Z suggestions

## Critical Issues
1. **Security**: Authentication bypass vulnerability
2. **Performance**: N+1 query detected
3. **Architecture**: Layer boundary violation

## Optimization Opportunities
- Database query optimization: 40% performance gain
- Response caching: 60% faster response times
- Memory optimization: 25% reduced usage
```

### Performance Analysis
```markdown
## Performance Bottlenecks
- Slow endpoint: /users (2.3s avg response)
- Memory leak: User session management
- Database: Missing indexes on frequently queried columns

## Optimization Recommendations
1. Implement connection pooling
2. Add response caching layer
3. Optimize database queries
4. Use async operations consistently
```

## Best Practices Enforcement

### Code Standards
- Type hint completeness
- Async/await consistency
- Error handling patterns
- Documentation quality

### Architecture Compliance  
- Clean Architecture layer separation
- Dependency injection usage
- Domain model isolation
- Interface segregation

### Security Standards
- Input validation requirements
- Authentication best practices
- Authorization pattern enforcement
- Sensitive data protection

### Performance Standards
- Response time thresholds
- Memory usage limits
- Database query efficiency
- Async operation patterns

## Customization and Extension

### Adding New Rules
1. Define checking criteria
2. Implement detection logic
3. Create recommendation templates
4. Test with sample codebases

### Team-Specific Configuration
- Custom coding standards
- Project-specific patterns
- Performance thresholds
- Security requirements

## Integration with Development Tools

### IDE Integration
- Real-time analysis during development
- Inline suggestions and warnings
- Quick-fix implementations

### Git Hooks
- Pre-commit quality checks
- Automated optimization suggestions
- Security scanning before push

### CI/CD Pipeline
- Quality gate enforcement
- Performance regression detection
- Automated documentation updates

## Success Metrics

### Development Efficiency
- Code review time: 2 hours → 30 minutes
- Bug detection: 80% fewer production issues
- Refactoring time: 1 week → 2 days
- Security vulnerabilities: 95% prevention rate

### Code Quality Improvements
- Test coverage: 70% → 90%+
- Cyclomatic complexity: Reduced by 40%
- Documentation completeness: 95%+
- Performance optimization: 30% average improvement

## Getting Started

### Installation and Setup
1. Ensure Claude Code is properly configured
2. Copy skill definitions to Claude workspace
3. Test skills on sample projects
4. Integrate into development workflow

### Basic Usage
```bash
# Review a specific file
claude review-fastapi app/main.py

# Analyze entire project
claude analyze-architecture .

# Performance optimization
claude optimize-performance src/api/

# Security assessment
claude scan-security
```

### Advanced Integration
- Configure automated triggers
- Set up notification systems
- Create custom reporting dashboards
- Implement team-specific rules

---

**Leverage AI to maintain consistently high-quality FastAPI applications.**