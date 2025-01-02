import pandas as pd
from typing import Dict, Any
from pathlib import Path
from ..base.base_processor import BaseProcessor

class ReverserProcessor(BaseProcessor):
    """Processor for reversing CSV data"""
    
    def reverse_rows(self, df: pd.DataFrame, keep_header: bool = True) -> pd.DataFrame:
        """Reverses row order"""
        if keep_header:
            header = df.iloc[0]
            df = df.iloc[1:].iloc[::-1]
            df = pd.concat([pd.DataFrame([header]), df])
        else:
            df = df.iloc[::-1]
        return df
    
    def reverse_columns(self, df: pd.DataFrame, keep_index: bool = False) -> pd.DataFrame:
        """Reverses column order"""
        if keep_index:
            index_col = df.index
            df = df.iloc[:, ::-1]
            df.index = index_col
        else:
            df = df.iloc[:, ::-1]
        return df
    
    def preview_reverse(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """Creates a preview of the reversed data"""
        # Get a sample of the data
        preview_df = df.head(5).copy()
        
        # Apply reversing based on configuration
        reverse_type = config.get('reverse_type', 'Rows')
        keep_header = config.get('keep_header', True)
        keep_index = config.get('keep_index', False)
        
        if reverse_type in ['Rows', 'Both']:
            preview_df = self.reverse_rows(preview_df, keep_header)
            
        if reverse_type in ['Columns', 'Both']:
            preview_df = self.reverse_columns(preview_df, keep_index)
            
        return preview_df
    
    def process_file(self, df: pd.DataFrame, config: dict) -> Dict[str, Any]:
        """Processes the input file according to configuration"""
        try:
            reverse_type = config.get('reverse_type', 'Rows')
            keep_header = config.get('keep_header', True)
            keep_index = config.get('keep_index', False)
            
            if reverse_type in ['Rows', 'Both']:
                df = self.reverse_rows(df, keep_header)
                
            if reverse_type in ['Columns', 'Both']:
                df = self.reverse_columns(df, keep_index)
            
            # Save processed file
            output_file = str(Path(self.input_file).with_stem(f"{Path(self.input_file).stem}_reversed"))
            df.to_csv(output_file, index=False)
            
            return {
                'success': True,
                'output_file': output_file,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'output_file': None,
                'error': str(e)
            } 