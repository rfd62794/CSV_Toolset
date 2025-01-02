from typing import List, Tuple, Dict, Any, Optional
import pandas as pd
from ..base.base_processor import BaseProcessor
from .sampling_strategies import (
    SamplingStrategy, SequentialSampling, 
    RandomSampling, StratifiedSampling
)

class SampleProcessor(BaseProcessor):
    """Processor for creating data samples"""
    
    STRATEGIES = {
        'sequential': SequentialSampling,
        'random': RandomSampling,
        'stratified': lambda col: StratifiedSampling(col)
    }
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def get_columns(self, file_path: str) -> List[str]:
        """Gets column names from CSV file"""
        return self.reader.get_columns(file_path)
    
    def get_strategy(self, method: str, strat_column: str = None) -> SamplingStrategy:
        """Gets appropriate sampling strategy"""
        if method not in self.STRATEGIES:
            raise ValueError(f"Unknown sampling method: {method}")
            
        strategy_class = self.STRATEGIES[method]
        if method == 'stratified':
            if not strat_column:
                raise ValueError("Stratification column required for stratified sampling")
            return strategy_class(strat_column)
        return strategy_class()
    
    def _process_data(self, df: pd.DataFrame, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Creates sample from DataFrame"""
        # Validate and get options
        sample_size = self._validate_sample_size(len(df), options.get('sample_size', 100))
        method = options.get('method', 'sequential')
        keep_header = options.get('keep_header', True)
        
        # Get appropriate strategy
        strategy = self.get_strategy(method, options.get('strat_column'))
        
        # Create sample
        sample = strategy.sample(df, sample_size)
        
        # Add header if requested
        if keep_header and method != 'sequential':
            header_row = df.head(1)
            sample = pd.concat([header_row, sample])
        
        return sample, {
            'total_rows': len(df),
            'sampled_rows': len(sample),
            'method': method
        }
    
    def _validate_sample_size(self, total_rows: int, sample_size: Any) -> int:
        """Validates and returns sample size"""
        try:
            size = int(sample_size)
            if size < 1:
                raise ValueError("Sample size must be at least 1")
            return min(size, total_rows)
        except (ValueError, TypeError):
            raise ValueError("Sample size must be a valid number") 