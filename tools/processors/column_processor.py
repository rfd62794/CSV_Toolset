from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from ..base.base_processor import BaseProcessor

class ColumnProcessor(BaseProcessor):
    """Processor for column operations"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
        self.writer = self.get_writer()
    
    def rename_column(self, df: pd.DataFrame, old_name: str, new_name: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Renames a column"""
        if old_name not in df.columns:
            raise ValueError(f"Column not found: {old_name}")
            
        if new_name in df.columns:
            raise ValueError(f"Column already exists: {new_name}")
            
        result = df.copy()
        result = result.rename(columns={old_name: new_name})
        
        stats = {
            'old_name': old_name,
            'new_name': new_name
        }
        
        return result, stats
    
    def reorder_columns(self, df: pd.DataFrame, new_positions: Dict[str, int]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Reorders columns based on new positions"""
        columns = list(df.columns)
        
        for col, new_pos in new_positions.items():
            if col not in columns:
                raise ValueError(f"Column not found: {col}")
                
            old_pos = columns.index(col)
            columns.insert(new_pos, columns.pop(old_pos))
        
        result = df[columns]
        
        stats = {
            'columns_moved': list(new_positions.keys()),
            'new_order': columns
        }
        
        return result, stats
    
    def remove_columns(self, df: pd.DataFrame, columns: List[str]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Removes specified columns"""
        missing = [col for col in columns if col not in df.columns]
        if missing:
            raise ValueError(f"Columns not found: {', '.join(missing)}")
            
        result = df.drop(columns=columns)
        
        stats = {
            'columns_removed': columns,
            'remaining_columns': list(result.columns)
        }
        
        return result, stats
    
    def add_column(self, df: pd.DataFrame, name: str, col_type: str, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Adds a new column"""
        if name in df.columns:
            raise ValueError(f"Column already exists: {name}")
            
        result = df.copy()
        
        if col_type == "empty":
            result[name] = pd.NA
        elif col_type == "sequence":
            result[name] = range(len(df))
        elif col_type == "constant":
            result[name] = options.get('value', '')
        elif col_type == "calculated":
            expr = options.get('expression', '')
            if not expr:
                raise ValueError("Expression required for calculated column")
            result[name] = result.eval(expr)
        else:
            raise ValueError(f"Invalid column type: {col_type}")
        
        stats = {
            'column_added': name,
            'type': col_type,
            'options': options
        }
        
        return result, stats 