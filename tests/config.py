from pathlib import Path
from typing import Dict, Any
import psutil
import os
import sys

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
    
    # Performance test settings
    PERFORMANCE_SETTINGS = {
        'timeout': 60,  # seconds
        'max_memory': int(psutil.virtual_memory().total * 0.5),  # 50% of system RAM
        'large_file_size': 1024 * 1024 * 100,  # 100MB
        'stress_test_iterations': 100,
        'benchmark_rounds': 5,
        'memory_check_interval': 0.1,  # seconds
        'performance_thresholds': {
            'load_time': 2.0,  # seconds
            'process_time': 5.0,  # seconds
            'memory_usage': 1024 * 1024 * 500,  # 500MB
            'cpu_usage': 80  # percent
        }
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
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Gets system information for test context"""
        return {
            'cpu_count': os.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent,
            'platform': sys.platform
        } 