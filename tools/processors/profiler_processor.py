import pandas as pd
import numpy as np
from typing import Dict, Any
from ..base.base_processor import BaseProcessor

class ProfilerProcessor(BaseProcessor):
    """Processor for data profiling"""
    
    def profile_data(self, df: pd.DataFrame, config: dict) -> Dict[str, Any]:
        """Profiles dataframe and returns analysis results"""
        if df is None or df.empty:
            raise ValueError("No data to profile")
            
        try:
            results = {}
            
            # Basic statistics
            if config.get('show_stats', True):
                results['statistics'] = self._compute_statistics(df)
            
            # Distribution analysis
            if config.get('show_distribution', True):
                results['distribution'] = self._analyze_distribution(df)
            
            # Correlations
            if config.get('show_correlations', True):
                results['correlations'] = self._compute_correlations(df)
            
            return results
            
        except Exception as e:
            raise ValueError(f"Error profiling data: {str(e)}")
    
    def _compute_statistics(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Computes basic statistics for each column"""
        stats = {}
        for col in df.columns:
            col_stats = {
                'type': str(df[col].dtype),
                'count': len(df[col])
            }
            
            if pd.api.types.is_numeric_dtype(df[col]):
                desc = df[col].describe()
                col_stats.update({
                    'mean': f"{desc['mean']:.3f}",
                    'std': f"{desc['std']:.3f}",
                    'min': f"{desc['min']:.3f}",
                    'max': f"{desc['max']:.3f}"
                })
            
            stats[col] = col_stats
        return stats
    
    def _analyze_distribution(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Analyzes value distribution for each column"""
        dist = {}
        for col in df.columns:
            dist[col] = {
                'unique': df[col].nunique(),
                'missing': df[col].isna().sum(),
                'top_values': df[col].value_counts().head(3).to_dict()
            }
        return dist
    
    def _compute_correlations(self, df: pd.DataFrame) -> list:
        """Computes correlations between numeric columns"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlations = []
        
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    correlations.append({
                        'col1': numeric_cols[i],
                        'col2': numeric_cols[j],
                        'value': corr_matrix.iloc[i, j]
                    })
        
        return correlations
    
    def _process_data(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """Required implementation of abstract method"""
        return df  # Profiler doesn't modify data 