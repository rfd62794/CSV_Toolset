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
    
    def split_column(self, df: pd.DataFrame, column: str, separator: str = None, 
                    new_names: List[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Splits a column into multiple columns"""
        if column not in df.columns:
            raise ValueError(f"Column not found: {column}")
            
        result = df.copy()
        
        if separator:
            # Split by separator
            split_df = result[column].str.split(separator, expand=True)
        else:
            # Split by character position
            split_df = pd.DataFrame({
                i: result[column].str[i] 
                for i in range(len(result[column].str[0]))
            })
        
        # Name new columns
        if new_names and len(new_names) >= split_df.shape[1]:
            split_df.columns = new_names[:split_df.shape[1]]
        else:
            split_df.columns = [f"{column}_{i+1}" for i in range(split_df.shape[1])]
        
        # Add split columns to result
        result = pd.concat([result, split_df], axis=1)
        result = result.drop(columns=[column])
        
        stats = {
            'original_column': column,
            'new_columns': list(split_df.columns),
            'separator': separator
        }
        
        return result, stats
    
    def merge_columns(self, df: pd.DataFrame, columns: List[str], new_name: str, 
                     separator: str = "") -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Merges multiple columns into one"""
        missing = [col for col in columns if col not in df.columns]
        if missing:
            raise ValueError(f"Columns not found: {', '.join(missing)}")
            
        result = df.copy()
        
        # Convert all columns to string and merge
        merged = result[columns[0]].astype(str)
        for col in columns[1:]:
            merged = merged + separator + result[col].astype(str)
        
        # Add merged column and remove originals
        result[new_name] = merged
        result = result.drop(columns=columns)
        
        stats = {
            'merged_columns': columns,
            'new_column': new_name,
            'separator': separator
        }
        
        return result, stats
    
    def derive_column(self, df: pd.DataFrame, new_name: str, 
                     method: str, source_columns: List[str] = None, 
                     **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Derives a new column using various methods"""
        result = df.copy()
        
        if method == "concatenate":
            result[new_name] = self._derive_concatenate(df, source_columns, options)
        elif method == "arithmetic":
            result[new_name] = self._derive_arithmetic(df, source_columns, options)
        elif method == "conditional":
            result[new_name] = self._derive_conditional(df, source_columns, options)
        elif method == "transform":
            result[new_name] = self._derive_transform(df, source_columns, options)
        else:
            raise ValueError(f"Invalid derivation method: {method}")
        
        stats = {
            'new_column': new_name,
            'method': method,
            'source_columns': source_columns,
            'options': options
        }
        
        return result, stats
    
    def convert_type(self, df: pd.DataFrame, column: str, 
                    new_type: str, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Converts column data type"""
        if column not in df.columns:
            raise ValueError(f"Column not found: {column}")
            
        result = df.copy()
        original_type = str(result[column].dtype)
        
        try:
            if new_type == "numeric":
                result[column] = pd.to_numeric(result[column], errors=options.get('on_error', 'raise'))
            elif new_type == "datetime":
                result[column] = pd.to_datetime(result[column], format=options.get('format'))
            elif new_type == "category":
                result[column] = result[column].astype('category')
            elif new_type == "string":
                result[column] = result[column].astype(str)
            elif new_type == "boolean":
                result[column] = result[column].astype(bool)
            else:
                result[column] = result[column].astype(new_type)
            
            stats = {
                'column': column,
                'original_type': original_type,
                'new_type': str(result[column].dtype),
                'conversion_options': options
            }
            
            return result, stats
            
        except Exception as e:
            raise ValueError(f"Type conversion failed: {str(e)}")
    
    # Helper methods for derive_column
    def _derive_concatenate(self, df: pd.DataFrame, columns: List[str], 
                           options: Dict[str, Any]) -> pd.Series:
        """Concatenates multiple columns"""
        separator = options.get('separator', '')
        return df[columns].astype(str).agg(separator.join, axis=1)
    
    def _derive_arithmetic(self, df: pd.DataFrame, columns: List[str], 
                          options: Dict[str, Any]) -> pd.Series:
        """Performs arithmetic operations"""
        operation = options.get('operation', 'sum')
        if operation == 'sum':
            return df[columns].sum(axis=1)
        elif operation == 'product':
            return df[columns].prod(axis=1)
        elif operation == 'mean':
            return df[columns].mean(axis=1)
        else:
            raise ValueError(f"Invalid arithmetic operation: {operation}")
    
    def _derive_conditional(self, df: pd.DataFrame, columns: List[str], 
                           options: Dict[str, Any]) -> pd.Series:
        """Creates conditional column"""
        condition = options.get('condition')
        if not condition:
            raise ValueError("Condition required for conditional derivation")
        return df.eval(condition)
    
    def _derive_transform(self, df: pd.DataFrame, columns: List[str], 
                         options: Dict[str, Any]) -> pd.Series:
        """Applies transformation to columns"""
        transform = options.get('transform', 'identity')
        if transform == 'identity':
            return df[columns[0]]
        elif transform == 'abs':
            return df[columns[0]].abs()
        elif transform == 'log':
            return np.log(df[columns[0]])
        elif transform == 'sqrt':
            return np.sqrt(df[columns[0]])
        else:
            raise ValueError(f"Invalid transform: {transform}") 