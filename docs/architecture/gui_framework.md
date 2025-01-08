# GUI Framework Architecture

## Overview
The CSV Toolkit GUI framework provides a modular, extensible architecture for building and managing the application's graphical interface. It uses tkinter as the underlying GUI toolkit and implements a component-based design pattern.

## Core Components

### 1. Main Window (`CSVToolkitWindow`)
The main application window class that inherits from `tk.Tk` and serves as the root container for all GUI elements.

```python
class CSVToolkitWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Toolkit")
        self.geometry("800x600")
```

#### Key Features
- Tool registry management
- Layout organization
- Event handling
- Component lifecycle management

### 2. Layout Structure
```
CSVToolkitWindow
├── MainContainer (ttk.Frame)
│   ├── Sidebar (ttk.Frame)
│   │   ├── Title Label
│   │   └── Tool Buttons
│   └── Content Area (ttk.Frame)
│       └── Active Tool / Welcome Screen
```

## Tool Integration

### 1. Tool Registry
Tools are registered in a central registry that maps tool names to their frame classes:
```python
self.tools = {
    "CSV Inspector": InspectorFrame,
    "Column Sweeper": SweeperFrame,
    "Order Reverser": ReverserFrame,
    # ... other tools
}
```

### 2. Tool Frame Base Class
All tool frames should inherit from a common base class:
```python
class ToolFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        
    def setup_ui(self):
        """Implement tool-specific UI setup"""
        raise NotImplementedError
        
    def process_data(self):
        """Implement tool-specific data processing"""
        raise NotImplementedError
```

### 3. Tool Integration Example
```python
class CustomToolFrame(ToolFrame):
    def setup_ui(self):
        # Create tool-specific widgets
        self.input_frame = ttk.LabelFrame(self, text="Input")
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add tool controls
        self.process_button = ttk.Button(
            self,
            text="Process",
            command=self.process_data
        )
        self.process_button.pack()
```

## Component Architecture

### 1. UI Components
- **Sidebar**: Tool selection and navigation
- **Content Area**: Active tool display
- **Welcome Screen**: Initial application view
- **Tool Frames**: Individual tool interfaces

### 2. Event System
```python
def show_tool(self, tool_class):
    """Tool switching event handler"""
    # Clear current content
    for widget in self.content.winfo_children():
        widget.destroy()
        
    # Create and show new tool
    tool = tool_class(self.content)
    tool.pack(fill=tk.BOTH, expand=True)
```

### 3. Layout Management
```python
def setup_ui(self):
    """Main UI layout setup"""
    # Create main container
    self.main_container = ttk.Frame(self)
    self.main_container.pack(fill=tk.BOTH, expand=True)
    
    # Create layout components
    self.create_sidebar()
    self.create_content_area()
```

## Extension Points

### 1. Adding New Tools
1. Create tool frame class
2. Register in tool registry
3. Implement required interfaces

Example:
```python
# 1. Create tool frame
class NewToolFrame(ToolFrame):
    def setup_ui(self):
        # Tool UI implementation
        pass
        
    def process_data(self):
        # Tool logic implementation
        pass

# 2. Register tool
self.tools["New Tool"] = NewToolFrame
```

### 2. Customizing Layout
```python
def customize_layout(self):
    # Override default styles
    style = ttk.Style()
    style.configure("Tool.TFrame", padding=10)
    
    # Add custom widgets
    self.status_bar = ttk.Frame(self)
    self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
```

### 3. Adding Features
```python
def add_toolbar(self):
    """Add custom toolbar"""
    toolbar = ttk.Frame(self.main_container)
    toolbar.pack(fill=tk.X, before=self.content)
    
    # Add toolbar buttons
    ttk.Button(toolbar, text="New").pack(side=tk.LEFT)
    ttk.Button(toolbar, text="Save").pack(side=tk.LEFT)
```

## Best Practices

### 1. Tool Development
- Follow consistent naming conventions
- Implement error handling
- Provide user feedback
- Use appropriate widget types
- Follow tkinter best practices

### 2. Layout Guidelines
- Use appropriate geometry managers
- Maintain consistent spacing
- Follow platform guidelines
- Support window resizing
- Consider accessibility

### 3. Event Handling
- Use appropriate event bindings
- Implement proper cleanup
- Handle concurrent operations
- Provide user feedback
- Maintain responsiveness

## Performance Considerations

### 1. Widget Creation
- Create widgets on demand
- Destroy unused widgets
- Use widget pooling for frequent updates
- Minimize widget hierarchy depth

### 2. Event Processing
- Use debouncing for frequent events
- Implement background processing
- Update UI efficiently
- Handle large datasets appropriately

### 3. Memory Management
- Clean up resources properly
- Implement proper widget destruction
- Handle large data efficiently
- Use appropriate data structures

## Testing

### 1. Unit Testing
```python
def test_tool_creation():
    root = tk.Tk()
    tool = CustomToolFrame(root)
    assert isinstance(tool, ToolFrame)
    assert len(tool.winfo_children()) > 0
```

### 2. Integration Testing
```python
def test_tool_switching():
    app = CSVToolkitWindow()
    app.show_tool(CustomToolFrame)
    assert isinstance(
        app.content.winfo_children()[0],
        CustomToolFrame
    )
```

## Error Handling

### 1. Widget Errors
```python
def create_widget(self):
    try:
        # Widget creation code
        pass
    except tk.TclError as e:
        logging.error(f"Widget creation failed: {e}")
        self.show_error_message()
```

### 2. Tool Loading Errors
```python
def show_tool(self, tool_class):
    try:
        tool = tool_class(self.content)
        tool.pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        self.show_error_dialog(
            f"Failed to load tool: {str(e)}"
        )
``` 