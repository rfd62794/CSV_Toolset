import pytest
from typing import Any
from pathlib import Path
import pandas as pd

class BaseProcessorTest:
    """Base class for processor tests"""
    
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
    
    def verify_output_structure(self, result: Any, stats: dict):
        """Verifies basic output structure"""
        assert isinstance(result, pd.DataFrame)
        assert isinstance(stats, dict)
        assert 'total_rows' in stats
        assert 'sampling_rate' in stats
    
    def verify_data_integrity(self, input_df: pd.DataFrame, output_df: pd.DataFrame):
        """Verifies data integrity between input and output"""
        # Check columns
        assert list(output_df.columns) == list(input_df.columns)
        
        # Check data types
        for col in output_df.columns:
            assert output_df[col].dtype == input_df[col].dtype
        
        # Check value ranges for numeric columns
        for col in input_df.select_dtypes(include=['number']).columns:
            assert output_df[col].min() >= input_df[col].min()
            assert output_df[col].max() <= input_df[col].max() 