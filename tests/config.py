from pathlib import Path
from typing import Dict, Any

class TestConfig:
    """Configuration for test suite"""
    
    # Test data settings
    DATA_SETTINGS = {
        'default_rows': 1000,
        'preview_rows': 5,
        'large_file_rows': 100000,
        'random_seed': 42
    }
    
    # Test file settings
    FILE_SETTINGS = {
        'encoding': 'utf-8',
        'chunk_size': 1000,
        'temp_dir': 'test_data'
    }
    
    # Test case categories
    TEST_CATEGORIES = {
        'unit': ['processor', 'frame'],
        'integration': ['file_io', 'ui'],
        'performance': ['large_files', 'memory']
    }
    
    # Test data types to verify
    DATA_TYPES = {
        'numeric': ['int64', 'float64'],
        'categorical': ['object', 'category'],
        'temporal': ['datetime64[ns]'],
        'boolean': ['bool']
    }
    
    @staticmethod
    def get_test_data_dir() -> Path:
        """Gets test data directory"""
        data_dir = Path(__file__).parent / 'test_data'
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir 