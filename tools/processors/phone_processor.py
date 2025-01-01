import pandas as pd
import re
from typing import List, Tuple, Dict, Any, Optional, Callable
from ..base.base_processor import BaseProcessor

class PhoneProcessor(BaseProcessor):
    """Processor for extracting phone numbers from CSV columns"""
    
    # Phone number pattern
    PHONE_PATTERN = r'\b(?:\+?1[-.]?)?\s*(?:\([0-9]{3}\)|[0-9]{3})[-.]?\s*[0-9]{3}[-.]?\s*[0-9]{4}\b'
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def get_columns(self, file_path: str) -> List[str]:
        """Gets column names from CSV file"""
        return self.reader.get_columns(file_path)
    
    def format_phone(self, match: re.Match) -> str:
        """Formats phone number to standard format"""
        # Extract just the digits
        digits = ''.join(re.findall(r'\d+', match.group(0)))
        
        # Remove leading 1 if present
        if len(digits) == 11 and digits.startswith('1'):
            digits = digits[1:]
            
        # Format as (XXX) XXX-XXXX
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    
    def extract_phones(self, text: str, format_numbers: bool = True) -> List[str]:
        """Extracts phone numbers from text"""
        if pd.isna(text):
            return []
            
        matches = list(re.finditer(self.PHONE_PATTERN, str(text)))
        if not matches:
            return []
            
        if format_numbers:
            return [self.format_phone(m) for m in matches]
        return [m.group(0) for m in matches]
    
    def _process_data(self, df: pd.DataFrame, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Processes DataFrame to extract phone numbers
        
        Args:
            df: Input DataFrame
            **options:
                columns: List of columns to search
                keep_original: Whether to keep original columns
                format_numbers: Whether to format found numbers
                
        Returns:
            tuple: (processed_df, stats_dict)
        """
        columns = options.get('columns', [])
        keep_original = options.get('keep_original', True)
        format_numbers = options.get('format_numbers', True)
        
        result_df = df.copy() if keep_original else pd.DataFrame(index=df.index)
        phones_found = 0
        
        # Process each column
        total_cols = len(columns)
        for i, col in enumerate(columns):
            # Extract phone numbers
            new_col = f"{col}_phones"
            phones = df[col].apply(
                lambda x: self.extract_phones(x, format_numbers)
            )
            
            # Count total phones found
            phones_found += sum(len(p) for p in phones)
            
            # Add extracted numbers to result
            result_df[new_col] = phones.apply(
                lambda x: '; '.join(x) if x else ''
            )
            
            # Update progress
            if self.progress:
                progress = int((i + 1) / total_cols * 80)  # Leave 20% for saving
                self.update_progress(
                    progress,
                    f"Processing column {i+1} of {total_cols}..."
                )
        
        return result_df, {
            'phones_found': phones_found,
            'columns_processed': len(columns)
        } 