from typing import Dict, Any, List, Callable
import pandas as pd
import re
from ..base.base_processor import BaseProcessor

class ValidatorProcessor(BaseProcessor):
    """Processor for data validation"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def validate_data(self, df: pd.DataFrame, rules: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Validates data against specified rules"""
        results = {
            'total_rows': len(df),
            'columns_checked': list(rules.keys()),
            'validation_results': {}
        }
        
        try:
            for column, column_rules in rules.items():
                if column not in df.columns:
                    raise ValueError(f"Column '{column}' not found")
                
                column_results = self._validate_column(df[column], column_rules)
                results['validation_results'][column] = column_results
            
            return results
            
        except Exception as e:
            raise RuntimeError(f"Error validating data: {str(e)}")
    
    def _validate_column(self, series: pd.Series, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Validates a single column"""
        results = {}
        
        if rules.get('null_check'):
            results['null_check'] = {
                'valid': not series.isnull().any(),
                'null_count': series.isnull().sum()
            }
        
        if rules.get('unique_check'):
            results['unique_check'] = {
                'valid': series.is_unique,
                'duplicate_count': len(series) - series.nunique()
            }
        
        if rules.get('type_check'):
            expected_type = rules['type_check'].get('type')
            results['type_check'] = self._check_data_type(series, expected_type)
        
        if rules.get('range_check'):
            range_config = rules['range_check']
            results['range_check'] = self._check_value_range(
                series,
                range_config.get('min'),
                range_config.get('max')
            )
        
        if rules.get('pattern_check'):
            pattern = rules['pattern_check'].get('pattern')
            results['pattern_check'] = self._check_pattern(series, pattern)
        
        if rules.get('custom_check'):
            func = rules['custom_check'].get('function')
            if func and callable(func):
                results['custom_check'] = {
                    'valid': all(func(x) for x in series),
                    'invalid_count': sum(not func(x) for x in series)
                }
        
        return results
    
    def _check_data_type(self, series: pd.Series, expected_type: str) -> Dict[str, Any]:
        """Checks data type of values"""
        type_checkers = {
            'int': lambda x: pd.to_numeric(x, errors='coerce').notnull(),
            'float': lambda x: pd.to_numeric(x, errors='coerce').notnull(),
            'date': lambda x: pd.to_datetime(x, errors='coerce').notnull(),
            'bool': lambda x: pd.to_numeric(x, errors='coerce').notnull() 
                            and x.isin([0, 1, True, False, 'True', 'False'])
        }
        
        if expected_type not in type_checkers:
            raise ValueError(f"Unsupported type check: {expected_type}")
            
        checker = type_checkers[expected_type]
        valid_mask = checker(series)
        
        return {
            'valid': valid_mask.all(),
            'invalid_count': (~valid_mask).sum(),
            'invalid_examples': series[~valid_mask].head().tolist()
        }
    
    def _check_value_range(self, series: pd.Series, min_val: Any = None, max_val: Any = None) -> Dict[str, Any]:
        """Checks if values are within specified range"""
        in_range = pd.Series(True, index=series.index)
        
        if min_val is not None:
            in_range &= series >= min_val
        if max_val is not None:
            in_range &= series <= max_val
        
        return {
            'valid': in_range.all(),
            'out_of_range_count': (~in_range).sum(),
            'out_of_range_examples': series[~in_range].head().tolist()
        }
    
    def _check_pattern(self, series: pd.Series, pattern: str) -> Dict[str, Any]:
        """Checks if values match regex pattern"""
        try:
            regex = re.compile(pattern)
            matches = series.astype(str).str.match(pattern)
            
            return {
                'valid': matches.all(),
                'invalid_count': (~matches).sum(),
                'invalid_examples': series[~matches].head().tolist()
            }
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {str(e)}") 