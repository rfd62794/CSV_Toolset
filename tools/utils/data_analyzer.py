import pandas as pd

class DataAnalyzer:
    """Handles data analysis operations"""
    
    @staticmethod
    def analyze_column(series):
        """Analyzes a single column"""
        return {
            'type': str(series.dtype),
            'unique_values': series.nunique(),
            'null_count': series.isnull().sum(),
            'sample_values': series.head().tolist()
        }
    
    @classmethod
    def analyze_dataframe(cls, df):
        """Analyzes entire DataFrame"""
        column_stats = {}
        for col in df.columns:
            column_stats[col] = cls.analyze_column(df[col])
        return column_stats 