import pandas as pd

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