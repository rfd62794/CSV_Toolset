from .base_processor import BaseProcessor
from ..utils.data_transformer import DataTransformer

class ReverserProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.transformer = DataTransformer()
    
    def _process_data(self, df, keep_header=True):
        """
        Reverses row order in DataFrame.
        Implements abstract method from BaseProcessor.
        """
        return self.transformer.reverse_rows(df, keep_header)
    
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