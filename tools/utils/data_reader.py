from typing import Optional, List, Dict, Any, Tuple
import pandas as pd
import chardet
from .config import ToolConfig

class DataReader:
    """Handles CSV file reading operations"""
    
    def __init__(self):
        self.config = ToolConfig()
    
    def detect_encoding(self, file_path: str, sample_size: int = 10000) -> str:
        """Detects file encoding"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(sample_size)
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                confidence = result['confidence']
                
                # Only use detected encoding if confidence is high
                if encoding and confidence > 0.8:
                    return encoding
                    
        except Exception:
            pass
            
        # Fall back to default encoding
        return self.config.FILE_SETTINGS['encoding']
    
    def read_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Reads CSV file with automatic encoding detection and proper type handling
        
        Args:
            file_path: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv
            
        Returns:
            pd.DataFrame: Loaded data
        """
        # Use provided encoding or detect it
        encoding = kwargs.pop('encoding', None)
        if not encoding:
            encoding = self.detect_encoding(file_path)
            
        default_args = {
            'encoding': encoding,
            'on_bad_lines': 'warn',
            'low_memory': False,  # Prevents mixed type warning
            'dtype': str  # Read all columns as strings initially
        }
        
        # Override defaults with provided kwargs
        args = {**default_args, **kwargs}
        
        try:
            df = pd.read_csv(file_path, **args)
            
            # Try to convert numeric columns where appropriate
            for col in df.columns:
                try:
                    # Check if column can be converted to numeric
                    numeric_series = pd.to_numeric(df[col], errors='raise')
                    df[col] = numeric_series
                except (ValueError, TypeError):
                    # Keep as string if conversion fails
                    continue
                    
            return df
            
        except UnicodeDecodeError:
            # If first attempt fails, try with default encoding
            args['encoding'] = self.config.FILE_SETTINGS['encoding']
            return pd.read_csv(file_path, **args)
    
    def read_csv_chunked(self, file_path: str, chunk_size: Optional[int] = None) -> pd.DataFrame:
        """Reads large CSV files in chunks"""
        if chunk_size is None:
            chunk_size = self.config.FILE_SETTINGS['chunk_size']
            
        encoding = self.detect_encoding(file_path)
        
        chunks = []
        for chunk in pd.read_csv(
            file_path, 
            chunksize=chunk_size,
            encoding=encoding,
            low_memory=False,
            dtype=str,
            on_bad_lines='warn'
        ):
            # Try to convert numeric columns
            for col in chunk.columns:
                try:
                    chunk[col] = pd.to_numeric(chunk[col], errors='raise')
                except (ValueError, TypeError):
                    continue
            chunks.append(chunk)
            
        return pd.concat(chunks)
    
    def get_columns(self, file_path: str) -> List[str]:
        """Gets column names from CSV file"""
        encoding = self.detect_encoding(file_path)
        return pd.read_csv(
            file_path, 
            nrows=0, 
            encoding=encoding
        ).columns.tolist()
    
    def preview_data(self, file_path: str, nrows: int = 5) -> pd.DataFrame:
        """Gets preview of CSV data"""
        return self.read_csv(file_path, nrows=nrows) 