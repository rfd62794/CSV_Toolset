from typing import List, Tuple, Dict, Any
import pandas as pd
import operator
from ..base.base_processor import BaseProcessor

class FilterProcessor(BaseProcessor):
    """Processor for filtering CSV data"""
    
    OPERATORS = {
        'equals': operator.eq,
        'not_equals': operator.ne,
        'greater_than': operator.gt,
        'less_than': operator.lt,
        'greater_equal': operator.ge,
        'less_equal': operator.le,
        'contains': lambda x, y: x.str.contains(y, na=False),
        'starts_with': lambda x, y: x.str.startswith(y, na=False),
        'ends_with': lambda x, y: x.str.endswith(y, na=False)
    }
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
        self.writer = self.get_writer()
    
    def filter_data(self, df: pd.DataFrame, conditions: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Filters DataFrame based on conditions"""
        if not conditions:
            raise ValueError("No filter conditions provided")
            
        try:
            result = df.copy()
            total_rows = len(df)
            
            for condition in conditions:
                column = condition['column']
                operator = condition['operator']
                value = condition['value']
                
                if column not in df.columns:
                    raise ValueError(f"Column '{column}' not found")
                
                if operator not in self.OPERATORS:
                    raise ValueError(f"Invalid operator: {operator}")
                
                mask = self.OPERATORS[operator](df[column], value)
                result = result[mask]
            
            stats = {
                'total_rows': total_rows,
                'filtered_rows': len(result),
                'removed_rows': total_rows - len(result),
                'conditions_applied': len(conditions)
            }
            
            return result, stats
            
        except Exception as e:
            raise RuntimeError(f"Error filtering data: {str(e)}") 