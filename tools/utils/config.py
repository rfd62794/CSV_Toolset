from typing import Dict, Any
from pathlib import Path

class ToolConfig:
    """Central configuration for the application"""
    
    # Progress step percentages
    PROGRESS_STEPS = {
        'READ': 0,
        'VALIDATE': 20,
        'PROCESS': 40,
        'SAVE': 80,
        'COMPLETE': 100
    }
    
    # File settings
    FILE_SETTINGS = {
        'encoding': 'utf-8',
        'chunk_size': 10000,
        'max_file_size': 1024 * 1024 * 100  # 100MB
    }
    
    # UI settings
    UI_SETTINGS = {
        'default_window_size': '800x600',
        'min_window_size': '600x400',
        'button_width': 15,
        'entry_width': 50
    }
    
    # Tool categories
    TOOL_CATEGORIES = {
        'Analysis': ['CSV Inspector'],
        'Data Cleaning': ['Column Sweeper', 'Phone Extractor'],
        'Data Manipulation': ['Sample Maker', 'Order Reverser', 'Column Appender', 'Data Reformatter']
    }
    
    # Reverser-specific settings
    REVERSER_SETTINGS = {
        'preview_rows': 5,
        'chunk_size': 10000,  # For large file processing
        'max_file_size': 1024 * 1024 * 100  # 100MB limit
    }
    
    # Sample-specific settings
    SAMPLE_SETTINGS = {
        'preview_rows': 5,
        'min_sample_size': 1,
        'max_sample_size': 1000000,  # 1M rows max
        'max_file_size': 1024 * 1024 * 200,  # 200MB limit
        'default_sample_size': 100,
        'sampling_methods': [
            ('Sequential (first N rows)', 'sequential'),
            ('Random sampling', 'random'),
            ('Stratified sampling', 'stratified')
        ]
    }
    
    @staticmethod
    def get_output_dir() -> Path:
        """Gets output directory path"""
        output_dir = Path.home() / 'CSVToolkit' / 'output'
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir 