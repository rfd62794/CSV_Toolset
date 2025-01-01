from typing import Tuple, Optional, Dict, Any
import pandas as pd
from pathlib import Path
from .config import ToolConfig
from .file_operations import FileOperations

class DataWriter:
    """Handles CSV file writing operations"""
    
    def __init__(self):
        self.config = ToolConfig()
        self.file_ops = FileOperations()
    
    def write_csv(self, df: pd.DataFrame, file_path: str, 
                 index: bool = False, **kwargs) -> Tuple[bool, Optional[str]]:
        """
        Writes DataFrame to CSV with error handling
        
        Returns:
            tuple: (success, error_message)
        """
        try:
            # Ensure output directory exists
            self.file_ops.ensure_directory(file_path)
            
            # Write with default settings
            default_args = {
                'encoding': self.config.FILE_SETTINGS['encoding'],
                'index': index
            }
            args = {**default_args, **kwargs}
            
            df.to_csv(file_path, **args)
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    def write_excel(self, df: pd.DataFrame, file_path: str,
                   sheet_name: str = 'Sheet1') -> Tuple[bool, Optional[str]]:
        """Writes DataFrame to Excel file"""
        try:
            self.file_ops.ensure_directory(file_path)
            df.to_excel(file_path, sheet_name=sheet_name, index=False)
            return True, None
        except Exception as e:
            return False, str(e) 