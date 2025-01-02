import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
from .config import TestConfig

config = TestConfig()

@pytest.fixture(scope="session")
def large_csv_file(tmp_path_factory) -> Path:
    """Creates a large CSV file for testing"""
    base_dir = tmp_path_factory.mktemp('test_data')
    file_path = base_dir / "large_test.csv"
    
    # Create large DataFrame
    rows = config.DATA_SETTINGS['large_file_rows']
    df = pd.DataFrame({
        'id': range(rows),
        'value': np.random.randn(rows),
        'category': np.random.choice(['A', 'B', 'C'], rows),
        'date': pd.date_range('2024-01-01', periods=rows)
    })
    
    df.to_csv(file_path, index=False)
    return file_path

@pytest.fixture(scope="session")
def mixed_data_file(tmp_path_factory) -> Path:
    """Creates a file with mixed data types"""
    base_dir = tmp_path_factory.mktemp('test_data')
    file_path = base_dir / "mixed_data.csv"
    
    rows = config.DATA_SETTINGS['default_rows']
    df = pd.DataFrame({
        'int_col': np.random.randint(0, 1000, rows),
        'float_col': np.random.randn(rows),
        'str_col': [f"Value_{i}" for i in range(rows)],
        'date_col': pd.date_range('2024-01-01', periods=rows),
        'bool_col': np.random.choice([True, False], rows),
        'cat_col': pd.Categorical(np.random.choice(['A', 'B', 'C'], rows))
    })
    
    df.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def system_monitor():
    """Provides system resource monitoring"""
    class SystemMonitor:
        def __init__(self):
            self.initial_memory = psutil.Process().memory_info().rss
            self.start_time = time.time()
            
        def get_metrics(self) -> Dict[str, Any]:
            process = psutil.Process()
            current_memory = process.memory_info().rss
            
            return {
                'memory_used': current_memory - self.initial_memory,
                'memory_percent': process.memory_percent(),
                'cpu_percent': process.cpu_percent(),
                'elapsed_time': time.time() - self.start_time,
                'system_memory_available': psutil.virtual_memory().available,
                'system_cpu_percent': psutil.cpu_percent()
            }
    
    return SystemMonitor() 