import pandas as pd
import numpy as np
from typing import List

class DataTransformer:
    """Handles common DataFrame transformations"""
    
    @staticmethod
    def reverse_rows(df, keep_header=True):
        """Reverses row order in DataFrame"""
        if keep_header:
            header = df.iloc[:1]
            reversed_data = df.iloc[1:].iloc[::-1]
            return pd.concat([header, reversed_data])
        return df.iloc[::-1]
    
    @staticmethod
    def sort_by_column(df, column, ascending=True, keep_header=True):
        """Sorts DataFrame by column"""
        if keep_header:
            header = df.iloc[:1]
            sorted_data = df.iloc[1:].sort_values(by=column, ascending=ascending)
            return pd.concat([header, sorted_data])
        return df.sort_values(by=column, ascending=ascending)
    
    @staticmethod
    def filter_rows(df, condition, keep_header=True):
        """Filters DataFrame rows based on condition"""
        if keep_header:
            header = df.iloc[:1]
            filtered_data = df.iloc[1:][condition]
            return pd.concat([header, filtered_data])
        return df[condition] 
    
    @staticmethod
    def create_sample(df, sample_size, random=False, keep_header=True):
        """Creates a sample from DataFrame"""
        if keep_header:
            header = df.iloc[:1]
            if random:
                sample = df.iloc[1:].sample(n=sample_size)
            else:
                sample = df.iloc[1:sample_size + 1]
            return pd.concat([header, sample])
        else:
            if random:
                return df.sample(n=sample_size)
            else:
                return df.iloc[:sample_size]
    
    @staticmethod
    def stratified_sample(df, column, size_per_group, random=True, keep_header=True):
        """Creates stratified sample based on column values"""
        if keep_header:
            header = df.iloc[:1]
            data = df.iloc[1:]
        else:
            data = df
            
        samples = []
        if keep_header:
            samples.append(header)
            
        for value in data[column].unique():
            group = data[data[column] == value]
            size = min(size_per_group, len(group))
            if random:
                sample = group.sample(n=size)
            else:
                sample = group.iloc[:size]
            samples.append(sample)
            
        return pd.concat(samples) 
    
    @staticmethod
    def filter_empty_values(df: pd.DataFrame, columns: List[str], 
                          treat_empty_as_null: bool = True) -> pd.DataFrame:
        """Filters rows with empty/null values in specified columns"""
        df_clean = df.copy()
        
        if treat_empty_as_null:
            # Consider empty strings as missing values
            for col in columns:
                df_clean = df_clean[df_clean[col].astype(str).str.strip() != '']
        
        # Remove rows with NaN values in selected columns
        df_clean = df_clean.dropna(subset=columns)
        return df_clean 