# Contributing to CSV Toolset

Thank you for your interest in contributing to CSV Toolset! This document provides guidelines and standards for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### 1. Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/CSV_Toolset.git
cd CSV_Toolset

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests:
   ```bash
   python -m pytest
   ```
4. Update documentation if needed

### 3. Submitting Changes

1. Push your changes to your fork
2. Submit a pull request using our template
3. Wait for review and address any feedback

## Code Style Guide

### Python Style Standards

1. Follow PEP 8 with these specifics:
   - 4 spaces for indentation
   - 88 characters max line length
   - Use type hints for function parameters and return values
   - Use docstrings for all public functions, classes, and modules

2. Naming Conventions:
   ```python
   # Classes: PascalCase
   class CsvProcessor:
       
   # Functions and variables: snake_case
   def process_csv_file():
       temp_variable = 0
   
   # Constants: UPPER_CASE
   MAX_FILE_SIZE = 1024
   ```

3. Imports Organization:
   ```python
   # Standard library imports
   import os
   import sys
   from typing import List, Dict
   
   # Third-party imports
   import pandas as pd
   import numpy as np
   
   # Local imports
   from .utils import validate_csv
   ```

### Documentation Standards

1. Docstring Format:
   ```python
   def process_csv(filepath: str, encoding: str = 'utf-8') -> pd.DataFrame:
       """Process a CSV file and return a pandas DataFrame.
       
       Args:
           filepath (str): Path to the CSV file
           encoding (str, optional): File encoding. Defaults to 'utf-8'
           
       Returns:
           pd.DataFrame: Processed data
           
       Raises:
           FileNotFoundError: If file doesn't exist
           ValueError: If file is empty
       """
   ```

2. Comments:
   - Use comments sparingly, prefer self-documenting code
   - Comment complex algorithms and business logic
   - Keep comments up to date with code changes

### Testing Standards

1. Test File Organization:
   ```python
   # test_csv_processor.py
   def test_process_csv_valid_file():
       """Test processing a valid CSV file."""
       
   def test_process_csv_empty_file():
       """Test handling of empty CSV file."""
   ```

2. Test Coverage Requirements:
   - Minimum 80% coverage for new code
   - 100% coverage for critical data processing functions
   - Include edge cases and error conditions

### CSV Processing Guidelines

1. File Handling:
   ```python
   def read_csv(filepath: str) -> pd.DataFrame:
       """Read CSV with proper error handling."""
       try:
           return pd.read_csv(filepath)
       except UnicodeDecodeError:
           # Try different encodings
           return pd.read_csv(filepath, encoding='latin1')
   ```

2. Performance Considerations:
   - Use generators for large file processing
   - Implement progress tracking for long operations
   - Consider memory usage with large datasets

### Error Handling

1. Exception Guidelines:
   ```python
   class CsvToolsetError(Exception):
       """Base exception for CSV Toolset."""
   
   class ValidationError(CsvToolsetError):
       """Raised when CSV validation fails."""
   ```

2. Logging Standards:
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   
   def process_file(filepath: str) -> None:
       logger.info(f"Processing file: {filepath}")
       try:
           # Processing logic
           pass
       except Exception as e:
           logger.error(f"Error processing file: {e}")
           raise
   ```

## Pull Request Guidelines

1. PR Title Format:
   - feat: Add new feature
   - fix: Fix bug
   - docs: Update documentation
   - refactor: Code refactoring
   - test: Add tests

2. PR Description:
   - Clear description of changes
   - Link to related issues
   - Screenshots for UI changes
   - Performance impact notes

## Version Control

1. Commit Message Format:
   ```
   type(scope): Short description
   
   Longer description if needed
   
   Fixes #123
   ```

2. Branch Naming:
   - feature/description
   - bugfix/description
   - docs/description

## Additional Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints Guide (PEP 484)](https://www.python.org/dev/peps/pep-0484/)
- [Documentation Guide](docs/tutorials/development.md)
- [Testing Guide](docs/tutorials/testing.md) 