"""Preferences versioning and migration utilities."""
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import logging
from pathlib import Path
from datetime import datetime
from .preferences_rollback import PreferencesRollback

logger = logging.getLogger(__name__)

class PreferencesVersion(Enum):
    """Enum for preferences file versions."""
    V1_0 = "1.0"  # Initial version
    V1_1 = "1.1"  # Added categories
    V1_2 = "1.2"  # Added timestamps
    V2_0 = "2.0"  # Current version with validation
    
    @classmethod
    def latest(cls) -> str:
        """Get the latest version."""
        return sorted(cls._value2member_map_.keys())[-1]
        
    @classmethod
    def is_valid(cls, version: str) -> bool:
        """Check if version is valid."""
        return version in cls._value2member_map_
        
    @classmethod
    def get_previous_version(cls, version: str) -> Optional[str]:
        """Get the previous version in the sequence."""
        if not cls.is_valid(version):
            return None
        versions = sorted(cls._value2member_map_.keys())
        try:
            idx = versions.index(version)
            return versions[idx - 1] if idx > 0 else None
        except ValueError:
            return None

class PreferencesMigrator:
    """Handles preferences version migrations."""
    
    @classmethod
    def migrate(cls, data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """
        Migrate preferences data to latest version.
        Returns (migrated_data, migration_notes).
        """
        version = data.get("version", "1.0")
        notes = []
        
        if not PreferencesVersion.is_valid(version):
            notes.append(f"Unknown version {version}, assuming 1.0")
            version = "1.0"
            
        # Apply migrations in sequence
        if version == "1.0":
            data, v1_notes = cls._migrate_1_0_to_1_1(data)
            notes.extend(v1_notes)
            version = "1.1"
            
        if version == "1.1":
            data, v2_notes = cls._migrate_1_1_to_1_2(data)
            notes.extend(v2_notes)
            version = "1.2"
            
        if version == "1.2":
            data, v3_notes = cls._migrate_1_2_to_2_0(data)
            notes.extend(v3_notes)
            
        return data, notes
        
    @staticmethod
    def _migrate_1_0_to_1_1(data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Migrate from v1.0 to v1.1 (add categories)."""
        notes = []
        if "categories" not in data:
            data["categories"] = {
                "General": {
                    "desc": "General tools",
                    "icon": "🔧",
                    "tools": {}
                }
            }
            # Move all tools to General category
            for tool, state in data.get("preferences", {}).items():
                data["categories"]["General"]["tools"][tool] = "Tool description"
            notes.append("Moved tools to General category")
            
        return data, notes
        
    @staticmethod
    def _migrate_1_1_to_1_2(data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Migrate from v1.1 to v1.2 (add timestamps)."""
        notes = []
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")
            notes.append("Added timestamp")
            
        return data, notes
        
    @staticmethod
    def _migrate_1_2_to_2_0(data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Migrate from v1.2 to v2.0 (add validation)."""
        notes = []
        
        # Ensure all preferences are boolean
        prefs = data.get("preferences", {})
        for tool, state in prefs.items():
            if not isinstance(state, bool):
                prefs[tool] = bool(state)
                notes.append(f"Converted {tool} state to boolean")
                
        # Ensure all categories have required fields
        for cat, info in data.get("categories", {}).items():
            if not isinstance(info, dict):
                info = {
                    "desc": "Category description",
                    "icon": "📁",
                    "tools": {}
                }
                data["categories"][cat] = info
                notes.append(f"Fixed invalid category: {cat}")
            else:
                for field in ["desc", "icon", "tools"]:
                    if field not in info:
                        info[field] = {
                            "desc": "Category description",
                            "icon": "📁",
                            "tools": {}
                        }[field]
                        notes.append(f"Added missing {field} to category {cat}")
                        
        data["version"] = PreferencesVersion.V2_0.value
        return data, notes

class PreferencesVersionManager:
    """Manages preferences versioning and migrations."""
    
    def __init__(self, path: Path):
        self.path = path
        self.version = PreferencesVersion.V2_0
        self.rollback = PreferencesRollback(path)
        
    def get_version(self, data: Dict[str, Any]) -> str:
        """Get version from preferences data."""
        return data.get("version", "1.0")
        
    def needs_migration(self, data: Dict[str, Any]) -> bool:
        """Check if preferences need migration."""
        current = self.get_version(data)
        return current != self.version.value
        
    def migrate_if_needed(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[List[str]]]:
        """
        Migrate preferences if needed.
        Returns (migrated_data, migration_notes or None).
        """
        if self.needs_migration(data):
            # Create backup before migration
            if not self.rollback.create_backup(data):
                logger.warning("Failed to create backup before migration")
                
            try:
                migrated, notes = PreferencesMigrator.migrate(data)
                logger.info("Migrated preferences:\n" + "\n".join(notes))
                return migrated, notes
            except Exception as e:
                logger.error(f"Migration failed: {str(e)}")
                # Try to restore from backup
                restored, restore_notes = self.rollback.restore_latest_backup()
                if restored:
                    logger.info("Restored from backup after failed migration")
                    return restored, ["Migration failed, restored from backup"]
                return data, [f"Migration failed: {str(e)}"]
        return data, None
        
    def rollback_to_version(self, version: str) -> Tuple[Optional[Dict[str, Any]], List[str]]:
        """
        Rollback to a specific version.
        Returns (rolled_back_data, notes) or (None, error_notes).
        """
        return self.rollback.rollback_to_version(version)
        
    def get_available_versions(self) -> List[str]:
        """Get list of versions available for rollback."""
        return self.rollback.get_available_versions()
        
    def restore_latest_backup(self) -> Tuple[Optional[Dict[str, Any]], List[str]]:
        """Restore from most recent backup."""
        return self.rollback.restore_latest_backup() 