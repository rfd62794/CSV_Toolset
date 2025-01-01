from ..utils.data_reader import DataReader
from ..utils.data_writer import DataWriter
from ..utils.data_validator import DataValidator
from ..utils.progress_tracker import ProgressTracker
from ..utils.config import ToolConfig

class BaseProcessor:
    """Base class for all data processors"""
    
    def __init__(self):
        self.reader = DataReader()
        self.writer = DataWriter()
        self.validator = DataValidator()
        self.progress = None
        self.config = ToolConfig()
    
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
            self.update_progress(
                self.config.PROGRESS_STEPS['READ'],
                "Reading file..."
            )
            df = self.reader.read_csv(input_file)
            
            # Validate input if needed
            if hasattr(self, 'required_columns'):
                valid, error = self.validator.validate_columns_exist(
                    df, 
                    self.required_columns
                )
                if not valid:
                    raise ValueError(error)
            
            # Process data
            self.update_progress(
                self.config.PROGRESS_STEPS['PROCESS'],
                "Processing data..."
            )
            result = self._process_data(df, **options)
            
            # Write output
            self.update_progress(
                self.config.PROGRESS_STEPS['SAVE'],
                "Saving results..."
            )
            success, error = self.writer.write_csv(result, output_file)
            
            if not success:
                raise Exception(self.config.ERRORS['SAVE_FAILED'].format(error))
            
            self.update_progress(
                self.config.PROGRESS_STEPS['COMPLETE'],
                "Processing complete!"
            )
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    def _process_data(self, df, **options):
        """Override this method in subclasses"""
        raise NotImplementedError 