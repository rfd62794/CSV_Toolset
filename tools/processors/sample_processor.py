import pandas as pd
import numpy as np

class SampleProcessor:
    @staticmethod
    def get_file_info(file_path):
        """
        Gets basic file information.
        
        Returns:
            dict: Contains total_rows and num_columns
        """
        # Get total rows (excluding header)
        total_rows = sum(1 for _ in open(file_path)) - 1
        
        # Get column count
        df_sample = pd.read_csv(file_path, nrows=1)
        num_columns = len(df_sample.columns)
        
        return {
            'total_rows': total_rows,
            'num_columns': num_columns
        }
    
    @classmethod
    def validate_sample_size(cls, file_path, sample_size):
        """
        Validates the requested sample size.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            sample_size = int(sample_size)
            if sample_size < 1:
                return False, "Sample size must be at least 1"
                
            total_rows = cls.get_file_info(file_path)['total_rows']
            if sample_size > total_rows:
                return False, f"Sample size ({sample_size:,}) is larger than total rows ({total_rows:,})"
                
            return True, None
            
        except ValueError:
            return False, "Sample size must be a valid number"
    
    @classmethod
    def create_sample(cls, file_path, sample_size, random=False, keep_header=True):
        """
        Creates a sample from the CSV file.
        
        Args:
            file_path: Path to input CSV
            sample_size: Number of rows to include
            random: If True, use random sampling
            keep_header: If True, preserve header row
            
        Returns:
            DataFrame containing the sample
        """
        if random:
            # Random sampling
            df = pd.read_csv(file_path)
            if keep_header:
                header = df.iloc[:1]
                sample = df.iloc[1:].sample(n=sample_size)
                df_sample = pd.concat([header, sample])
            else:
                df_sample = df.sample(n=sample_size)
        else:
            # Sequential sampling
            skiprows = None if keep_header else 0
            df_sample = pd.read_csv(
                file_path,
                nrows=sample_size,
                skiprows=skiprows
            )
            
        return df_sample 