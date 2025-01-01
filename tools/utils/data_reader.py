from typing import Optional, List, Dict, Any
import pandas as pd
from .config import ToolConfig

class DataReader:
    """Handles CSV file reading operations"""
    
    def __init__(self):
        self.config = ToolConfig()
    
    def read_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Reads CSV file with default settings"""
        default_args = {
            'encoding': self.config.FILE_SETTINGS['encoding'],
            'on_bad_lines': 'warn'
        }
        # Override defaults with provided kwargs
        args = {**default_args, **kwargs}
        return pd.read_csv(file_path, **args)
    
    def read_csv_chunked(self, file_path: str, chunk_size: Optional[int] = None) -> pd.DataFrame:
        """Reads large CSV files in chunks"""
        if chunk_size is None:
            chunk_size = self.config.FILE_SETTINGS['chunk_size']
            
        chunks = []
        for chunk in pd.read_csv(
            file_path, 
            chunksize=chunk_size,
            encoding=self.config.FILE_SETTINGS['encoding']
        ):
            chunks.append(chunk)
        return pd.concat(chunks)
    
    def get_columns(self, file_path: str) -> List[str]:
        """Gets column names from CSV file"""
        return pd.read_csv(
            file_path, 
            nrows=0, 
            encoding=self.config.FILE_SETTINGS['encoding']
        ).columns.tolist()
    
    def preview_data(self, file_path: str, nrows: int = 5) -> pd.DataFrame:
        """Gets preview of CSV data"""
        return pd.read_csv(
            file_path,
            nrows=nrows,
            encoding=self.config.FILE_SETTINGS['encoding']
        ) 