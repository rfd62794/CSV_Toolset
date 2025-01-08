# CSV Column Splitter

A GUI tool for splitting CSV files into multiple files based on unique values in a selected column.

## Features

- Graphical user interface for easy operation
- Automatic encoding detection
- Progress tracking with visual feedback
- Results summary display
- Detailed logging of operations
- Preserves headers in all output files
- Creates organized output directory

## Usage

1. Launch the tool:
```bash
python stand_alone/csv_column_splitter.py
```

2. Using the Interface:
   - Click "Select CSV File" to choose your input file
   - Select the column to split on from the list
   - Click "Split File" to begin processing
   - Monitor progress and results in the interface

3. Output:
   - Creates a "Split" directory next to input file
   - Generates separate files for each unique value
   - Names files as `original_name_matching_value.csv`
   - Shows summary of rows per value

## Example

```
Input CSV (companies.csv):
Company,SIC_Code,Revenue
Acme Inc,2056,1000000
Beta Corp,2056,2000000
Gamma Ltd,3012,1500000
Delta Co,3012,3000000

Output:
Split/
├── companies_matching_2056.csv  (2 rows + header)
└── companies_matching_3012.csv  (2 rows + header)
```

## Technical Details

### Class Structure

- **CSVFileHandler**: Handles file operations and encoding detection
- **CSVSplitter**: Manages the splitting logic
- **GUI**: Manages the user interface and results display

### Error Handling

The tool handles various scenarios:
- Invalid file encodings
- Missing or malformed columns
- Insufficient disk space
- File access permissions
- Memory management for large files

### Logging

Comprehensive logging with timestamps:
```
2025-01-08 14:42:06 - INFO - GUI initialized
2025-01-08 14:42:09 - INFO - Detecting encoding for file: companies.csv
2025-01-08 14:42:10 - INFO - Created new file for value: 2056
```

## Troubleshooting

### Common Issues

1. **Memory Management**
   - Processes one row at a time
   - Efficient file handling
   - Minimal memory footprint

2. **File Naming**
   - Sanitizes value names for filenames
   - Handles special characters
   - Prevents naming conflicts

3. **Large Files**
   - Shows progress updates
   - Processes in chunks
   - Maintains responsiveness

### Solutions

1. If splitting fails:
   - Check disk space
   - Verify write permissions
   - Monitor memory usage

2. If files are missing:
   - Check log for skipped values
   - Verify column data
   - Check output directory

3. If processing is slow:
   - Close other applications
   - Check system resources
   - Consider file size

## Advanced Usage

### Future Features

1. **Filtering Options**
   - Value-based filtering
   - Regular expression matching
   - Custom output naming

2. **Batch Processing**
   - Multiple file processing
   - Directory monitoring
   - Automated splitting

3. **Data Analysis**
   - Value frequency analysis
   - Data distribution reports
   - Pattern detection

## Integration

The tool can be:
- Used as a standalone application
- Imported as a Python module
- Integrated with data pipelines
- Automated with scripts

## Best Practices

1. **Data Preparation**
   - Clean data before splitting
   - Check for unique values
   - Ensure consistent formatting

2. **Processing**
   - Monitor progress
   - Check log messages
   - Verify output files

3. **Post-Processing**
   - Validate split files
   - Archive results if needed
   - Clean up temporary files

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

## Related Tools

Other tools in the suite that complement this functionality:
- csv_data_truncator.py
- csv_inspector.py
- csv_columnsweep.py 