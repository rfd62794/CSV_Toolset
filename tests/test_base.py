import pytest
from typing import Any, Dict, List, Optional
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
from .config import TestConfig

class BaseProcessorTest:
    """Base class for processor tests"""
    
    config = TestConfig()
    
    @pytest.fixture
    def processor(self):
        """Should be implemented by child classes"""
        raise NotImplementedError
    
    @pytest.fixture
    def test_data(self):
        """Should be implemented by child classes"""
        raise NotImplementedError
    
    @pytest.fixture
    def test_file_path(self, tmp_path: Path, test_data: pd.DataFrame) -> Path:
        """Creates a test CSV file"""
        file_path = tmp_path / "test.csv"
        test_data.to_csv(file_path, index=False)
        return file_path
    
    @pytest.fixture
    def large_test_data(self) -> pd.DataFrame:
        """Creates large test dataset"""
        rows = self.config.DATA_SETTINGS['large_file_rows']
        return pd.DataFrame({
            'id': range(rows),
            'value': np.random.randn(rows),
            'category': np.random.choice(['A', 'B', 'C'], rows),
            'date': pd.date_range('2024-01-01', periods=rows)
        })
    
    def create_test_data(
        self,
        rows: int = None,
        columns: Dict[str, Any] = None,
        seed: int = None
    ) -> pd.DataFrame:
        """Creates customized test data"""
        if seed is not None:
            np.random.seed(seed)
            
        rows = rows or self.config.DATA_SETTINGS['default_rows']
        
        if not columns:
            columns = {
                'id': range(rows),
                'numeric': np.random.randn(rows),
                'category': np.random.choice(['A', 'B', 'C'], rows),
                'date': pd.date_range('2024-01-01', periods=rows),
                'boolean': np.random.choice([True, False], rows)
            }
        
        return pd.DataFrame(columns)
    
    def verify_output_structure(
        self,
        result: Any,
        stats: dict,
        expected_stats: List[str] = None
    ):
        """Verifies basic output structure"""
        assert isinstance(result, pd.DataFrame)
        assert isinstance(stats, dict)
        
        if expected_stats:
            for stat in expected_stats:
                assert stat in stats
    
    def verify_data_integrity(
        self,
        input_df: pd.DataFrame,
        output_df: pd.DataFrame,
        check_types: bool = True,
        check_ranges: bool = True,
        exclude_cols: List[str] = None
    ):
        """Verifies data integrity between input and output"""
        exclude_cols = exclude_cols or []
        columns = [col for col in input_df.columns if col not in exclude_cols]
        
        # Check columns
        assert all(col in output_df.columns for col in columns)
        
        if check_types:
            # Check data types
            for col in columns:
                assert output_df[col].dtype == input_df[col].dtype
        
        if check_ranges:
            # Check value ranges for numeric columns
            for col in input_df[columns].select_dtypes(include=['number']).columns:
                assert output_df[col].min() >= input_df[col].min()
                assert output_df[col].max() <= input_df[col].max()
    
    def verify_temporal_data(self, df: pd.DataFrame, column: str):
        """Verifies temporal data handling"""
        assert pd.api.types.is_datetime64_any_dtype(df[column])
        assert isinstance(df[column].iloc[0], pd.Timestamp)
    
    def verify_categorical_data(
        self,
        df: pd.DataFrame,
        column: str,
        categories: List[str] = None
    ):
        """Verifies categorical data handling"""
        unique_values = df[column].unique()
        if categories:
            assert all(val in categories for val in unique_values)
    
    def verify_numeric_ranges(
        self,
        df: pd.DataFrame,
        column: str,
        min_val: float = None,
        max_val: float = None
    ):
        """Verifies numeric data ranges"""
        if min_val is not None:
            assert df[column].min() >= min_val
        if max_val is not None:
            assert df[column].max() <= max_val 