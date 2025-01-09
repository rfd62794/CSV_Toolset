"""Tests for preferences versioning system."""
import pytest
from pathlib import Path
from datetime import datetime
from tools.preferences_version import (
    PreferencesVersion,
    PreferencesMigrator,
    PreferencesVersionManager
)

@pytest.fixture
def v1_0_data():
    """Sample v1.0 preferences data."""
    return {
        "preferences": {
            "CSV Inspector": True,
            "Data Profiler": False
        }
    }

@pytest.fixture
def v1_1_data():
    """Sample v1.1 preferences data with categories."""
    return {
        "version": "1.1",
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
        }
    }

@pytest.fixture
def v1_2_data():
    """Sample v1.2 preferences data with timestamps."""
    return {
        "version": "1.2",
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
        "timestamp": "20250111_123456"
    }

@pytest.fixture
def v2_0_data():
    """Sample v2.0 preferences data with validation."""
    return {
        "version": "2.0",
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
        "timestamp": "20250111_123456"
    }

def test_preferences_version_latest():
    """Test getting latest version."""
    assert PreferencesVersion.latest() == "2.0"

def test_preferences_version_is_valid():
    """Test version validation."""
    assert PreferencesVersion.is_valid("1.0")
    assert PreferencesVersion.is_valid("2.0")
    assert not PreferencesVersion.is_valid("0.9")
    assert not PreferencesVersion.is_valid("3.0")

def test_migrate_v1_0_to_v1_1(v1_0_data):
    """Test migration from v1.0 to v1.1."""
    data, notes = PreferencesMigrator._migrate_1_0_to_1_1(v1_0_data)
    assert "categories" in data
    assert "General" in data["categories"]
    assert "tools" in data["categories"]["General"]
    assert "Moved tools to General category" in notes

def test_migrate_v1_1_to_v1_2(v1_1_data):
    """Test migration from v1.1 to v1.2."""
    data, notes = PreferencesMigrator._migrate_1_1_to_1_2(v1_1_data)
    assert "timestamp" in data
    assert "Added timestamp" in notes

def test_migrate_v1_2_to_v2_0(v1_2_data):
    """Test migration from v1.2 to v2.0."""
    data, notes = PreferencesMigrator._migrate_1_2_to_2_0(v1_2_data)
    assert data["version"] == "2.0"
    assert isinstance(data["preferences"]["CSV Inspector"], bool)

def test_full_migration_chain(v1_0_data):
    """Test complete migration from v1.0 to latest."""
    data, notes = PreferencesMigrator.migrate(v1_0_data)
    assert data["version"] == PreferencesVersion.latest()
    assert "categories" in data
    assert "timestamp" in data
    assert len(notes) > 0

def test_version_manager_needs_migration(v1_0_data, v2_0_data):
    """Test version manager migration detection."""
    manager = PreferencesVersionManager(Path("test.json"))
    assert manager.needs_migration(v1_0_data)
    assert not manager.needs_migration(v2_0_data)

def test_version_manager_migrate_if_needed(v1_0_data):
    """Test version manager migration handling."""
    manager = PreferencesVersionManager(Path("test.json"))
    data, notes = manager.migrate_if_needed(v1_0_data)
    assert data["version"] == PreferencesVersion.latest()
    assert notes is not None
    assert len(notes) > 0

def test_invalid_version_handling():
    """Test handling of invalid version numbers."""
    data = {"version": "invalid", "preferences": {}}
    data, notes = PreferencesMigrator.migrate(data)
    assert "Unknown version" in notes[0]
    assert data["version"] == PreferencesVersion.latest()

def test_missing_version_handling():
    """Test handling of missing version field."""
    data = {"preferences": {}}
    data, notes = PreferencesMigrator.migrate(data)
    assert data["version"] == PreferencesVersion.latest()

def test_malformed_categories_handling(v1_1_data):
    """Test handling of malformed category data."""
    v1_1_data["categories"]["Bad"] = "not a dict"
    data, notes = PreferencesMigrator.migrate(v1_1_data)
    assert isinstance(data["categories"]["Bad"], dict)
    assert "Fixed invalid category" in " ".join(notes)

def test_boolean_conversion():
    """Test conversion of non-boolean preference values."""
    data = {
        "version": "1.2",
        "preferences": {
            "Tool1": 1,
            "Tool2": "true",
            "Tool3": 0
        }
    }
    data, notes = PreferencesMigrator.migrate(data)
    assert isinstance(data["preferences"]["Tool1"], bool)
    assert isinstance(data["preferences"]["Tool2"], bool)
    assert isinstance(data["preferences"]["Tool3"], bool) 