# Tool Preferences System

## Overview
The tool preferences system allows users to customize which tools are visible in the main menu. It provides a first-run experience and persistent storage of user preferences.

## Key Components

### 1. Preferences Dialog (`tools/preferences_dialog.py`)
```python
from tools.preferences_dialog import ToolPreferencesDialog

# Show dialog
dialog = ToolPreferencesDialog(parent, categories, current_preferences)
```

Features:
- Category-based organization
- Tool descriptions and tooltips
- Select All/None functionality
- Scrollable interface
- Persistent storage

### 2. App Integration (`app.py`)
```python
class CSVToolkitApp(CSVToolkit):
    def __init__(self):
        super().__init__()
        self.preferences = ToolPreferencesDialog.load_preferences()
        if self.preferences is None:
            self.show_preferences_dialog()
```

### 3. Storage Location
Preferences are stored in:
```
~/.csv_toolkit/preferences.json
```

Format:
```json
{
    "CSV Inspector": true,
    "Data Profiler": true,
    "Column Sweeper": false
    // ... other tools
}
```

## Usage

### 1. First Run
- Dialog shows automatically
- All tools enabled by default
- User selects desired tools
- Preferences saved on Save

### 2. Accessing Preferences
- Tools menu -> Tool Preferences
- Keyboard: Ctrl+,
- Changes apply immediately

### 3. Tool Categories
- Analysis Tools (📊)
- Data Cleaning Tools (🧹)
- Data Manipulation Tools (🔧)
- Data Formatting Tools (📝)

## Development

### 1. Adding New Tools
```python
# In csv_toolkit.py
self.categories["New Category"] = {
    "desc": "Category description",
    "icon": "🔧",
    "tools": {
        "New Tool": "Tool description"
    }
}
```

### 2. Handling Preferences
```python
# Load preferences
prefs = ToolPreferencesDialog.load_preferences()

# Save preferences
ToolPreferencesDialog.save_preferences(prefs)

# Check tool visibility
is_visible = prefs.get("Tool Name", True)  # Default to True
```

### 3. Error Handling
- File not found -> Create new
- Invalid JSON -> Reset to defaults
- Missing tools -> Use defaults
- Permission errors -> Show error dialog

## Best Practices

### 1. Tool Organization
- Group related tools
- Clear descriptions
- Meaningful icons
- Logical categories

### 2. User Experience
- Immediate feedback
- Clear descriptions
- Easy navigation
- Keyboard shortcuts

### 3. Performance
- Lazy loading
- Efficient storage
- Quick updates
- Minimal redraws 