from abc import ABC, abstractmethod
from typing import Callable, Optional, Tuple, Any, Dict
import pandas as pd
from ..utils.data_reader import DataReader
from ..utils.data_writer import DataWriter
from ..utils.data_validator import DataValidator
from ..utils.progress_tracker import ProgressTracker
from ..utils.config import ToolConfig

class BaseProcessor(ABC):
    """Base class for all data processors"""
    
    def __init__(self):
        self.reader = DataReader()
        self.writer = DataWriter()
        self.validator = DataValidator()
        self.config = ToolConfig()
        self.progress: Optional[ProgressTracker] = None
        
    def set_progress_callback(self, callback: Optional[Callable[[int, str], None]]) -> None:
        """Sets up progress tracking"""
        self.progress = ProgressTracker(callback) if callback else None
    
    def update_progress(self, percent: int, message: str) -> None:
        """Updates progress if tracker exists"""
        if self.progress:
            self.progress.update(percent, message)
    
    @abstractmethod
    def _process_data(self, df: pd.DataFrame, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Process the DataFrame with given options.
        Must be implemented by subclasses.
        
        Args:
            df: Input DataFrame
            **options: Processing options
            
        Returns:
            tuple: (processed_df, stats_dict)
        """
        pass
    
    def process_file(self, input_file: str, output_file: str = None, **options) -> Tuple[bool, Any]:
        """
        Processes a CSV file with progress tracking.
        
        Args:
            input_file: Path to input CSV
            output_file: Optional path to output CSV
            **options: Processing options
            
        Returns:
            tuple: (success, result_or_error)
        """
        try:
            # Validate input file
            valid, error = self.validator.validate_file(input_file)
            if not valid:
                return False, error
            
            # Read data
            self.update_progress(
                self.config.PROGRESS_STEPS['READ'],
                "Reading file..."
            )
            df = self.reader.read_csv(input_file)
            
            # Process data
            self.update_progress(
                self.config.PROGRESS_STEPS['PROCESS'],
                "Processing data..."
            )
            result_df, stats = self._process_data(df, **options)
            
            # Save if output file specified
            if output_file:
                self.update_progress(
                    self.config.PROGRESS_STEPS['SAVE'],
                    "Saving results..."
                )
                success, error = self.writer.write_csv(result_df, output_file)
                if not success:
                    return False, error
            
            self.update_progress(
                self.config.PROGRESS_STEPS['COMPLETE'],
                "Processing complete!"
            )
            
            return True, (result_df, stats)
            
        except Exception as e:
            return False, str(e) 