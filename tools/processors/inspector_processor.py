import pandas as pd
from typing import Dict, Any
from ..base.base_processor import BaseProcessor

class InspectorProcessor(BaseProcessor):
    """Processor for inspecting CSV data"""
    
    def inspect_data(self, df: pd.DataFrame, config: dict) -> Dict[str, Dict[str, Any]]:
        """Inspects dataframe and returns analysis results"""
        results = {}
        
        # Basic info
        results['Basic Info'] = {
            'Rows': len(df),
            'Columns': len(df.columns),
            'Memory Usage': f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        }
        
        # Data types
        if config.get('show_datatypes', True):
            results['Data Types'] = {
                col: str(dtype) for col, dtype in df.dtypes.items()
            }
        
        # Null counts
        if config.get('show_nulls', True):
            results['Null Counts'] = {
                col: str(df[col].isna().sum()) for col in df.columns
            }
        
        # Unique values
        if config.get('show_unique', True):
            results['Unique Values'] = {
                col: str(df[col].nunique()) for col in df.columns
            }
        
        return results
    
    def _process_data(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """Required implementation of abstract method"""
        return df  # Inspector doesn't modify data 