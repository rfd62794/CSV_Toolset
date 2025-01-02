import pandas as pd
from typing import Dict, Any, List, Union
from pathlib import Path
from ..base.base_processor import BaseProcessor

class ColumnManagerProcessor(BaseProcessor):
    """Processor for managing CSV columns"""
    
    def rename_columns(self, df: pd.DataFrame, rename_map: Dict[str, str]) -> pd.DataFrame:
        """Renames columns according to mapping"""
        return df.rename(columns=rename_map)
    
    def reorder_columns(self, df: pd.DataFrame, column_order: List[str]) -> pd.DataFrame:
        """Reorders columns in specified order"""
        # Validate all columns exist
        missing = set(column_order) - set(df.columns)
        if missing:
            raise ValueError(f"Columns not found: {missing}")
            
        # Add any remaining columns at the end
        remaining = [col for col in df.columns if col not in column_order]
        final_order = column_order + remaining
        
        return df[final_order]
    
    def remove_columns(self, df: pd.DataFrame, columns_to_remove: List[str]) -> pd.DataFrame:
        """Removes specified columns"""
        return df.drop(columns=columns_to_remove)
    
    def add_column(self, df: pd.DataFrame, column_name: str, 
                   value: Union[str, int, float]) -> pd.DataFrame:
        """Adds a new column with specified value"""
        df[column_name] = value
        return df
    
    def split_column(self, df: pd.DataFrame, column: str, 
                    separator: str, new_names: List[str]) -> pd.DataFrame:
        """Splits a column into multiple columns"""
        split_df = df[column].str.split(separator, expand=True)
        
        # Validate number of new columns matches split result
        if len(new_names) != len(split_df.columns):
            raise ValueError(
                f"Number of new column names ({len(new_names)}) "
                f"doesn't match split result ({len(split_df.columns)})"
            )
            
        # Add split columns with new names
        for i, name in enumerate(new_names):
            df[name] = split_df[i]
            
        return df
    
    def combine_columns(self, df: pd.DataFrame, columns: List[str],
                       new_column: str, separator: str = " ") -> pd.DataFrame:
        """Combines multiple columns into one"""
        df[new_column] = df[columns].astype(str).agg(separator.join, axis=1)
        return df
    
    def process_file(self, input_file: str, config: dict) -> Dict[str, Any]:
        """Processes the input file according to configuration"""
        try:
            df = pd.read_csv(input_file)
            operation = config.get('operation')
            
            if operation == 'Rename Columns':
                rename_map = config.get('rename_map', {})
                df = self.rename_columns(df, rename_map)
                
            elif operation == 'Reorder Columns':
                column_order = config.get('column_order', [])
                df = self.reorder_columns(df, column_order)
                
            elif operation == 'Remove Columns':
                columns_to_remove = config.get('columns_to_remove', [])
                df = self.remove_columns(df, columns_to_remove)
                
            elif operation == 'Add Column':
                column_name = config.get('new_column_name')
                value = config.get('column_value')
                df = self.add_column(df, column_name, value)
                
            elif operation == 'Split Column':
                column = config.get('split_column')
                separator = config.get('separator', ',')
                new_names = config.get('new_column_names', [])
                df = self.split_column(df, column, separator, new_names)
                
            elif operation == 'Combine Columns':
                columns = config.get('columns_to_combine', [])
                new_column = config.get('combined_column_name')
                separator = config.get('separator', ' ')
                df = self.combine_columns(df, columns, new_column, separator)
            
            # Save processed file
            output_file = str(Path(input_file).with_stem(f"{Path(input_file).stem}_processed"))
            df.to_csv(output_file, index=False)
            
            return {
                'success': True,
                'output_file': output_file,
                'columns': list(df.columns),
                'rows': len(df),
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'output_file': None,
                'columns': [],
                'rows': 0,
                'error': str(e)
            } 