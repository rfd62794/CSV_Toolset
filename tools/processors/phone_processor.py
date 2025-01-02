import pandas as pd
import re
from typing import Dict, Any
from pathlib import Path
from ..base.base_processor import BaseProcessor

class PhoneProcessor(BaseProcessor):
    """Processor for formatting phone numbers"""
    
    def __init__(self):
        super().__init__()
        self.formats = {
            '(XXX) XXX-XXXX': r'(\d{3}) \d{3}-\d{4}',
            'XXX-XXX-XXXX': r'\d{3}-\d{3}-\d{4}',
            'XXX.XXX.XXXX': r'\d{3}.\d{3}.\d{4}',
            'XXXXXXXXXX': r'\d{10}'
        }
    
    def format_number(self, number: str, format_pattern: str) -> str:
        """Formats a phone number according to the specified pattern"""
        try:
            # Extract digits only
            digits = ''.join(filter(str.isdigit, str(number)))
            
            # Handle empty or invalid input
            if not digits or len(digits) < 10:
                return number  # Return original if invalid
            
            # Take last 10 digits if longer
            digits = digits[-10:]
            
            # Format according to pattern
            if format_pattern == '(XXX) XXX-XXXX':
                return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            elif format_pattern == 'XXX-XXX-XXXX':
                return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
            elif format_pattern == 'XXX.XXX.XXXX':
                return f"{digits[:3]}.{digits[3:6]}.{digits[6:]}"
            else:  # XXXXXXXXXX
                return digits
                
        except Exception:
            return number  # Return original if formatting fails
    
    def preview_format(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """Creates a preview of the phone formatting"""
        try:
            preview_df = df.head(5).copy()
            
            column = config.get('column')
            if not column or column not in preview_df.columns:
                raise ValueError("Invalid column selected")
                
            format_pattern = config.get('format', '(XXX) XXX-XXXX')
            keep_original = config.get('keep_original', True)
            validate = config.get('validate_numbers', True)
            
            # Format numbers
            new_col = f"{column}_formatted"
            preview_df[new_col] = preview_df[column].apply(
                lambda x: self.format_number(x, format_pattern)
            )
            
            # Validate if requested
            if validate:
                pattern = self.formats[format_pattern]
                preview_df[f"{column}_valid"] = preview_df[new_col].apply(
                    lambda x: bool(re.match(pattern, str(x)))
                )
            
            # Remove original if not keeping
            if not keep_original:
                preview_df.drop(column, axis=1, inplace=True)
                
            return preview_df
            
        except Exception as e:
            raise ValueError(f"Preview error: {str(e)}")
    
    def process_file(self, df: pd.DataFrame, config: dict) -> Dict[str, Any]:
        """Processes the input file according to configuration"""
        try:
            column = config.get('column')
            if not column or column not in df.columns:
                raise ValueError("Invalid column selected")
                
            format_pattern = config.get('format', '(XXX) XXX-XXXX')
            keep_original = config.get('keep_original', True)
            validate = config.get('validate_numbers', True)
            
            # Format numbers
            new_col = f"{column}_formatted"
            df[new_col] = df[column].apply(
                lambda x: self.format_number(x, format_pattern)
            )
            
            # Validate if requested
            if validate:
                pattern = self.formats[format_pattern]
                df[f"{column}_valid"] = df[new_col].apply(
                    lambda x: bool(re.match(pattern, str(x)))
                )
            
            # Remove original if not keeping
            if not keep_original:
                df.drop(column, axis=1, inplace=True)
            
            # Save processed file
            output_file = str(Path(self.input_file).with_stem(f"{Path(self.input_file).stem}_formatted"))
            df.to_csv(output_file, index=False)
            
            return {
                'success': True,
                'output_file': output_file,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'output_file': None,
                'error': str(e)
            }
    
    def _process_data(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """Implements required abstract method"""
        column = config.get('column')
        format_pattern = config.get('format', '(XXX) XXX-XXXX')
        
        df = df.copy()
        df[column] = df[column].apply(
            lambda x: self.format_number(x, format_pattern)
        )
        return df 