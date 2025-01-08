# Configuration System Documentation

## Overview
The CSV Toolkit uses a JSON-based configuration system that allows customization of tool behavior and application settings. Each tool can have its own configuration file, and there's a central application configuration for global settings.

## Configuration Structure

### Directory Layout
```
config/
├── data_profiler.json    # Data Profiler tool configuration
├── data_sampler.json     # Data Sampling tool configuration
├── phone_formatter.json  # Phone Formatting tool configuration
└── data_sweeper.json    # Data Sweeper tool configuration
```

### Configuration File Format
All configuration files use JSON format for consistency and ease of use.

Example (`data_profiler.json`):
```json
{
    "show_stats": true,
    "show_distribution": true,
    "show_correlations": true,
    "sample_size": 1000
}
```

## Tool Configurations

### 1. Data Profiler
**File:** `config/data_profiler.json`
```json
{
    "show_stats": true,        // Show statistical analysis
    "show_distribution": true, // Show data distribution graphs
    "show_correlations": true, // Show correlation matrices
    "sample_size": 1000       // Maximum sample size for analysis
}
```

### 2. Data Sampler
**File:** `config/data_sampler.json`
```json
{
    "default_size": 100,     // Default sample size
    "random_seed": 42,       // Random seed for reproducibility
    "stratify": false        // Enable stratified sampling
}
```

### 3. Phone Formatter
**File:** `config/phone_formatter.json`
```json
{
    "default_format": "E.164",  // Default phone number format
    "validate_numbers": true,   // Enable number validation
    "region_code": "US"         // Default region code
}
```

### 4. Data Sweeper
**File:** `config/data_sweeper.json`
```json
{
    "trim_whitespace": true,    // Remove leading/trailing whitespace
    "remove_duplicates": true,  // Remove duplicate rows
    "case_sensitive": false,    // Case-sensitive comparison
    "null_values": ["", "NA", "NULL"]  // Values to treat as null
}
```

## Usage

### 1. Loading Configuration
```python
import json
from pathlib import Path

def load_tool_config(tool_name: str) -> dict:
    config_path = Path("config") / f"{tool_name}.json"
    with open(config_path, 'r') as f:
        return json.load(f)

# Usage
config = load_tool_config("data_profiler")
```

### 2. Applying Configuration
```python
class Tool:
    def __init__(self):
        self.config = self.load_config()
        self.apply_config()
    
    def load_config(self):
        return load_tool_config(self.tool_name)
    
    def apply_config(self):
        for key, value in self.config.items():
            setattr(self, key, value)
```

### 3. Configuration Validation
```python
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ConfigSchema:
    required_fields: Dict[str, type]
    optional_fields: Dict[str, tuple[type, Any]]

def validate_config(config: dict, schema: ConfigSchema) -> bool:
    # Check required fields
    for field, field_type in schema.required_fields.items():
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(config[field], field_type):
            raise TypeError(f"Invalid type for {field}")
    
    # Check optional fields
    for field, (field_type, default) in schema.optional_fields.items():
        if field in config and not isinstance(config[field], field_type):
            raise TypeError(f"Invalid type for {field}")
    
    return True
```

## Best Practices

### 1. Configuration Management
- Keep configuration files in version control
- Use environment variables for sensitive data
- Document all configuration options
- Provide default values for optional settings

### 2. Configuration Loading
- Implement graceful fallbacks
- Validate configuration on load
- Cache configuration when appropriate
- Handle missing files gracefully

### 3. Configuration Updates
- Implement hot reload capability
- Validate before applying changes
- Log configuration changes
- Maintain backward compatibility

## Error Handling

### 1. Missing Configuration
```python
def get_config(tool_name: str) -> dict:
    try:
        return load_tool_config(tool_name)
    except FileNotFoundError:
        logging.warning(f"Config not found for {tool_name}, using defaults")
        return get_default_config(tool_name)
```

### 2. Invalid Configuration
```python
def apply_config(config: dict) -> None:
    try:
        validate_config(config, CONFIG_SCHEMA)
        apply_validated_config(config)
    except (ValueError, TypeError) as e:
        logging.error(f"Invalid configuration: {e}")
        apply_default_config()
```

## Configuration Migration

### 1. Version Management
```json
{
    "version": "1.0.0",
    "settings": {
        // Tool-specific settings
    }
}
```

### 2. Migration Function
```python
def migrate_config(config: dict) -> dict:
    current_version = config.get("version", "0.0.0")
    if current_version < LATEST_VERSION:
        return perform_migration(config, current_version)
    return config
```

## Security Considerations
1. Don't store sensitive data in configuration files
2. Use appropriate file permissions
3. Validate all configuration inputs
4. Sanitize configuration values before use
5. Implement access controls for configuration changes 