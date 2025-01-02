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
    
    def validate_file(self, df: pd.DataFrame, **options) -> Tuple[bool, str]:
        """Validates input data"""
        if df.empty:
            return False, "File contains no data"
            
        file_size = df.memory_usage(deep=True).sum()
        max_size = self.config.SAMPLE_SETTINGS['max_file_size']
        
        if file_size > max_size:
            size_mb = max_size / (1024 * 1024)
            return False, f"File too large. Maximum size is {size_mb:.0f}MB"
        
        # Check for null values in stratification column
        strat_column = options.get('strat_column')
        if strat_column:
            if strat_column not in df.columns:
                return False, f"Stratification column '{strat_column}' not found"
            if df[strat_column].isnull().any():
                return False, f"Column '{strat_column}' contains missing values"
            if df[strat_column].nunique() < 2:
                return False, f"Column '{strat_column}' must have at least 2 unique values"
            
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
                    
                # Validate stratification column
                if strat_column not in df.columns:
                    raise ValueError(f"Stratification column '{strat_column}' not found")
                    
                # Calculate proportions for each group
                group_counts = df[strat_column].value_counts()
                
                # Check if we have enough samples in each group
                min_group_size = group_counts.min()
                if min_group_size < 1:
                    raise ValueError(f"Found empty group in column '{strat_column}'")
                
                if sample_size < len(group_counts):
                    raise ValueError(
                        f"Sample size ({sample_size}) must be at least the number of groups "
                        f"({len(group_counts)}) for stratified sampling"
                    )
                
                # Calculate proportions and minimum samples per group
                props = group_counts / len(df)
                min_samples_per_group = max(1, int(sample_size * 0.01))  # At least 1% or 1 sample
                
                # Get stratified sample
                samples = []
                total_groups = len(props)
                remaining_size = sample_size
                
                for i, (group, prop) in enumerate(props.items()):
                    if self.progress:
                        progress = int(40 + ((i + 1) / total_groups * 30))
                        self.update_progress(progress, f"Processing group {i+1} of {total_groups}...")
                    
                    # Calculate group sample size (ensure at least minimum samples)
                    group_df = df[df[strat_column] == group]
                    desired_size = max(
                        min_samples_per_group,
                        min(
                            int(np.ceil(prop * sample_size)),  # Proportional size
                            len(group_df),  # Available size
                            remaining_size  # Remaining samples needed
                        )
                    )
                    
                    # Take sample from group
                    if len(group_df) > desired_size:
                        group_sample = group_df.sample(
                            n=desired_size,
                            random_state=random_seed
                        )
                    else:
                        group_sample = group_df
                    
                    samples.append(group_sample)
                    remaining_size -= len(group_sample)
                
                sample = pd.concat(samples)
                
                # Add distribution stats
                group_stats = {
                    f"group_{group}": len(group_df)
                    for group, group_df in sample.groupby(strat_column)
                }
                
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
            
            # Update stats dictionary to include group stats
            stats = {
                'total_rows': total_rows,
                'sampled_rows': len(sample),
                'method': method,
                'sampling_rate': f"{(len(sample) / total_rows * 100):.1f}%"
            }
            
            if method == 'stratified':
                stats['group_stats'] = {
                    str(group): len(group_df)
                    for group, group_df in sample.groupby(strat_column)
                }
            
            return sample, stats
            
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
    
    def _get_group_stats(self, df: pd.DataFrame, sample: pd.DataFrame, strat_column: str) -> Dict[str, Any]:
        """Calculates detailed group statistics"""
        orig_props = df[strat_column].value_counts(normalize=True)
        sample_props = sample[strat_column].value_counts(normalize=True)
        
        stats = {}
        for group in orig_props.index:
            stats[str(group)] = {
                'original_count': int(orig_props[group] * len(df)),
                'sample_count': int(sample_props.get(group, 0) * len(sample)),
                'original_pct': f"{orig_props[group]*100:.1f}%",
                'sample_pct': f"{sample_props.get(group, 0)*100:.1f}%"
            }
        return stats 
    
    def preview_sample(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """Creates a preview of the sample"""
        try:
            # Get configuration values
            sample_type = config.get('sample_type', 'Random')
            sample_size = int(config.get('sample_size', 5))  # Use smaller size for preview
            strat_column = config.get('strat_column')
            
            # Limit preview sample size
            preview_size = min(sample_size, 5)  # Show at most 5 rows in preview
            
            if sample_type == 'Random':
                preview = df.sample(n=preview_size)
            elif sample_type == 'Systematic':
                step = len(df) // preview_size
                preview = df.iloc[::step].head(preview_size)
            elif sample_type == 'Stratified' and strat_column:
                # Get proportional samples from each stratum
                groups = df.groupby(strat_column)
                proportions = groups.size() / len(df)
                preview = pd.concat([
                    group.sample(n=max(1, int(preview_size * prop)))
                    for prop, (_, group) in zip(proportions, groups)
                ]).head(preview_size)
            else:
                preview = df.head(preview_size)
                
            return preview.copy()
            
        except Exception as e:
            raise ValueError(f"Error creating preview: {str(e)}") 