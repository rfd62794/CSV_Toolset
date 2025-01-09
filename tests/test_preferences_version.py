"""Tests for preferences version control system."""
import pytest
from datetime import datetime
from typing import Dict, Any
from tools.utils.preferences_version import PreferencesVersion, PreferencesMigrator

@pytest.fixture
def v1_0_data() -> Dict[str, Any]:
    """Sample v1.0 preferences data."""
    return {
        "version": "1.0",
        "preferences": {
            "Tool1": True,
            "Tool2": False
        }
    }

@pytest.fixture
def v1_1_data() -> Dict[str, Any]:
    """Sample v1.1 preferences data with categories."""
    return {
        "version": "1.1",
        "preferences": {
            "Tool1": True,
            "Tool2": False
        },
        "categories": {
            "General": {
                "desc": "General tools",
                "icon": "🔧",
                "tools": {
                    "Tool1": "Tool 1 description",
                    "Tool2": "Tool 2 description"
                }
            }
        }
    }

@pytest.fixture
def v1_2_data() -> Dict[str, Any]:
    """Sample v1.2 preferences data with timestamps."""
    return {
        "version": "1.2",
        "preferences": {
            "Tool1": True,
            "Tool2": False
        },
        "categories": {
            "General": {
                "desc": "General tools",
                "icon": "🔧",
                "tools": {
                    "Tool1": "Tool 1 description",
                    "Tool2": "Tool 2 description"
                }
            }
        },
        "timestamp": "20250112_150000"
    }

@pytest.fixture
def v2_0_data() -> Dict[str, Any]:
    """Sample v2.0 preferences data with validation."""
    return {
        "version": "2.0",
        "preferences": {
            "Tool1": True,
            "Tool2": False
        },
        "categories": {
            "General": {
                "desc": "General tools",
                "icon": "🔧",
                "tools": {
                    "Tool1": "Tool 1 description",
                    "Tool2": "Tool 2 description"
                }
            }
        },
        "timestamp": "20250112_150000"
    }

def test_preferences_version_latest():
    """Test getting latest version."""
    assert PreferencesVersion.latest() == "2.0"

def test_preferences_version_is_valid():
    """Test version validation."""
    assert PreferencesVersion.is_valid("1.0")
    assert PreferencesVersion.is_valid("1.1")
    assert PreferencesVersion.is_valid("1.2")
    assert PreferencesVersion.is_valid("2.0")
    assert not PreferencesVersion.is_valid("0.9")
    assert not PreferencesVersion.is_valid("3.0")
    assert not PreferencesVersion.is_valid("invalid")

def test_get_migration_path():
    """Test getting migration path."""
    assert PreferencesVersion.get_migration_path("1.0") == ["1.1", "1.2", "2.0"]
    assert PreferencesVersion.get_migration_path("1.1") == ["1.2", "2.0"]
    assert PreferencesVersion.get_migration_path("1.2") == ["2.0"]
    assert PreferencesVersion.get_migration_path("2.0") == []
    assert PreferencesVersion.get_migration_path("invalid") == []

def test_migrate_v1_0_to_v1_1(v1_0_data):
    """Test migration from v1.0 to v1.1."""
    result, notes = PreferencesMigrator._migrate_1_0_to_1_1(v1_0_data)
    assert result["version"] == "1.1"
    assert "categories" in result
    assert "General" in result["categories"]
    assert "tools" in result["categories"]["General"]
    assert "Moved tools to General category" in notes

def test_migrate_v1_1_to_v1_2(v1_1_data):
    """Test migration from v1.1 to v1.2."""
    result, notes = PreferencesMigrator._migrate_1_1_to_1_2(v1_1_data)
    assert result["version"] == "1.2"
    assert "timestamp" in result
    assert "Added timestamp" in notes

def test_migrate_v1_2_to_v2_0(v1_2_data):
    """Test migration from v1.2 to v2.0."""
    # Add some invalid data to test conversion
    v1_2_data["preferences"]["Tool3"] = "not_boolean"
    v1_2_data["categories"]["Invalid"] = "not_dict"
    
    result, notes = PreferencesMigrator._migrate_1_2_to_2_0(v1_2_data)
    assert result["version"] == "2.0"
    assert all(isinstance(v, bool) for v in result["preferences"].values())
    assert all(isinstance(v, dict) for v in result["categories"].values())
    assert any("Converted Tool3 state to boolean" in note for note in notes)

def test_full_migration_chain(v1_0_data):
    """Test migrating from v1.0 to latest through all versions."""
    result, notes = PreferencesMigrator.migrate(v1_0_data)
    assert result["version"] == PreferencesVersion.latest()
    assert "categories" in result
    assert "timestamp" in result
    assert len(notes) > 0

def test_migrate_invalid_version():
    """Test migrating with invalid version."""
    data = {"version": "invalid"}
    result, notes = PreferencesMigrator.migrate(data)
    assert result == data
    assert "Invalid version" in notes

def test_migrate_missing_version():
    """Test migrating without version field."""
    data = {"preferences": {}}
    result, notes = PreferencesMigrator.migrate(data)
    assert result == data
    assert "Invalid version" in notes

def test_migrate_latest_version(v2_0_data):
    """Test migrating already latest version."""
    result, notes = PreferencesMigrator.migrate(v2_0_data)
    assert result == v2_0_data
    assert "Already at latest version" in notes

def test_migrate_with_errors():
    """Test migration error handling."""
    # Create invalid data that will cause migration to fail
    data = {
        "version": "1.0",
        "preferences": None  # This will cause migration to fail
    }
    result, notes = PreferencesMigrator.migrate(data)
    assert "Migration failed" in notes[0] 