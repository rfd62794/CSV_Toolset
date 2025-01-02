import pandas as pd
from typing import List, Tuple, Dict, Any
from ..base.base_processor import BaseProcessor

class ReverserProcessor(BaseProcessor):
    """Processor for reversing row order in CSV files"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def _process_data(self, df: pd.DataFrame, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Reverses the order of rows in DataFrame
        
        Args:
            df: Input DataFrame
            **options:
                keep_header: bool - Whether to keep header row at top
        """
        keep_header = options.get('keep_header', True)
        total_rows = len(df)
        
        if self.progress:
            self.update_progress(20, f"Processing {total_rows:,} rows...")
        
        if keep_header and total_rows > 1:
            # Keep header row and reverse the rest
            header = df.iloc[:1]
            body = df.iloc[1:].iloc[::-1]
            result = pd.concat([header, body])
        else:
            # Reverse all rows
            result = df.iloc[::-1]
        
        return result, {
            'total_rows': total_rows,
            'keep_header': keep_header
        }
    
    def process_file(self, input_file, keep_header=True, progress_callback=None):
        """Reverses row order in CSV file"""
        self.set_progress_callback(progress_callback)
        
        try:
            # Read data
            self.update_progress(0, "Reading file...")
            df = self.reader.read_csv(input_file)
            
            # Process data
            self.update_progress(50, "Reversing rows...")
            result = self._process_data(df, keep_header)
            
            stats = {
                'total_rows': len(result),
                'header_kept': keep_header
            }
            
            return result, stats
            
        except Exception as e:
            return False, str(e) 