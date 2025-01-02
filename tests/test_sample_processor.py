import pytest
import pandas as pd
import numpy as np
from tools.processors.sample_processor import SampleProcessor

@pytest.fixture
def processor():
    return SampleProcessor()

@pytest.fixture
def test_data():
    return pd.DataFrame({
        'id': range(1000),
        'category': ['A']*500 + ['B']*300 + ['C']*200,
        'value': np.random.randn(1000),
        'date': pd.date_range('2024-01-01', periods=1000)
    })

def test_sequential_sampling(processor, test_data):
    result, stats = processor._process_data(test_data, sample_size=100, method='sequential')
    assert len(result) == 100
    assert result.index.tolist() == list(range(100))
    assert stats['sampling_rate'] == '10.0%'

def test_random_sampling_reproducibility(processor, test_data):
    result1, _ = processor._process_data(test_data, sample_size=100, method='random', random_seed=42)
    result2, _ = processor._process_data(test_data, sample_size=100, method='random', random_seed=42)
    pd.testing.assert_frame_equal(result1, result2)

def test_stratified_sampling_proportions(processor, test_data):
    result, stats = processor._process_data(
        test_data,
        sample_size=100,
        method='stratified',
        strat_column='category'
    )
    group_stats = stats['group_stats']
    assert abs(group_stats['A']['sample_pct'] - '50.0%') < 5
    assert abs(group_stats['B']['sample_pct'] - '30.0%') < 5
    assert abs(group_stats['C']['sample_pct'] - '20.0%') < 5

def test_edge_cases(processor):
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

def test_sample_size_validation(processor, test_data):
    # Too small
    with pytest.raises(ValueError, match="must be at least"):
        processor._process_data(test_data, sample_size=0)
    
    # Too large
    huge_size = processor.config.SAMPLE_SETTINGS['max_sample_size'] + 1
    result, stats = processor._process_data(test_data, sample_size=huge_size)
    assert len(result) <= processor.config.SAMPLE_SETTINGS['max_sample_size'] 