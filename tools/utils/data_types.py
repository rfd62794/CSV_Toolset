from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
import re

class DataTypeDetector:
    """Utility class for detecting and converting data types"""
    
    DATE_PATTERNS = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
        r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
    ]
    
    @classmethod
    def detect_column_type(cls, series: pd.Series) -> Tuple[str, float]:
        """Detects the most likely data type for a column"""
        # Check for all null
        if series.isna().all():
            return 'null', 1.0
            
        # Get non-null values
        non_null = series.dropna()
        if len(non_null) == 0:
            return 'null', 1.0
            
        # Try numeric first
        try:
            pd.to_numeric(non_null)
            # Check if integers
            if (non_null.astype(float) % 1 == 0).all():
                return 'integer', 1.0
            return 'float', 1.0
        except (ValueError, TypeError):
            pass
        
        # Try datetime
        for pattern in cls.DATE_PATTERNS:
            if non_null.astype(str).str.match(pattern).mean() > 0.8:
                return 'datetime', 0.8
        
        # Check for boolean
        bool_values = {'true', 'false', 'yes', 'no', '1', '0', 't', 'f', 'y', 'n'}
        if non_null.astype(str).str.lower().isin(bool_values).all():
            return 'boolean', 1.0
        
        # Default to string
        return 'string', 1.0
    
    @classmethod
    def convert_column(cls, series: pd.Series, target_type: str) -> pd.Series:
        """Converts a column to the specified type"""
        try:
            if target_type == 'integer':
                return pd.to_numeric(series, errors='coerce').astype('Int64')
            elif target_type == 'float':
                return pd.to_numeric(series, errors='coerce')
            elif target_type == 'datetime':
                return pd.to_datetime(series, errors='coerce')
            elif target_type == 'boolean':
                return series.map({'true': True, 'false': False, 
                                 'yes': True, 'no': False,
                                 '1': True, '0': False,
                                 't': True, 'f': False,
                                 'y': True, 'n': False}).astype('boolean')
            else:
                return series.astype(str)
        except Exception:
            return series.astype(str) 