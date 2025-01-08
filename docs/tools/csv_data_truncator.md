# CSV Data Truncator

A GUI tool for truncating data in CSV columns to a specified length while preserving data integrity.

## Features

- Graphical user interface for easy operation
- Automatic encoding detection
- Progress tracking with visual feedback
- Detailed logging of operations
- Error handling with user-friendly messages
- Preserves original CSV headers
- Creates backup of original file

## Usage

1. Launch the tool:
```bash
python stand_alone/csv_data_truncator.py
```

2. Using the Interface:
   - Click "Select CSV File" to choose your input file
   - Select the column to truncate from the list
   - Enter the desired length (default: 4)
   - Click "Process File" to start

3. Output:
   - Creates a new file with "_truncated" suffix
   - Preserves original file
   - Shows progress during processing
   - Displays completion message with output location

## Example

```
Input CSV:
Name,ID,Description
John,12345,Very long description text
Jane,67890,Another long text here

Output CSV (truncated ID to 4):
Name,ID,Description
John,1234,Very long description text
Jane,6789,Another long text here
```

## Technical Details

### Class Structure

- **CSVFileHandler**: Handles file operations and encoding detection
- **DataTruncator**: Manages the truncation logic
- **CSVProcessor**: Coordinates the processing workflow
- **GUI**: Manages the user interface

### Error Handling

The tool handles common issues:
- Invalid file encodings
- Missing columns
- Malformed rows
- File access permissions
- Memory constraints

### Logging

Logs are written to console with timestamps:
```
2025-01-08 14:42:06 - INFO - GUI initialized
2025-01-08 14:42:09 - INFO - Detecting encoding for file: example.csv
2025-01-08 14:42:10 - INFO - Processing column: ID
```

## Troubleshooting

### Common Issues

1. **File Encoding Errors**
   - Tool attempts multiple encodings
   - Logs attempted encodings
   - Shows detailed error message

2. **Memory Issues**
   - Processes files in chunks
   - Minimal memory footprint
   - Suitable for large files

3. **Permission Errors**
   - Checks write permissions
   - Creates output in accessible location
   - Clear error messages

### Solutions

1. If encoding detection fails:
   - Check file encoding manually
   - Try saving file as UTF-8
   - Check for special characters

2. If processing is slow:
   - Check available system memory
   - Close other applications
   - Process smaller chunks

3. If output fails:
   - Check write permissions
   - Verify disk space
   - Try different output location

## Advanced Usage

### Command Line Arguments (Future)

```bash
python csv_data_truncator.py --file input.csv --column ID --length 4
```

### Configuration Options

Future versions will support:
- Custom output directory
- Multiple column processing
- Batch processing
- Custom naming patterns

## Integration

The tool can be:
- Used standalone
- Imported as a module
- Integrated with other tools
- Automated in scripts

## Best Practices

1. **Before Processing**
   - Backup important files
   - Verify input data
   - Check available space

2. **During Processing**
   - Monitor progress
   - Check log messages
   - Don't modify input file

3. **After Processing**
   - Verify output
   - Check log files
   - Archive if needed

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for:
- Code style guidelines
- Testing requirements
- Pull request process
- Development setup 