import pandas as pd
import re
from typing import List, Tuple, Dict, Any, Optional, Callable
from ..base.base_processor import BaseProcessor

class PhoneProcessor(BaseProcessor):
    """Processor for extracting phone numbers from CSV columns"""
    
    # Phone number pattern - updated for better matching
    PHONE_PATTERN = r'\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})'
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def get_columns(self, file_path: str) -> List[str]:
        """Gets column names from CSV file"""
        return self.reader.get_columns(file_path)
    
    def format_phone(self, match: re.Match) -> str:
        """Formats phone number to standard format"""
        area_code, prefix, number = match.groups()
        return f"({area_code}) {prefix}-{number}"
    
    def extract_phones(self, text: str, format_numbers: bool = True) -> List[str]:
        """Extracts phone numbers from text"""
        if pd.isna(text):
            return []
            
        text = str(text)  # Convert to string to handle numeric values
        matches = list(re.finditer(self.PHONE_PATTERN, text))
        if not matches:
            return []
            
        if format_numbers:
            return [self.format_phone(m) for m in matches]
        return [m.group(0) for m in matches]
    
    def process_file(self, input_file: str, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Processes file to extract phone numbers
        
        Args:
            input_file: Path to input CSV
            **options:
                columns: List of columns to search
                keep_original: Whether to keep original columns
                format_numbers: Whether to format found numbers
                progress_callback: Optional progress callback function
        """
        # Set up progress tracking
        if 'progress_callback' in options:
            self.set_progress_callback(options.pop('progress_callback'))
        
        # Read the data
        self.update_progress(20, "Reading file...")
        df = self.reader.read_csv(input_file)
        
        # Process the data
        self.update_progress(40, "Processing columns...")
        result_df, stats = self._process_data(df, **options)
        
        return result_df, stats
    
    def _process_data(self, df: pd.DataFrame, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Processes DataFrame to extract phone numbers"""
        columns = options.get('columns', [])
        keep_original = options.get('keep_original', True)
        format_numbers = options.get('format_numbers', True)
        
        # Create new DataFrame with selected columns
        if keep_original:
            result_df = df.copy()
        else:
            result_df = pd.DataFrame(index=df.index)
        
        phones_found = 0
        total_cols = len(columns)
        
        # Process each column
        for i, col in enumerate(columns):
            # Extract phone numbers
            new_col = f"{col}_phones"
            phones = df[col].apply(lambda x: self.extract_phones(x, format_numbers))
            
            # Count total phones found
            phones_found += sum(len(p) for p in phones)
            
            # Add extracted numbers to result
            result_df[new_col] = phones.apply(lambda x: '; '.join(x) if x else '')
            
            # Update progress
            if self.progress:
                progress = int(40 + ((i + 1) / total_cols * 40))  # 40-80% progress
                self.update_progress(progress, f"Processing column {i+1} of {total_cols}...")
        
        # Clean up any empty columns
        if not keep_original:
            result_df = result_df.loc[:, (result_df != '').any()]
        
        return result_df, {
            'phones_found': phones_found,
            'columns_processed': len(columns)
        } 