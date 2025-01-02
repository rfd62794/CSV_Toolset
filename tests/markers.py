import pytest

# Test type markers
pytest.mark.unit.description = "Unit tests for individual components"
pytest.mark.integration.description = "Integration tests between components"
pytest.mark.performance.description = "Performance and load testing"

# Component markers
pytest.mark.processor.description = "Tests for data processors"
pytest.mark.frame.description = "Tests for UI frames"
pytest.mark.widget.description = "Tests for UI widgets"
pytest.mark.utils.description = "Tests for utility functions"

# Feature markers
pytest.mark.file_io.description = "Tests for file operations"
pytest.mark.ui.description = "Tests for user interface"
pytest.mark.validation.description = "Tests for data validation"
pytest.mark.error_handling.description = "Tests for error handling"

# Performance markers
pytest.mark.slow.description = "Tests that take longer to run"
pytest.mark.memory_intensive.description = "Tests that use significant memory"
pytest.mark.large_files.description = "Tests with large data files"

# Data type markers
pytest.mark.numeric_data.description = "Tests with numeric data"
pytest.mark.categorical_data.description = "Tests with categorical data"
pytest.mark.temporal_data.description = "Tests with date/time data"
pytest.mark.mixed_data.description = "Tests with mixed data types" 