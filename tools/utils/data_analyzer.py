import pandas as pd
import numpy as np
from typing import Dict, Any, List

class DataAnalyzer:
    """Handles data analysis and statistics"""
    
    @staticmethod
    def get_column_type(series: pd.Series) -> str:
        """Determines column data type"""
        if pd.api.types.is_numeric_dtype(series):
            return 'numeric'
        elif pd.api.types.is_datetime64_dtype(series):
            return 'datetime'
        return 'text'
    
    @staticmethod
    def get_sample_values(series: pd.Series, n: int = 5) -> List[Any]:
        """Gets sample of unique values from column"""
        unique = series.dropna().unique()
        if len(unique) <= n:
            return unique.tolist()
        return unique[:n].tolist()
    
    @staticmethod
    def analyze_column(series: pd.Series) -> Dict[str, Any]:
        """Analyzes a single column"""
        stats = {
            'type': DataAnalyzer.get_column_type(series),
            'unique_values': series.nunique(),
            'null_count': series.isna().sum(),
            'sample_values': DataAnalyzer.get_sample_values(series)
        }
        
        # Add type-specific statistics
        if stats['type'] == 'numeric':
            stats.update({
                'min': series.min(),
                'max': series.max(),
                'mean': series.mean(),
                'median': series.median()
            })
        elif stats['type'] == 'text':
            non_empty = series.astype(str).str.strip().str.len() > 0
            stats.update({
                'empty_count': (~non_empty).sum(),
                'min_length': series[non_empty].str.len().min(),
                'max_length': series[non_empty].str.len().max()
            })
            
        return stats
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Analyzes all columns in DataFrame"""
        return {col: self.analyze_column(df[col]) for col in df.columns} 