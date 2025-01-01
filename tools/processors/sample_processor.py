import pandas as pd
import numpy as np
from .base_processor import BaseProcessor

class SampleProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
    
    def _process_data(self, df, sample_size, random=False, keep_header=True):
        """
        Creates a sample from the DataFrame.
        Implements abstract method from BaseProcessor.
        """
        if random:
            if keep_header:
                header = df.iloc[:1]
                sample = df.iloc[1:].sample(n=sample_size)
                return pd.concat([header, sample])
            else:
                return df.sample(n=sample_size)
        else:
            # Sequential sampling
            if keep_header:
                return pd.concat([df.iloc[:1], df.iloc[1:sample_size + 1]])
            else:
                return df.iloc[:sample_size]
    
    def process_file(self, input_file, sample_size, random=False, keep_header=True, progress_callback=None):
        """Creates a sample from the CSV file"""
        self.set_progress_callback(progress_callback)
        
        # Validate sample size
        df = self.reader.read_csv(input_file)
        valid, error = self.validator.validate_sample_size(len(df), sample_size)
        if not valid:
            return False, error
            
        # Process the sample
        df_sample = self._process_data(df, int(sample_size), random, keep_header)
        
        stats = {
            'total_rows': len(df),
            'sample_size': len(df_sample),
            'sampling_method': 'random' if random else 'sequential'
        }
        
        return df_sample, stats 