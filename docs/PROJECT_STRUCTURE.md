# Project Structure

## Overview
CSV Toolkit is organized into a clear, modular structure to make it easy to understand and maintain. This document outlines the organization and key components.

## Directory Structure
```
CSV_Toolkit/
├── docs/                    # Documentation
│   ├── guides/             # User and developer guides
│   ├── api/                # API documentation
│   ├── examples/           # Code examples
│   └── tutorials/          # Step-by-step tutorials
├── tools/                  # Core toolkit modules
│   ├── base/              # Base classes and interfaces
│   ├── processors/        # CSV processing modules
│   ├── utils/             # Utility functions
│   └── widgets/           # GUI components
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── performance/      # Performance tests
├── config/               # Configuration files
├── resources/            # Static resources
└── scripts/              # Development scripts
```

## Key Components

### 1. Documentation (`docs/`)
- `PROJECT_STRUCTURE.md`: This file
- `TASKLIST.md`: Current tasks and progress
- `CHANGELOG.md`: Version history and changes
- `DEVLOG.md`: Development journal
- `MILESTONES.md`: Project goals and milestones
- `guides/`: Detailed documentation
  - `getting_started.md`: Quick start guide
  - `performance_monitoring.md`: Performance guide
  - `preferences.md`: Preferences system guide
  - `tool_development.md`: Tool creation guide

### 2. Core Tools (`tools/`)
- Base classes and interfaces
- CSV processing modules
- Utility functions
- GUI components
- Performance monitoring
- Preferences management

### 3. Testing (`tests/`)
- Unit tests for individual components
- Integration tests for system interaction
- Performance tests and benchmarks
- Test fixtures and utilities

### 4. Configuration (`config/`)
- Default settings
- Performance thresholds
- Logging configuration
- Development settings

## Development Workflow

### 1. Documentation Updates
- Update DEVLOG.md for all changes
- Keep CHANGELOG.md current
- Update TASKLIST.md for new tasks
- Review MILESTONES.md progress

### 2. Code Changes
- Follow modular design
- Update relevant tests
- Add documentation
- Update performance metrics

### 3. Testing
- Run unit tests
- Verify integration
- Check performance
- Update test documentation

## Best Practices

### 1. Code Organization
- Keep modules focused
- Use clear naming
- Follow PEP 8
- Document interfaces

### 2. Documentation
- Keep docs current
- Include examples
- Add API references
- Update guides

### 3. Testing
- Write tests first
- Cover edge cases
- Monitor performance
- Document test cases

## Getting Started
1. Review `docs/guides/getting_started.md`
2. Check current tasks in `TASKLIST.md`
3. Read development log in `DEVLOG.md`
4. Review milestones in `MILESTONES.md`

## Contributing
1. Check `TASKLIST.md` for current needs
2. Follow development workflow
3. Update documentation
4. Add tests
5. Submit changes 