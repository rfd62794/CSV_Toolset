# CSV Utils API Reference

## Overview
The `csv_utils.py` module provides utility classes and functions for handling CSV files safely and efficiently. It includes encoding detection, safe file operations, and path management utilities.

## Classes

### CSVHandler

A utility class that provides static methods for safe CSV file operations.

#### Methods

##### `detect_encoding(file_path: str) -> str`
Detects the encoding of a CSV file.

**Parameters:**
- `file_path` (str): Path to the CSV file

**Returns:**
- str: Detected encoding of the file

**Example:**
```python
encoding = CSVHandler.detect_encoding("data.csv")
print(f"File encoding: {encoding}")
```

##### `safe_read_csv(file_path: str, encoding: Optional[str] = None) -> tuple[list, list]`
Safely reads a CSV file with automatic encoding detection if not specified.

**Parameters:**
- `file_path` (str): Path to the CSV file
- `encoding` (Optional[str]): File encoding (if None, will be auto-detected)

**Returns:**
- tuple[list, list]: A tuple containing:
  - header (list): CSV header row
  - data (list): List of data rows

**Example:**
```python
header, data = CSVHandler.safe_read_csv("data.csv")
print(f"Columns: {header}")
print(f"Row count: {len(data)}")
```

##### `safe_write_csv(file_path: str, header: list, data: list, encoding: str = 'utf-8')`
Safely writes data to a CSV file with specified encoding.

**Parameters:**
- `file_path` (str): Output file path
- `header` (list): CSV header row
- `data` (list): List of data rows
- `encoding` (str): File encoding (defaults to 'utf-8')

**Example:**
```python
header = ["Name", "Age"]
data = [["John", "30"], ["Jane", "25"]]
CSVHandler.safe_write_csv("output.csv", header, data)
```

### FileManager

A utility class for managing file paths and operations.

#### Methods

##### `generate_output_path(input_path: str, suffix: str) -> str`
Generates an output file path by adding a suffix to the original filename.

**Parameters:**
- `input_path` (str): Original file path
- `suffix` (str): Suffix to add to the filename

**Returns:**
- str: Generated output file path

**Example:**
```python
output_path = FileManager.generate_output_path("data.csv", "processed")
# Result: "data_processed.csv"
```

## Dependencies
- `chardet`: For encoding detection
- `csv`: Python's built-in CSV handling
- `os`: For file path operations
- `typing`: For type hints

## Best Practices
1. Always use `safe_read_csv` instead of direct file operations to handle encoding correctly
2. Use `generate_output_path` to create consistent output file names
3. Handle potential exceptions when using these utilities
4. Specify encoding explicitly when known to avoid detection overhead

## Error Handling
The utilities include basic error handling, but users should implement additional error handling for:
- File not found errors
- Permission errors
- Encoding errors
- Memory errors with large files

## Performance Considerations
- Encoding detection requires reading the entire file
- For large files, consider streaming operations instead of loading entire file
- Cache encoding information when processing multiple files with same encoding 