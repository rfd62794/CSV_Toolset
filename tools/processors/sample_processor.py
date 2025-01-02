from typing import Union, Dict, Any, Tuple
import pandas as pd
from pathlib import Path
from ..base.base_processor import BaseProcessor

class SampleProcessor(BaseProcessor):
    """Processor for creating data samples"""
    
    def process_file(self, input_data: Union[str, pd.DataFrame], config: dict) -> Dict[str, Any]:
        """
        Creates sample from input data
        
        Args:
            input_data: Path to CSV file or DataFrame
            config: Dictionary containing:
                sample_type: Sampling method ('Random', 'Systematic', 'Stratified')
                sample_size: Number of rows to sample
                strat_column: Column to use for stratification (for stratified sampling)
        """
        try:
            # Read data if file path provided
            if isinstance(input_data, (str, Path)):
                self.update_progress(20, "Reading file...")
                df = pd.read_csv(input_data)
            else:
                df = input_data
            
            # Get configuration values
            sample_type = config.get('sample_type', 'Random')
            sample_size = int(config.get('sample_size', 100))
            strat_column = config.get('strat_column')
            
            # Validate sample size
            if sample_size < 1:
                raise ValueError("Sample size must be at least 1")
            if sample_size > len(df):
                sample_size = len(df)
            
            # Create sample
            self.update_progress(40, "Creating sample...")
            
            if sample_type == 'Random':
                result = df.sample(n=sample_size)
            elif sample_type == 'Systematic':
                step = len(df) // sample_size
                result = df.iloc[::step].head(sample_size)
            elif sample_type == 'Stratified' and strat_column:
                groups = df.groupby(strat_column)
                proportions = groups.size() / len(df)
                result = pd.concat([
                    group.sample(n=max(1, int(sample_size * prop)))
                    for prop, (_, group) in zip(proportions, groups)
                ]).head(sample_size)
            else:
                result = df.head(sample_size)
            
            # Generate output file path and save
            self.update_progress(80, "Saving sample...")
            if isinstance(input_data, (str, Path)):
                input_path = Path(input_data)
                output_file = input_path.parent / f"{input_path.stem}_sample_{sample_size}{input_path.suffix}"
                result.to_csv(output_file, index=False)
            else:
                output_file = "sample.csv"  # Default name when input is DataFrame
                result.to_csv(output_file, index=False)
            
            self.update_progress(100, "Sample created successfully!")
            
            return {
                'success': True,
                'output_file': str(output_file),
                'rows': len(result),
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'output_file': None,
                'rows': 0,
                'error': str(e)
            } 