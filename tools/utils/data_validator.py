from typing import Tuple, List, Any
import pandas as pd
import os

class DataValidator:
    """Handles data validation across tools"""
    
    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str]:
        """Validates file exists and is CSV"""
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
            
        if not file_path.lower().endswith('.csv'):
            return False, "File must be a CSV file"
            
        if os.path.getsize(file_path) == 0:
            return False, "File is empty"
            
        return True, ""
    
    @staticmethod
    def validate_columns_exist(df: pd.DataFrame, columns: List[str]) -> Tuple[bool, str]:
        """Validates columns exist in DataFrame"""
        missing = [col for col in columns if col not in df.columns]
        if missing:
            return False, f"Columns not found: {', '.join(missing)}"
        return True, ""
    
    @staticmethod
    def validate_sample_size(total_rows: int, sample_size: Any) -> Tuple[bool, str]:
        """Validates sample size is valid"""
        try:
            sample_size = int(sample_size)
            if sample_size < 1:
                return False, "Sample size must be at least 1"
            if sample_size > total_rows:
                return False, f"Sample size ({sample_size:,}) is larger than total rows ({total_rows:,})"
            return True, ""
        except ValueError:
            return False, "Sample size must be a valid number" 