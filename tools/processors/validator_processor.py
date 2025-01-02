import pandas as pd
import numpy as np
from typing import Dict, Any, List
from ..base.base_processor import BaseProcessor

class ValidatorProcessor(BaseProcessor):
    """Processor for validating CSV data"""
    
    def check_datatypes(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Checks data types for each column"""
        results = {}
        for column in df.columns:
            # Try to infer consistent data type
            unique_types = df[column].apply(type).unique()
            consistent = len(unique_types) == 1
            
            # Check for numeric values
            numeric_count = pd.to_numeric(df[column], errors='coerce').notna().sum()
            
            results[column] = {
                'passed': consistent,
                'details': {
                    'types_found': [t.__name__ for t in unique_types],
                    'numeric_count': numeric_count,
                    'total_rows': len(df)
                }
            }
        return results
    
    def check_nulls(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Checks for null values in each column"""
        results = {}
        for column in df.columns:
            null_count = df[column].isna().sum()
            results[column] = {
                'passed': null_count == 0,
                'details': {
                    'null_count': null_count,
                    'total_rows': len(df),
                    'null_percentage': f"{(null_count/len(df))*100:.2f}%"
                }
            }
        return results
    
    def check_duplicates(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Checks for duplicate values in each column"""
        results = {}
        for column in df.columns:
            duplicate_count = df[column].duplicated().sum()
            results[column] = {
                'passed': duplicate_count == 0,
                'details': {
                    'duplicate_count': duplicate_count,
                    'unique_count': df[column].nunique(),
                    'total_rows': len(df)
                }
            }
        return results
    
    def check_ranges(self, df: pd.DataFrame, ranges: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, Any]]:
        """Checks value ranges for numeric columns"""
        results = {}
        for column, range_values in ranges.items():
            if column not in df.columns:
                continue
                
            numeric_data = pd.to_numeric(df[column], errors='coerce')
            min_val = range_values.get('min')
            max_val = range_values.get('max')
            
            if min_val is not None and max_val is not None:
                in_range = (numeric_data >= min_val) & (numeric_data <= max_val)
                out_of_range = (~in_range).sum()
                
                results[column] = {
                    'passed': out_of_range == 0,
                    'details': {
                        'out_of_range_count': out_of_range,
                        'min_found': numeric_data.min(),
                        'max_found': numeric_data.max(),
                        'total_rows': len(df)
                    }
                }
                
        return results
    
    def process_file(self, input_file: str, config: dict) -> Dict[str, Any]:
        """Processes the input file according to configuration"""
        try:
            df = pd.read_csv(input_file)
            results = {
                'success': True,
                'validation_results': {},
                'error': None
            }
            
            # Run enabled validations
            if config.get('check_datatypes'):
                results['validation_results']['datatypes'] = self.check_datatypes(df)
                
            if config.get('check_nulls'):
                results['validation_results']['nulls'] = self.check_nulls(df)
                
            if config.get('check_duplicates'):
                results['validation_results']['duplicates'] = self.check_duplicates(df)
                
            if config.get('check_ranges'):
                ranges = config.get('ranges', {})
                results['validation_results']['ranges'] = self.check_ranges(df, ranges)
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'validation_results': {},
                'error': str(e)
            } 