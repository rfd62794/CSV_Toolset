from typing import Dict, Any, List
import pandas as pd
import numpy as np
from scipy import stats
from ..base.base_processor import BaseProcessor

class ProfilerProcessor(BaseProcessor):
    """Processor for data profiling"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
    
    def profile_data(self, df: pd.DataFrame, analyses: Dict[str, bool]) -> Dict[str, Any]:
        """Generates data profile based on selected analyses"""
        results = {}
        
        try:
            if analyses.get('basic_stats'):
                results['basic_stats'] = self._compute_basic_stats(df)
            
            if analyses.get('data_types'):
                results['data_types'] = self._analyze_data_types(df)
            
            if analyses.get('missing_values'):
                results['missing_values'] = self._analyze_missing_values(df)
            
            if analyses.get('distribution'):
                results['distribution'] = self._analyze_distributions(df)
            
            if analyses.get('correlations'):
                results['correlations'] = self._compute_correlations(df)
            
            if analyses.get('outliers'):
                results['outliers'] = self._detect_outliers(df)
            
            if analyses.get('patterns'):
                results['patterns'] = self._analyze_patterns(df)
            
            # Compile data quality issues
            results['issues'] = self._compile_issues(results)
            
            return results
            
        except Exception as e:
            raise RuntimeError(f"Error profiling data: {str(e)}")
    
    def _compute_basic_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Computes basic statistics"""
        return {
            'row_count': len(df),
            'column_count': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'duplicate_rows': df.duplicated().sum(),
            'numeric_columns': len(df.select_dtypes(include=['number']).columns),
            'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns),
            'temporal_columns': len(df.select_dtypes(include=['datetime']).columns)
        }
    
    def _analyze_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyzes column data types"""
        return {
            'type_counts': df.dtypes.value_counts().to_dict(),
            'column_types': df.dtypes.to_dict(),
            'type_suggestions': self._suggest_data_types(df)
        }
    
    def _analyze_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyzes missing values"""
        missing = df.isnull().sum()
        return {
            'total_missing': missing.sum(),
            'missing_by_column': missing.to_dict(),
            'missing_patterns': self._analyze_missing_patterns(df)
        }
    
    def _analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyzes value distributions"""
        numeric_cols = df.select_dtypes(include=['number'])
        categorical_cols = df.select_dtypes(include=['object', 'category'])
        
        results = {
            'numeric_stats': numeric_cols.describe().to_dict(),
            'categorical_stats': {
                col: df[col].value_counts().to_dict()
                for col in categorical_cols
            }
        }
        
        # Add skewness and kurtosis for numeric columns
        if not numeric_cols.empty:
            results['skewness'] = numeric_cols.skew().to_dict()
            results['kurtosis'] = numeric_cols.kurtosis().to_dict()
        
        return results
    
    def _compute_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Computes correlations between numeric columns"""
        numeric_cols = df.select_dtypes(include=['number'])
        if numeric_cols.empty:
            return {}
            
        return {
            'pearson': numeric_cols.corr('pearson').to_dict(),
            'spearman': numeric_cols.corr('spearman').to_dict()
        }
    
    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detects outliers in numeric columns"""
        numeric_cols = df.select_dtypes(include=['number'])
        results = {}
        
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = df[col][(df[col] < lower) | (df[col] > upper)]
            
            results[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(df)) * 100,
                'range': (lower, upper),
                'examples': outliers.head().tolist()
            }
        
        return results
    
    def _analyze_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyzes patterns in the data"""
        return {
            'constant_columns': [
                col for col in df.columns
                if df[col].nunique() == 1
            ],
            'binary_columns': [
                col for col in df.columns
                if df[col].nunique() == 2
            ],
            'unique_columns': [
                col for col in df.columns
                if df[col].is_unique
            ]
        } 