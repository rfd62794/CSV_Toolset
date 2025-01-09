"""Tests for preferences backup and restore system."""
import pytest
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from tools.utils.preferences_backup import PreferencesBackup

@pytest.fixture
def backup_dir(tmp_path) -> Path:
    """Create temporary backup directory."""
    return tmp_path / "backups"

@pytest.fixture
def sample_preferences() -> Dict[str, Any]:
    """Sample preferences data for testing."""
    return {
        "version": "2.0",
        "preferences": {
            "Tool1": True,
            "Tool2": False
        },
        "categories": {
            "Category1": {
                "desc": "Test category",
                "icon": "📊",
                "tools": {
                    "Tool1": "Tool 1 description",
                    "Tool2": "Tool 2 description"
                }
            }
        },
        "timestamp": "20250112_143000"
    }

@pytest.fixture
def backup_system(backup_dir) -> PreferencesBackup:
    """Initialize backup system."""
    return PreferencesBackup(backup_dir)

def test_create_backup(backup_system, sample_preferences):
    """Test creating a backup."""
    assert backup_system.create_backup(sample_preferences)
    backups = list(backup_system.backup_dir.glob("preferences_*.json"))
    assert len(backups) == 1
    
    # Verify backup content
    backup_data = json.loads(backups[0].read_text())
    assert backup_data["version"] == "2.0"
    assert backup_data["data"] == sample_preferences
    assert "checksum" in backup_data
    assert "timestamp" in backup_data

def test_restore_backup(backup_system, sample_preferences):
    """Test restoring from backup."""
    # Create backup
    assert backup_system.create_backup(sample_preferences)
    
    # Get backup timestamp
    backups = backup_system.list_backups()
    assert len(backups) == 1
    timestamp = backups[0]["timestamp"]
    
    # Restore and verify
    restored = backup_system.restore_backup(timestamp)
    assert restored == sample_preferences

def test_restore_latest_backup(backup_system, sample_preferences):
    """Test restoring latest backup when no timestamp specified."""
    # Create multiple backups
    assert backup_system.create_backup(sample_preferences)
    time.sleep(0.1)  # Ensure different timestamps
    
    modified_prefs = sample_preferences.copy()
    modified_prefs["preferences"]["Tool1"] = False
    assert backup_system.create_backup(modified_prefs)
    
    # Restore latest
    restored = backup_system.restore_backup()
    assert restored == modified_prefs

def test_list_backups(backup_system, sample_preferences):
    """Test listing available backups."""
    # Create multiple backups
    assert backup_system.create_backup(sample_preferences)
    time.sleep(0.1)
    assert backup_system.create_backup(sample_preferences)
    
    # List and verify
    backups = backup_system.list_backups()
    assert len(backups) == 2
    for backup in backups:
        assert "timestamp" in backup
        assert "version" in backup
        assert "size" in backup
        assert "path" in backup

def test_verify_all_backups(backup_system, sample_preferences):
    """Test verifying all backups."""
    # Create valid backup
    assert backup_system.create_backup(sample_preferences)
    
    # Create invalid backup
    invalid_file = backup_system.backup_dir / "preferences_invalid.json"
    invalid_file.write_text("invalid json")
    
    # Verify all
    results = backup_system.verify_all_backups()
    assert len(results) == 2
    
    # One should be valid, one invalid
    valid_count = sum(1 for _, is_valid in results if is_valid)
    assert valid_count == 1

def test_cleanup_old_backups(backup_system, sample_preferences):
    """Test cleanup of old backups."""
    # Create more than max_backups
    for _ in range(backup_system.max_backups + 5):
        backup_system.create_backup(sample_preferences)
        time.sleep(0.1)  # Ensure different timestamps
    
    # Verify only max_backups remain
    backups = backup_system.list_backups()
    assert len(backups) == backup_system.max_backups
    
    # Verify they're the most recent ones
    timestamps = [b["timestamp"] for b in backups]
    assert sorted(timestamps) == timestamps

def test_backup_integrity(backup_system, sample_preferences):
    """Test backup data integrity."""
    # Create backup
    assert backup_system.create_backup(sample_preferences)
    
    # Get backup file
    backup_file = next(backup_system.backup_dir.glob("preferences_*.json"))
    
    # Modify backup file
    backup_data = json.loads(backup_file.read_text())
    backup_data["data"]["preferences"]["Tool1"] = not backup_data["data"]["preferences"]["Tool1"]
    backup_file.write_text(json.dumps(backup_data))
    
    # Attempt restore - should fail verification
    timestamp = backup_data["timestamp"]
    assert backup_system.restore_backup(timestamp) is None

def test_invalid_backup_dir(tmp_path):
    """Test handling of invalid backup directory."""
    # Create a file where the backup dir should be
    invalid_dir = tmp_path / "invalid"
    invalid_dir.write_text("not a directory")
    
    with pytest.raises(Exception):
        PreferencesBackup(invalid_dir)

def test_missing_backup(backup_system):
    """Test restoring non-existent backup."""
    assert backup_system.restore_backup("nonexistent") is None 