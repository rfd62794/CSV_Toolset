import pandas as pd
from typing import List, Tuple, Dict, Any
from ..base.base_processor import BaseProcessor

class ReformatterProcessor(BaseProcessor):
    """Processor for reformatting CSV data"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def get_columns(self, file_path: str) -> List[str]:
        """Gets column names from CSV file"""
        return self.reader.get_columns(file_path)
    
    def _process_data(self, df: pd.DataFrame, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Reformats DataFrame according to options
        
        Args:
            df: Input DataFrame
            **options:
                case: str - Case transformation ('upper', 'lower', 'title')
                trim: bool - Whether to trim whitespace
                columns: List[str] - Columns to process
                remove_special: bool - Whether to remove special characters
                date_format: str - Format for date columns
                number_format: str - Format for numeric columns
        """
        columns = options.get('columns', df.columns)
        case = options.get('case', None)
        trim = options.get('trim', False)
        remove_special = options.get('remove_special', False)
        date_format = options.get('date_format')
        number_format = options.get('number_format')
        
        result = df.copy()
        processed_cols = 0
        
        # Process each column
        total_cols = len(columns)
        for i, col in enumerate(columns):
            if col not in result.columns:
                continue
                
            # Update progress
            if self.progress:
                progress = int(((i + 1) / total_cols) * 80)
                self.update_progress(progress, f"Processing column {i+1} of {total_cols}...")
            
            # Apply transformations
            if case:
                if case == 'upper':
                    result[col] = result[col].astype(str).str.upper()
                elif case == 'lower':
                    result[col] = result[col].astype(str).str.lower()
                elif case == 'title':
                    result[col] = result[col].astype(str).str.title()
            
            if trim:
                result[col] = result[col].astype(str).str.strip()
            
            if remove_special:
                result[col] = result[col].astype(str).str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
            
            # Try date formatting
            if date_format and pd.api.types.is_datetime64_any_dtype(df[col]):
                try:
                    result[col] = pd.to_datetime(result[col]).dt.strftime(date_format)
                except (ValueError, TypeError):
                    pass
            
            # Try number formatting
            if number_format and pd.api.types.is_numeric_dtype(df[col]):
                try:
                    result[col] = result[col].apply(lambda x: format(x, number_format))
                except (ValueError, TypeError):
                    pass
            
            processed_cols += 1
        
        return result, {
            'columns_processed': processed_cols,
            'total_rows': len(df)
        } 