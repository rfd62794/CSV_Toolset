import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from ..base.base_processor import BaseProcessor

class SampleProcessor(BaseProcessor):
    """Processor for creating data samples"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def get_columns(self, file_path: str) -> List[str]:
        """Gets column names from CSV file"""
        return self.reader.get_columns(file_path)
    
    def _process_data(self, df: pd.DataFrame, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Creates sample from DataFrame
        
        Args:
            df: Input DataFrame
            **options:
                sample_size: Number of rows to sample
                method: Sampling method ('sequential', 'random', 'stratified')
                strat_column: Column to use for stratification
                keep_header: Whether to keep header row
        """
        sample_size = int(options.get('sample_size', 100))
        method = options.get('method', 'sequential')
        strat_column = options.get('strat_column')
        keep_header = options.get('keep_header', True)
        
        total_rows = len(df)
        if sample_size > total_rows:
            sample_size = total_rows
        
        # Get sample based on method
        if method == 'random':
            sample = df.sample(n=sample_size)
            
        elif method == 'stratified' and strat_column:
            # Calculate proportions for each group
            props = df[strat_column].value_counts(normalize=True)
            
            # Get stratified sample
            samples = []
            for group in props.index:
                group_size = int(np.ceil(props[group] * sample_size))
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
            sample = df.head(sample_size)
        
        # Sort by index if random sampling was used
        if method in ['random', 'stratified']:
            sample = sample.sort_index()
        
        # Add header row if requested
        if keep_header and method != 'sequential':
            header_row = df.head(1)
            sample = pd.concat([header_row, sample])
        
        return sample, {
            'total_rows': total_rows,
            'sampled_rows': len(sample),
            'method': method
        }
    
    def validate_sample_size(self, total_rows: int, sample_size: Any) -> Tuple[bool, str]:
        """Validates sample size input"""
        try:
            size = int(sample_size)
            if size < 1:
                return False, "Sample size must be at least 1"
            if size > total_rows:
                return False, f"Sample size ({size:,}) is larger than total rows ({total_rows:,})"
            return True, ""
        except (ValueError, TypeError):
            return False, "Sample size must be a valid number" 