from ..utils.data_reader import DataReader
from ..utils.data_writer import DataWriter
from ..utils.progress_tracker import ProgressTracker

class BaseProcessor:
    """Base class for all data processors"""
    
    def __init__(self):
        self.reader = DataReader()
        self.writer = DataWriter()
        self.progress = None
    
    def set_progress_callback(self, callback):
        """Sets up progress tracking"""
        self.progress = ProgressTracker(callback)
    
    def update_progress(self, value, message=None):
        """Updates progress if callback is set"""
        if self.progress:
            self.progress.update(value, message)
    
    def process_file(self, input_file, output_file, **options):
        """Template method for file processing"""
        try:
            # Read input
            self.update_progress(0, "Reading file...")
            df = self.reader.read_csv(input_file)
            
            # Process data
            self.update_progress(33, "Processing data...")
            result = self._process_data(df, **options)
            
            # Write output
            self.update_progress(66, "Saving results...")
            success, error = self.writer.write_csv(result, output_file)
            
            if not success:
                raise Exception(f"Failed to save file: {error}")
            
            self.update_progress(100, "Processing complete!")
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    def _process_data(self, df, **options):
        """Override this method in subclasses"""
        raise NotImplementedError 