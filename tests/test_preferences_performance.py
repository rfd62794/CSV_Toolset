"""Tests for preferences system performance."""
import pytest
import time
import psutil
from pathlib import Path
from typing import Dict, Any
from .test_performance_base import BasePerformanceTest
from tools.preferences_validator import PreferencesValidator
from tools.utils.performance_monitor import PerformanceMonitor

class TestPreferencesPerformance(BasePerformanceTest):
    """Test suite for preferences system performance."""
    
    @pytest.fixture
    def large_preferences(self) -> Dict[str, Any]:
        """Generate large preferences dataset for testing."""
        return {
            "version": "2.0",
            "preferences": {
                f"Tool{i}": i % 2 == 0 
                for i in range(1000)
            },
            "categories": {
                f"Category{i}": {
                    "desc": f"Category {i} description",
                    "icon": "📊",
                    "tools": {
                        f"Tool{j}": f"Tool {j} description"
                        for j in range(i*100, (i+1)*100)
                    }
                }
                for i in range(10)
            },
            "timestamp": "20250109_123456"
        }
    
    def test_validation_performance(self, large_preferences):
        """Test validation performance with large dataset."""
        metrics = self.benchmark_operation(
            PreferencesValidator.validate,
            large_preferences
        )
        self.verify_performance_metrics(metrics)
    
    def test_sanitization_performance(self, large_preferences):
        """Test sanitization performance with large dataset."""
        # Corrupt some data to test sanitization
        corrupted = large_preferences.copy()
        corrupted["preferences"].update({
            "InvalidTool": "not_boolean",
            123: True
        })
        
        metrics = self.benchmark_operation(
            PreferencesValidator.sanitize,
            corrupted
        )
        self.verify_performance_metrics(metrics)
    
    def test_load_save_performance(self, large_preferences, tmp_path):
        """Test preferences load/save performance."""
        test_file = tmp_path / "test_preferences.json"
        
        # Test save performance
        save_metrics = self.benchmark_operation(
            PreferencesValidator.save_validated,
            test_file,
            large_preferences
        )
        self.verify_performance_metrics(save_metrics)
        
        # Test load performance
        load_metrics = self.benchmark_operation(
            PreferencesValidator.load_and_validate,
            test_file
        )
        self.verify_performance_metrics(load_metrics)
    
    def test_memory_usage_validation(self, large_preferences):
        """Test memory usage during validation."""
        memory_used, _ = self.measure_memory_usage(
            PreferencesValidator.validate,
            large_preferences
        )
        
        # Memory usage should not exceed 50MB for validation
        assert memory_used < 50 * 1024 * 1024, \
            f"Memory usage ({memory_used/1024/1024:.1f}MB) exceeds 50MB threshold"
    
    def test_memory_usage_sanitization(self, large_preferences):
        """Test memory usage during sanitization."""
        memory_used, _ = self.measure_memory_usage(
            PreferencesValidator.sanitize,
            large_preferences
        )
        
        # Memory usage should not exceed 50MB for sanitization
        assert memory_used < 50 * 1024 * 1024, \
            f"Memory usage ({memory_used/1024/1024:.1f}MB) exceeds 50MB threshold" 