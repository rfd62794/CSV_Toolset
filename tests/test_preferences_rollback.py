"""Tests for preferences rollback system."""
import pytest
from pathlib import Path
import json
import shutil
from datetime import datetime
from tools.preferences_rollback import PreferencesRollback
from tools.preferences_version import PreferencesVersion

@pytest.fixture
def temp_prefs_dir(tmp_path):
    """Create temporary preferences directory."""
    prefs_dir = tmp_path / ".csv_toolkit"
    prefs_dir.mkdir()
    yield prefs_dir
    shutil.rmtree(prefs_dir)

@pytest.fixture
def rollback_manager(temp_prefs_dir):
    """Create rollback manager with temporary directory."""
    prefs_path = temp_prefs_dir / "preferences.json"
    return PreferencesRollback(prefs_path)

@pytest.fixture
def sample_data():
    """Sample preferences data."""
    return {
        "version": "2.0",
        "preferences": {
            "Tool1": True,
            "Tool2": False
        },
        "categories": {
            "Category1": {
                "desc": "Test category",
                "icon": "🔧",
                "tools": {
                    "Tool1": "Description 1",
                    "Tool2": "Description 2"
                }
            }
        },
        "timestamp": "20250111_123456"
    }

def test_create_backup(rollback_manager, sample_data):
    """Test backup creation."""
    backup_path = rollback_manager.create_backup(sample_data)
    assert backup_path is not None
    assert backup_path.exists()
    
    with open(backup_path) as f:
        backup_data = json.load(f)
        assert "timestamp" in backup_data
        assert backup_data["version"] == "2.0"
        assert backup_data["data"] == sample_data

def test_backup_rotation(rollback_manager, sample_data):
    """Test backup rotation with MAX_BACKUPS limit."""
    # Create more backups than MAX_BACKUPS
    paths = []
    for i in range(rollback_manager.MAX_BACKUPS + 2):
        path = rollback_manager.create_backup(sample_data)
        paths.append(path)
        
    # Check only MAX_BACKUPS files exist
    backups = list(rollback_manager.backup_dir.glob(f"*{rollback_manager.BACKUP_SUFFIX}"))
    assert len(backups) == rollback_manager.MAX_BACKUPS
    
    # Check oldest backups were removed
    assert not paths[0].exists()
    assert not paths[1].exists()
    assert paths[-1].exists()

def test_rollback_to_version(rollback_manager, sample_data):
    """Test rolling back to a specific version."""
    # Create backups for different versions
    v1_data = {**sample_data, "version": "1.0"}
    v2_data = {**sample_data, "version": "2.0"}
    
    rollback_manager.create_backup(v1_data)
    rollback_manager.create_backup(v2_data)
    
    # Test rollback to v1.0
    data, notes = rollback_manager.rollback_to_version("1.0")
    assert data is not None
    assert data["version"] == "1.0"
    assert "Rolled back to version 1.0" in notes[0]
    
    # Test rollback to invalid version
    data, notes = rollback_manager.rollback_to_version("0.9")
    assert data is None
    assert "Invalid target version" in notes[0]

def test_get_available_versions(rollback_manager, sample_data):
    """Test getting list of available versions."""
    # Create backups for different versions
    versions = ["1.0", "1.1", "2.0"]
    for version in versions:
        data = {**sample_data, "version": version}
        rollback_manager.create_backup(data)
        
    available = rollback_manager.get_available_versions()
    assert set(available) == set(versions)

def test_find_version_backup(rollback_manager, sample_data):
    """Test finding latest backup for a version."""
    # Create multiple backups of same version
    data = {**sample_data, "version": "1.0"}
    path1 = rollback_manager.create_backup(data)
    path2 = rollback_manager.create_backup(data)
    
    backup = rollback_manager._find_version_backup("1.0")
    assert backup == path2  # Should return most recent

def test_restore_latest_backup(rollback_manager, sample_data):
    """Test restoring from latest backup."""
    # Create multiple backups
    v1_data = {**sample_data, "version": "1.0"}
    v2_data = {**sample_data, "version": "2.0"}
    
    rollback_manager.create_backup(v1_data)
    rollback_manager.create_backup(v2_data)
    
    # Test restore
    data, notes = rollback_manager.restore_latest_backup()
    assert data is not None
    assert data["version"] == "2.0"
    assert "Restored from latest backup" in notes[0]

def test_error_handling(rollback_manager):
    """Test error handling in rollback operations."""
    # Test restore with no backups
    data, notes = rollback_manager.restore_latest_backup()
    assert data is None
    assert "No backups available" in notes[0]
    
    # Test rollback to non-existent version
    data, notes = rollback_manager.rollback_to_version("3.0")
    assert data is None
    assert "Invalid target version" in notes[0]

def test_backup_data_integrity(rollback_manager, sample_data):
    """Test backup data integrity."""
    backup_path = rollback_manager.create_backup(sample_data)
    
    # Verify backup structure
    with open(backup_path) as f:
        backup_data = json.load(f)
        assert isinstance(backup_data["timestamp"], str)
        assert isinstance(backup_data["version"], str)
        assert isinstance(backup_data["data"], dict)
        assert backup_data["data"] == sample_data

def test_backup_directory_creation(temp_prefs_dir):
    """Test backup directory creation."""
    prefs_path = temp_prefs_dir / "preferences.json"
    backup_dir = temp_prefs_dir / ".backups"
    
    assert not backup_dir.exists()
    PreferencesRollback(prefs_path)
    assert backup_dir.exists()

def test_cleanup_error_handling(rollback_manager, sample_data, monkeypatch):
    """Test error handling during cleanup."""
    def mock_unlink(*args):
        raise OSError("Test error")
        
    monkeypatch.setattr(Path, "unlink", mock_unlink)
    
    # Should not raise exception
    for _ in range(rollback_manager.MAX_BACKUPS + 1):
        rollback_manager.create_backup(sample_data) 