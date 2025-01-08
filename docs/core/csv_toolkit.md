# CSV Toolkit Core Documentation

## Overview
The `csv_toolkit.py` module implements the main GUI application for CSV manipulation and analysis. It provides a comprehensive set of tools organized into categories for different CSV processing tasks.

## Class: CSVToolkit

### Description
The `CSVToolkit` class is the main application class that inherits from `tk.Tk`. It provides a graphical interface for accessing various CSV manipulation tools.

### Core Features

#### Tool Categories
1. **Analysis Tools**
   - CSV Inspector: Examine CSV file structure and contents
   - Data Profiler: Generate statistical profiles of data

2. **Data Cleaning Tools**
   - Column Sweeper: Clean and standardize column data
   - Phone Formatter: Format and validate phone numbers
   - Data Validator: Validate data quality and consistency

3. **Data Manipulation Tools**
   - Sample Maker: Create data samples
   - Order Reverser: Reverse row order
   - Column Appender: Add columns to CSV files
   - CSV Merger: Combine multiple CSV files
   - CSV Splitter: Split CSV into multiple files
   - Data Transformer: Transform column values
   - Data Filter: Filter rows based on conditions
   - Column Manager: Manage and organize columns

4. **Data Formatting Tools**
   - Data Reformatter: Reformat CSV files with different options

### Key Components

#### Tool Manager
- Manages registration and organization of tools
- Handles tool categorization and accessibility
- Provides tool discovery and filtering capabilities

#### User Interface Elements
1. **Main Container**
   - Tool selection frame with categorized tabs
   - Tool display area for active tool
   - Search functionality for quick tool access

2. **Toolbar**
   - Test runner integration
   - Results display and management
   - Tool-specific controls

3. **Menu System**
   - File operations
   - Tool management
   - Help and documentation access

### Testing Integration
- Built-in test runner functionality
- Test results tracking and display
- Historical test data management

### Usage Example
```python
if __name__ == "__main__":
    app = CSVToolkit()
    app.mainloop()
```

## Architecture

### Tool Registration System
Tools are registered using the `register_tools()` method, which organizes them into categories:
```python
def register_tools(self):
    # Analysis tools
    self.tool_manager.register_tool(InspectorFrame, "Analysis")
    self.tool_manager.register_tool(ProfilerFrame, "Analysis")
    # ... other tool registrations
```

### Tool Management
Each tool is managed through the `ToolManager` class, which handles:
- Tool registration and categorization
- Tool instantiation and lifecycle
- Tool discovery and filtering

### Error Handling
The application implements comprehensive error handling:
- Initialization error catching and reporting
- Tool loading error management
- Runtime error handling with user feedback

## Extension Points
1. **New Tool Integration**
   - Create a new tool frame class
   - Register it with appropriate category
   - Implement required interfaces

2. **Category Extension**
   - Add new category in categories dictionary
   - Define category metadata
   - Register tools in the category

## Best Practices
1. Tool Development
   - Follow consistent frame structure
   - Implement error handling
   - Provide user feedback
   - Include tool documentation

2. UI Customization
   - Use consistent styling
   - Follow accessibility guidelines
   - Maintain responsive design

## Related Components
- `tools/utils/tool_manager.py`: Tool management system
- `tools/frames/*`: Individual tool implementations
- `tools/test_runner.py`: Testing infrastructure 