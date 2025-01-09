"""Preferences version control and migration system."""
import json
from enum import Enum
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from .performance_monitor import PerformanceMonitor

class PreferencesVersion(Enum):
    """Supported preferences versions."""
    V1_0 = "1.0"  # Initial version
    V1_1 = "1.1"  # Added categories
    V1_2 = "1.2"  # Added timestamps
    V2_0 = "2.0"  # Added validation and performance monitoring

    @classmethod
    def latest(cls) -> str:
        """Get latest version."""
        return cls.V2_0.value

    @classmethod
    def is_valid(cls, version: str) -> bool:
        """Check if version is valid."""
        return any(v.value == version for v in cls)

    @classmethod
    def get_migration_path(cls, from_version: str) -> List[str]:
        """Get ordered list of versions to migrate through."""
        if not cls.is_valid(from_version):
            return []
            
        versions = [v.value for v in cls]
        start_idx = versions.index(from_version)
        return versions[start_idx + 1:]

class PreferencesMigrator:
    """Handles preferences version migration."""
    
    _monitor = PerformanceMonitor()
    
    @classmethod
    def migrate(cls, data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Migrate preferences to latest version."""
        with cls._monitor.monitor_operation("PreferencesMigrator", "migrate"):
            try:
                current_version = data.get("version")
                if not current_version or not PreferencesVersion.is_valid(current_version):
                    return data, ["Invalid version"]
                
                if current_version == PreferencesVersion.latest():
                    return data, ["Already at latest version"]
                
                # Get migration path
                migration_path = PreferencesVersion.get_migration_path(current_version)
                if not migration_path:
                    return data, ["No migration path available"]
                
                # Apply migrations in sequence
                result = data.copy()
                notes = []
                
                for target_version in migration_path:
                    migration_func = cls._get_migration_func(target_version)
                    if migration_func:
                        result, step_notes = migration_func(result)
                        notes.extend(step_notes)
                    
                return result, notes
                
            except Exception as e:
                cls._monitor.log_error("migration_error", str(e))
                return data, [f"Migration failed: {str(e)}"]
    
    @classmethod
    def _get_migration_func(cls, target_version: str):
        """Get migration function for target version."""
        migrations = {
            "1.1": cls._migrate_1_0_to_1_1,
            "1.2": cls._migrate_1_1_to_1_2,
            "2.0": cls._migrate_1_2_to_2_0
        }
        return migrations.get(target_version)
    
    @staticmethod
    def _migrate_1_0_to_1_1(data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Migrate from v1.0 to v1.1 (add categories)."""
        notes = []
        result = data.copy()
        
        # Move tools to General category
        if "preferences" in result:
            result["categories"] = {
                "General": {
                    "desc": "General tools",
                    "icon": "🔧",
                    "tools": {
                        tool: f"{tool} description"
                        for tool in result["preferences"].keys()
                    }
                }
            }
            notes.append("Moved tools to General category")
        
        result["version"] = PreferencesVersion.V1_1.value
        return result, notes
    
    @staticmethod
    def _migrate_1_1_to_1_2(data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Migrate from v1.1 to v1.2 (add timestamps)."""
        notes = []
        result = data.copy()
        
        # Add timestamp if missing
        if "timestamp" not in result:
            result["timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")
            notes.append("Added timestamp")
        
        result["version"] = PreferencesVersion.V1_2.value
        return result, notes
    
    @staticmethod
    def _migrate_1_2_to_2_0(data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Migrate from v1.2 to v2.0 (add validation)."""
        notes = []
        result = data.copy()
        
        # Ensure all preferences are boolean
        prefs = result.get("preferences", {})
        for tool, state in prefs.items():
            if not isinstance(state, bool):
                prefs[tool] = bool(state)
                notes.append(f"Converted {tool} state to boolean")
        
        # Ensure all categories have required fields
        for cat, info in result.get("categories", {}).items():
            if not isinstance(info, dict):
                info = {}
                
            if "desc" not in info:
                info["desc"] = "Category description"
                notes.append(f"Added description to {cat}")
                
            if "icon" not in info:
                info["icon"] = "📁"
                notes.append(f"Added icon to {cat}")
                
            if "tools" not in info:
                info["tools"] = {}
                notes.append(f"Added tools dict to {cat}")
                
            result["categories"][cat] = info
        
        result["version"] = PreferencesVersion.V2_0.value
        return result, notes 