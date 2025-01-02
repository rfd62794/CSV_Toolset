from typing import List, Tuple, Dict, Any, Optional
import pandas as pd
import numpy as np
from ..base.base_processor import BaseProcessor

class SampleProcessor(BaseProcessor):
    """Processor for creating data samples"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def get_columns(self, file_path: str) -> List[str]:
        """Gets column names from CSV file"""
        return self.reader.get_columns(file_path)
    
    def validate_sample_size(self, total_rows: int, sample_size: Any) -> Tuple[bool, str]:
        """Validates sample size input"""
        try:
            size = int(sample_size)
            min_size = self.config.SAMPLE_SETTINGS['min_sample_size']
            max_size = min(total_rows, self.config.SAMPLE_SETTINGS['max_sample_size'])
            
            if size < min_size:
                return False, f"Sample size must be at least {min_size}"
            if size > max_size:
                return False, f"Sample size ({size:,}) cannot exceed {max_size:,}"
            return True, ""
            
        except (ValueError, TypeError):
            return False, "Sample size must be a valid number"
    
    def validate_file(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """Validates input data"""
        if df.empty:
            return False, "File contains no data"
            
        file_size = df.memory_usage(deep=True).sum()
        max_size = self.config.SAMPLE_SETTINGS['max_file_size']
        
        if file_size > max_size:
            size_mb = max_size / (1024 * 1024)
            return False, f"File too large. Maximum size is {size_mb:.0f}MB"
            
        return True, ""
    
    def _process_data(self, df: pd.DataFrame, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Creates sample from DataFrame
        
        Args:
            df: Input DataFrame
            **options:
                sample_size: Number of rows to sample
                method: Sampling method ('sequential', 'random', 'stratified')
                strat_column: Column to use for stratification
                random_seed: Optional seed for random sampling
        """
        # Validate input
        valid, error = self.validate_file(df)
        if not valid:
            raise ValueError(error)
        
        # Get and validate options
        sample_size = int(options.get('sample_size', self.config.SAMPLE_SETTINGS['default_sample_size']))
        valid, error = self.validate_sample_size(len(df), sample_size)
        if not valid:
            raise ValueError(error)
            
        method = options.get('method', 'sequential')
        strat_column = options.get('strat_column')
        random_seed = options.get('random_seed')
        
        total_rows = len(df)
        if sample_size > total_rows:
            sample_size = total_rows
        
        try:
            # Set random seed if provided
            if random_seed is not None:
                np.random.seed(random_seed)
            
            # Get sample based on method
            if method == 'random':
                if self.progress:
                    self.update_progress(40, "Creating random sample...")
                sample = df.sample(n=sample_size, random_state=random_seed)
                
            elif method == 'stratified' and strat_column:
                if self.progress:
                    self.update_progress(40, "Creating stratified sample...")
                    
                # Calculate proportions for each group
                props = df[strat_column].value_counts(normalize=True)
                
                # Get stratified sample
                samples = []
                total_groups = len(props)
                
                for i, (group, prop) in enumerate(props.items()):
                    if self.progress:
                        progress = int(40 + ((i + 1) / total_groups * 30))
                        self.update_progress(progress, f"Processing group {i+1} of {total_groups}...")
                        
                    group_size = int(np.ceil(prop * sample_size))
                    group_df = df[df[strat_column] == group]
                    
                    if len(group_df) > group_size:
                        samples.append(group_df.sample(n=group_size))
                    else:
                        samples.append(group_df)
                
                sample = pd.concat(samples)
                
                # Trim to exact sample size if needed
                if len(sample) > sample_size:
                    sample = sample.sample(n=sample_size)
                    
            else:  # sequential
                if self.progress:
                    self.update_progress(40, "Creating sequential sample...")
                sample = df.head(sample_size)
            
            # Sort by index if random sampling was used
            if method in ['random', 'stratified']:
                sample = sample.sort_index()
            
            if self.progress:
                self.update_progress(80, "Finalizing sample...")
            
            return sample, {
                'total_rows': total_rows,
                'sampled_rows': len(sample),
                'method': method,
                'sampling_rate': f"{(len(sample) / total_rows * 100):.1f}%"
            }
            
        except Exception as e:
            raise RuntimeError(f"Error creating sample: {str(e)}") 
    
    def process_file(self, input_file: str, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Creates sample from CSV file
        
        Args:
            input_file: Path to input CSV file
            **options:
                sample_size: Number of rows to sample
                method: Sampling method ('sequential', 'random', 'stratified')
                strat_column: Column to use for stratification
                progress_callback: Optional progress callback function
        """
        # Set up progress tracking
        if 'progress_callback' in options:
            self.set_progress_callback(options.pop('progress_callback'))
        
        try:
            # Read data
            self.update_progress(0, "Reading file...")
            df = self.reader.read_csv(input_file)
            
            # Process data
            self.update_progress(40, "Creating sample...")
            result_df, stats = self._process_data(df, **options)
            
            return result_df, stats
            
        except Exception as e:
            raise RuntimeError(f"Error creating sample: {str(e)}") 