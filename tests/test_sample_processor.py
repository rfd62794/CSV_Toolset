import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from tools.processors.sample_processor import SampleProcessor
from .test_base import BaseProcessorTest

class TestSampleProcessor(BaseProcessorTest):
    """Test suite for Sample Processor"""
    
    @pytest.fixture
    def processor(self):
        return SampleProcessor()
    
    @pytest.fixture
    def test_data(self):
        # Create rich test dataset
        return pd.DataFrame({
            'id': range(1000),
            'category': ['A']*500 + ['B']*300 + ['C']*200,
            'subcategory': ['X', 'Y', 'Z'] * 334,
            'value': np.random.randn(1000),
            'date': pd.date_range('2024-01-01', periods=1000),
            'amount': np.random.randint(1, 1000, 1000),
            'status': ['Active', 'Inactive'] * 500
        })
    
    def test_sequential_sampling(self, processor, test_data):
        """Test sequential sampling functionality"""
        # Basic sequential sample
        result, stats = processor._process_data(test_data, sample_size=100, method='sequential')
        assert len(result) == 100
        assert result.index.tolist() == list(range(100))
        assert stats['sampling_rate'] == '10.0%'
        
        # Full dataset sample
        result, stats = processor._process_data(test_data, sample_size=1000, method='sequential')
        assert len(result) == 1000
        assert stats['sampling_rate'] == '100.0%'
        
        # Verify data integrity
        assert result['id'].tolist() == list(range(1000))
    
    def test_random_sampling(self, processor, test_data):
        """Test random sampling functionality"""
        # Test reproducibility
        result1, _ = processor._process_data(test_data, sample_size=100, method='random', random_seed=42)
        result2, _ = processor._process_data(test_data, sample_size=100, method='random', random_seed=42)
        pd.testing.assert_frame_equal(result1, result2)
        
        # Test different seeds produce different results
        result3, _ = processor._process_data(test_data, sample_size=100, method='random', random_seed=43)
        assert not result1.equals(result3)
        
        # Test sample size accuracy
        result, stats = processor._process_data(test_data, sample_size=250, method='random')
        assert len(result) == 250
        assert stats['sampling_rate'] == '25.0%'
    
    def test_stratified_sampling(self, processor, test_data):
        """Test stratified sampling functionality"""
        # Test single column stratification
        result, stats = processor._process_data(
            test_data,
            sample_size=100,
            method='stratified',
            strat_column='category'
        )
        group_stats = stats['group_stats']
        
        # Check proportions
        assert abs(float(group_stats['A']['sample_pct'].rstrip('%')) - 50.0) < 5
        assert abs(float(group_stats['B']['sample_pct'].rstrip('%')) - 30.0) < 5
        assert abs(float(group_stats['C']['sample_pct'].rstrip('%')) - 20.0) < 5
        
        # Test with binary column
        result, stats = processor._process_data(
            test_data,
            sample_size=100,
            method='stratified',
            strat_column='status'
        )
        assert len(result) == 100
        assert set(result['status'].unique()) == {'Active', 'Inactive'}
    
    def test_edge_cases(self, processor):
        """Test edge cases and error handling"""
        # Empty DataFrame
        with pytest.raises(ValueError, match="File contains no data"):
            processor._process_data(pd.DataFrame(), sample_size=10)
        
        # Single row
        single_row = pd.DataFrame({'a': [1]})
        result, stats = processor._process_data(single_row, sample_size=10)
        assert len(result) == 1
        
        # Missing values in stratification
        df_with_nulls = pd.DataFrame({'cat': ['A', None, 'B']})
        with pytest.raises(ValueError, match="contains missing values"):
            processor._process_data(
                df_with_nulls,
                sample_size=2,
                method='stratified',
                strat_column='cat'
            )
        
        # Single category in stratification
        df_single_cat = pd.DataFrame({'cat': ['A']*10})
        with pytest.raises(ValueError, match="at least 2 unique values"):
            processor._process_data(
                df_single_cat,
                sample_size=5,
                method='stratified',
                strat_column='cat'
            )
    
    def test_validation(self, processor, test_data):
        """Test input validation"""
        # Sample size validation
        with pytest.raises(ValueError, match="must be at least"):
            processor._process_data(test_data, sample_size=0)
        
        with pytest.raises(ValueError, match="must be a valid number"):
            processor._process_data(test_data, sample_size="invalid")
        
        # Large sample size handling
        huge_size = processor.config.SAMPLE_SETTINGS['max_sample_size'] + 1
        result, stats = processor._process_data(test_data, sample_size=huge_size)
        assert len(result) <= processor.config.SAMPLE_SETTINGS['max_sample_size']
        
        # Invalid method
        with pytest.raises(ValueError, match="Invalid sampling method"):
            processor._process_data(test_data, sample_size=10, method="invalid")
        
        # Missing stratification column
        with pytest.raises(ValueError, match="Stratification column .* not found"):
            processor._process_data(
                test_data,
                sample_size=10,
                method="stratified",
                strat_column="nonexistent"
            )
    
    def test_data_integrity(self, processor, test_data):
        """Test that sampling preserves data integrity"""
        result, _ = processor._process_data(test_data, sample_size=100)
        
        # Check all columns are preserved
        assert list(result.columns) == list(test_data.columns)
        
        # Check data types are preserved
        for col in result.columns:
            assert result[col].dtype == test_data[col].dtype
        
        # Check value ranges
        assert result['amount'].min() >= test_data['amount'].min()
        assert result['amount'].max() <= test_data['amount'].max()
        
        # Check date handling
        assert isinstance(result['date'].iloc[0], datetime) 