class ToolConfig:
    """Common configuration settings"""
    
    # File settings
    DEFAULT_ENCODING = 'utf-8'
    CSV_EXTENSIONS = ['.csv']
    
    # Preview settings
    DEFAULT_PREVIEW_ROWS = 5
    
    # Progress settings
    PROGRESS_STEPS = {
        'READ': 0,
        'PROCESS': 33,
        'SAVE': 66,
        'COMPLETE': 100
    }
    
    # Error messages
    ERRORS = {
        'NO_FILE': "No file selected",
        'INVALID_FILE': "Selected file is not a CSV file",
        'FILE_NOT_FOUND': "File not found: {}",
        'SAVE_FAILED': "Failed to save file: {}"
    } 