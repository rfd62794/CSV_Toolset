"""Tests for preferences validation system."""
import pytest
from pathlib import Path
import json
from datetime import datetime
from tools.preferences_validator import PreferencesValidator

@pytest.fixture
def valid_preferences():
    """Sample valid preferences data."""
    return {
        "version": "1.0",
        "preferences": {
            "CSV Inspector": True,
            "Data Profiler": False
        },
        "categories": {
            "Analysis": {
                "desc": "Analysis tools",
                "icon": "📊",
                "tools": {
                    "CSV Inspector": "Inspect CSV files",
                    "Data Profiler": "Profile data"
                }
            }
        },
        "timestamp": "20250109_123456"
    }

@pytest.fixture
def invalid_preferences():
    """Sample invalid preferences data."""
    return {
        "version": "invalid",
        "preferences": {
            "Tool1": "not_boolean",
            123: True  # Invalid key type
        },
        "categories": {
            "Bad Category": "not_dict",
            "": {}  # Empty category name
        }
    }

def test_validate_valid_preferences(valid_preferences):
    """Test validation of valid preferences."""
    assert PreferencesValidator.validate(valid_preferences)

def test_validate_invalid_preferences(invalid_preferences):
    """Test validation of invalid preferences."""
    assert not PreferencesValidator.validate(invalid_preferences)

def test_sanitize_valid_preferences(valid_preferences):
    """Test sanitization of already valid preferences."""
    sanitized = PreferencesValidator.sanitize(valid_preferences)
    assert PreferencesValidator.validate(sanitized)
    assert sanitized == valid_preferences

def test_sanitize_invalid_preferences(invalid_preferences):
    """Test sanitization of invalid preferences."""
    sanitized = PreferencesValidator.sanitize(invalid_preferences)
    assert PreferencesValidator.validate(sanitized)
    assert "version" in sanitized
    assert isinstance(sanitized["preferences"], dict)
    assert all(isinstance(k, str) for k in sanitized["preferences"].keys())
    assert all(isinstance(v, bool) for v in sanitized["preferences"].values())

def test_missing_required_fields():
    """Test handling of missing required fields."""
    data = {}
    sanitized = PreferencesValidator.sanitize(data)
    assert PreferencesValidator.validate(sanitized)
    assert all(field in sanitized for field in ["version", "preferences", "categories", "timestamp"])

def test_invalid_category_structure():
    """Test handling of invalid category structure."""
    data = {
        "version": "1.0",
        "preferences": {},
        "categories": {
            "Test": {
                "desc": 123,  # Invalid type
                "tools": None  # Invalid type
            }
        },
        "timestamp": "20250109_123456"
    }
    sanitized = PreferencesValidator.sanitize(data)
    assert PreferencesValidator.validate(sanitized)
    assert isinstance(sanitized["categories"]["Test"]["desc"], str)
    assert isinstance(sanitized["categories"]["Test"]["tools"], dict)

def test_invalid_tool_names():
    """Test handling of invalid tool names."""
    data = {
        "version": "1.0",
        "preferences": {
            "": True,  # Empty name
            " ": False,  # Whitespace name
            123: True  # Non-string name
        },
        "timestamp": "20250109_123456"
    }
    sanitized = PreferencesValidator.sanitize(data)
    assert PreferencesValidator.validate(sanitized)
    assert all(name.strip() for name in sanitized["preferences"].keys())

def test_load_and_validate_missing_file(tmp_path):
    """Test loading preferences from non-existent file."""
    path = tmp_path / "nonexistent.json"
    assert PreferencesValidator.load_and_validate(path) is None

def test_load_and_validate_invalid_json(tmp_path):
    """Test loading invalid JSON file."""
    path = tmp_path / "invalid.json"
    path.write_text("invalid json content")
    assert PreferencesValidator.load_and_validate(path) is None

def test_save_validated_preferences(tmp_path, valid_preferences):
    """Test saving valid preferences."""
    path = tmp_path / "preferences.json"
    assert PreferencesValidator.save_validated(path, valid_preferences)
    assert path.exists()
    loaded = json.loads(path.read_text())
    assert PreferencesValidator.validate(loaded)

def test_save_validated_invalid_preferences(tmp_path, invalid_preferences):
    """Test saving invalid preferences (should be sanitized)."""
    path = tmp_path / "preferences.json"
    assert PreferencesValidator.save_validated(path, invalid_preferences)
    assert path.exists()
    loaded = json.loads(path.read_text())
    assert PreferencesValidator.validate(loaded)

def test_timestamp_format():
    """Test timestamp format validation."""
    data = {
        "version": "1.0",
        "preferences": {},
        "categories": {},
        "timestamp": "invalid_format"
    }
    assert not PreferencesValidator.validate(data)
    sanitized = PreferencesValidator.sanitize(data)
    assert PreferencesValidator.validate(sanitized)
    assert len(sanitized["timestamp"]) == 15  # YYYYMMDD_HHMMSS

def test_version_format():
    """Test version format validation."""
    data = {
        "version": "1",  # Invalid format
        "preferences": {},
        "categories": {},
        "timestamp": "20250109_123456"
    }
    assert not PreferencesValidator.validate(data)
    sanitized = PreferencesValidator.sanitize(data)
    assert PreferencesValidator.validate(sanitized)
    assert sanitized["version"].count(".") == 1 