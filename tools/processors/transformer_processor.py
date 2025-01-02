from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from ..base.base_processor import BaseProcessor

class TransformerProcessor(BaseProcessor):
    """Processor for transforming CSV data"""
    
    TRANSFORMATIONS = {
        'Uppercase': lambda x: x.str.upper(),
        'Lowercase': lambda x: x.str.lower(),
        'Title Case': lambda x: x.str.title(),
        'Strip Whitespace': lambda x: x.str.strip(),
        'Remove Special Characters': lambda x: x.str.replace(r'[^a-zA-Z0-9\s]', '', regex=True),
        'Format Numbers': lambda x: pd.to_numeric(x, errors='coerce').fillna(x),
        'Format Dates': lambda x: pd.to_datetime(x, errors='coerce').fillna(x)
    }
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
        self.writer = self.get_writer()
    
    def transform_data(self, df: pd.DataFrame, column: str, transformations: Dict[str, bool], 
                      custom_regex: str = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Applies transformations to specified column"""
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")
            
        result = df.copy()
        applied = []
        
        try:
            for trans_name, apply in transformations.items():
                if not apply:
                    continue
                    
                if trans_name == "Custom Regex" and custom_regex:
                    result[column] = result[column].str.replace(
                        custom_regex, '', regex=True
                    )
                    applied.append(f"Custom Regex: {custom_regex}")
                elif trans_name in self.TRANSFORMATIONS:
                    result[column] = self.TRANSFORMATIONS[trans_name](result[column])
                    applied.append(trans_name)
            
            stats = {
                'column': column,
                'transformations_applied': applied,
                'rows_processed': len(df)
            }
            
            return result, stats
            
        except Exception as e:
            raise RuntimeError(f"Error transforming data: {str(e)}") 