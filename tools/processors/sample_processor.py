import pandas as pd
import numpy as np
from .base_processor import BaseProcessor
from ..utils.data_transformer import DataTransformer

class SampleProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.transformer = DataTransformer()
    
    def _process_data(self, df, sample_size, random=False, keep_header=True):
        """
        Creates a sample from DataFrame.
        Implements abstract method from BaseProcessor.
        """
        # Validate sample size
        valid, error = self.validator.validate_sample_size(len(df), sample_size)
        if not valid:
            raise ValueError(error)
            
        return self.transformer.create_sample(
            df, 
            int(sample_size), 
            random, 
            keep_header
        )
    
    def process_file(self, input_file, sample_size, random=False, keep_header=True, progress_callback=None):
        """Creates a sample from CSV file"""
        self.set_progress_callback(progress_callback)
        
        try:
            # Read data
            self.update_progress(0, "Reading file...")
            df = self.reader.read_csv(input_file)
            
            # Process sample
            self.update_progress(50, "Creating sample...")
            result = self._process_data(df, sample_size, random, keep_header)
            
            stats = {
                'total_rows': len(df),
                'sample_size': len(result),
                'sampling_method': 'random' if random else 'sequential'
            }
            
            return result, stats
            
        except Exception as e:
            return False, str(e) 