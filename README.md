# CSV Toolset

A comprehensive toolkit for CSV file manipulation and analysis, featuring both standalone tools and an integrated framework.

## Project Structure

```
CSV_Toolset/
├── stand_alone/          # Independent CSV processing tools
├── tools/               # Core framework components
├── gui/                 # GUI components for the framework
├── config/             # Configuration files
├── tests/              # Test suite
└── requirements.txt    # Python dependencies
```

## Features

### Standalone Tools

Located in `stand_alone/`, these are independent tools that can be run without the main framework:

- **csv_data_truncator.py**: Truncates data in specified columns to a given length
- **csv_column_splitter.py**: Splits CSV files based on unique values in a column
- **csv_inspector.py**: Analyzes and displays CSV file structure and content
- **csv_columnsweep.py**: Removes rows with missing data in selected columns
- **csv_order_reverse.py**: Reverses row or column order in CSV files
- **phoneColumnExtract.py**: Extracts and formats phone numbers from columns
- **sample_maker.py**: Creates sample datasets from larger CSV files
- **adapt_reformat.py**: Reformats CSV files to match specific requirements
- **csv_append_column_filler_data.py**: Fills empty columns with specified data
- **csv_inspector_gadget.py**: Advanced CSV analysis and validation tool

### Framework Components

The integrated framework provides a more comprehensive solution:

- **csv_toolkit.py**: Main framework entry point
- **csv_utils.py**: Common utilities for CSV processing
- **app.py**: Application launcher

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd CSV_Toolset
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Standalone Tools

Each tool in the `stand_alone` directory can be run independently:

```bash
python stand_alone/csv_data_truncator.py
python stand_alone/csv_column_splitter.py
# etc...
```

These tools provide GUI interfaces for:
- File selection
- Column selection
- Processing options
- Progress tracking
- Results display

### Framework Usage

The main framework can be launched using:

```bash
python app.py
```

## Development

### Project Organization

- **stand_alone/**: Independent tools with their own GUIs
- **tools/**: Core processing modules and utilities
- **gui/**: Framework GUI components
- **config/**: Configuration files and settings
- **tests/**: Test suite and test data

### Code Style

- Follows PEP 8 guidelines
- Uses type hints
- Implements SOLID principles
- Includes comprehensive error handling
- Features detailed logging

### Adding New Tools

1. Standalone Tools:
   - Create new Python file in `stand_alone/`
   - Follow existing tool patterns for consistency
   - Include GUI components for user interaction
   - Add error handling and logging

2. Framework Components:
   - Add new modules to appropriate directories
   - Update framework interfaces as needed
   - Include tests in `tests/` directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Dependencies

Core dependencies (see `requirements.txt`):
- Python 3.x
- tkinter (for GUI components)
- chardet (for encoding detection)

## License

[Your License Here]

## Contact

[Your Contact Information] 