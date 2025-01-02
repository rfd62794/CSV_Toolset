from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Any

class SamplingStrategy(ABC):
    """Base class for sampling strategies"""
    
    @abstractmethod
    def sample(self, df: pd.DataFrame, sample_size: int) -> pd.DataFrame:
        """Creates a sample using the strategy"""
        pass

class SequentialSampling(SamplingStrategy):
    """Takes the first N rows"""
    
    def sample(self, df: pd.DataFrame, sample_size: int) -> pd.DataFrame:
        return df.head(sample_size)

class RandomSampling(SamplingStrategy):
    """Takes a random sample"""
    
    def sample(self, df: pd.DataFrame, sample_size: int) -> pd.DataFrame:
        return df.sample(n=sample_size).sort_index()

class StratifiedSampling(SamplingStrategy):
    """Takes a stratified sample based on a column"""
    
    def __init__(self, strat_column: str):
        self.strat_column = strat_column
    
    def sample(self, df: pd.DataFrame, sample_size: int) -> pd.DataFrame:
        props = df[self.strat_column].value_counts(normalize=True)
        samples = []
        
        for group in props.index:
            group_size = int(np.ceil(props[group] * sample_size))
            group_df = df[df[self.strat_column] == group]
            if len(group_df) > group_size:
                samples.append(group_df.sample(n=group_size))
            else:
                samples.append(group_df)
        
        sample = pd.concat(samples)
        if len(sample) > sample_size:
            sample = sample.sample(n=sample_size)
        
        return sample.sort_index() 