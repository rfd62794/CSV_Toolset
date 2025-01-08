# Contributing to CSV Toolset

Thank you for your interest in contributing to CSV Toolset! This document provides guidelines and instructions for contributing.

## Development Environment Setup

1. Fork and clone the repository:
```bash
git clone [your-fork-url]
cd CSV_Toolset
```

2. Set up Python virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Code Style Guidelines

### Python Standards
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for all classes and functions

### Example Function Style
```python
def process_csv_data(
    input_file: str,
    column_index: int,
    encoding: Optional[str] = None
) -> bool:
    """
    Process CSV data with specified parameters.

    Args:
        input_file: Path to the input CSV file
        column_index: Index of the column to process
        encoding: File encoding (default: auto-detect)

    Returns:
        bool: True if processing successful, False otherwise

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If column_index is invalid
    """
    # Function implementation
```

### Error Handling
- Use specific exception types
- Include error messages with context
- Log errors appropriately
- Provide user-friendly error messages in GUI

### Logging
- Use the Python logging module
- Include appropriate log levels
- Add context to log messages
- Don't log sensitive information

## Adding New Tools

### Standalone Tools
1. Create new file in `stand_alone/` directory
2. Follow the existing pattern:
   - Class-based structure
   - GUI implementation
   - Error handling
   - Progress tracking
   - Logging

### Framework Components
1. Add new modules to appropriate directories
2. Update interfaces as needed
3. Include unit tests
4. Update documentation

## Testing

### Unit Tests
- Write tests for new functionality
- Place tests in `tests/` directory
- Follow existing test patterns
- Ensure tests are independent

### Running Tests
```bash
python -m pytest tests/
```

## Pull Request Process

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes:
- Follow code style guidelines
- Add tests
- Update documentation

3. Commit your changes:
```bash
git add .
git commit -m "Description of changes"
```

4. Push to your fork:
```bash
git push origin feature/your-feature-name
```

5. Create Pull Request:
- Use clear, descriptive title
- Include detailed description
- Reference any related issues
- Ensure all tests pass
- Request review

## Code Review Process

### What We Look For
- Code style compliance
- Test coverage
- Documentation
- Error handling
- Performance considerations
- Security considerations

### Review Timeline
- Initial review within 1-2 days
- Address feedback promptly
- Final review and merge

## Questions or Problems?

- Open an issue for bugs
- Use discussions for questions
- Tag maintainers for urgent issues

Thank you for contributing to CSV Toolset! 