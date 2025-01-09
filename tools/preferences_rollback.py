"""Preferences rollback and recovery utilities."""
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import json
import shutil
import logging
from datetime import datetime
from .preferences_version import PreferencesVersion

logger = logging.getLogger(__name__)

class PreferencesRollback:
    """Manages preferences rollback and recovery."""
    
    BACKUP_SUFFIX = ".backup"
    MAX_BACKUPS = 5
    
    def __init__(self, path: Path):
        self.path = path
        self.backup_dir = path.parent / ".backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def create_backup(self, data: Dict[str, Any]) -> Optional[Path]:
        """Create a backup before migration."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"preferences_{timestamp}{self.BACKUP_SUFFIX}"
            
            # Add version info to backup
            backup_data = {
                "timestamp": timestamp,
                "version": data.get("version", "1.0"),
                "data": data
            }
            
            with open(backup_path, "w") as f:
                json.dump(backup_data, f, indent=2)
                
            self._cleanup_old_backups()
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")
            return None
            
    def rollback_to_version(self, target_version: str) -> Tuple[Optional[Dict[str, Any]], List[str]]:
        """
        Rollback to a specific version.
        Returns (rolled_back_data, notes) or (None, error_notes).
        """
        try:
            if not PreferencesVersion.is_valid(target_version):
                return None, [f"Invalid target version: {target_version}"]
                
            # Find latest backup with target version
            backup = self._find_version_backup(target_version)
            if not backup:
                return None, [f"No backup found for version {target_version}"]
                
            # Load and verify backup
            with open(backup) as f:
                backup_data = json.load(f)
                
            if backup_data["version"] != target_version:
                return None, ["Backup version mismatch"]
                
            # Restore from backup
            data = backup_data["data"]
            with open(self.path, "w") as f:
                json.dump(data, f, indent=2)
                
            return data, [f"Rolled back to version {target_version}"]
            
        except Exception as e:
            logger.error(f"Rollback failed: {str(e)}")
            return None, [f"Rollback failed: {str(e)}"]
            
    def get_available_versions(self) -> List[str]:
        """Get list of versions available for rollback."""
        versions = set()
        for backup in self.backup_dir.glob(f"*{self.BACKUP_SUFFIX}"):
            try:
                with open(backup) as f:
                    data = json.load(f)
                    if "version" in data:
                        versions.add(data["version"])
            except Exception:
                continue
        return sorted(list(versions))
        
    def _find_version_backup(self, version: str) -> Optional[Path]:
        """Find latest backup for specified version."""
        latest_backup = None
        latest_timestamp = None
        
        for backup in self.backup_dir.glob(f"*{self.BACKUP_SUFFIX}"):
            try:
                with open(backup) as f:
                    data = json.load(f)
                    
                if data["version"] == version:
                    timestamp = data["timestamp"]
                    if not latest_timestamp or timestamp > latest_timestamp:
                        latest_backup = backup
                        latest_timestamp = timestamp
                        
            except Exception:
                continue
                
        return latest_backup
        
    def _cleanup_old_backups(self):
        """Remove old backups keeping only MAX_BACKUPS."""
        backups = sorted(
            self.backup_dir.glob(f"*{self.BACKUP_SUFFIX}"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        for backup in backups[self.MAX_BACKUPS:]:
            try:
                backup.unlink()
            except Exception as e:
                logger.warning(f"Failed to remove old backup {backup}: {str(e)}")
                
    def restore_latest_backup(self) -> Tuple[Optional[Dict[str, Any]], List[str]]:
        """
        Restore from most recent backup.
        Returns (restored_data, notes) or (None, error_notes).
        """
        try:
            backups = sorted(
                self.backup_dir.glob(f"*{self.BACKUP_SUFFIX}"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            
            if not backups:
                return None, ["No backups available"]
                
            # Load latest backup
            with open(backups[0]) as f:
                backup_data = json.load(f)
                
            # Restore data
            data = backup_data["data"]
            with open(self.path, "w") as f:
                json.dump(data, f, indent=2)
                
            return data, ["Restored from latest backup"]
            
        except Exception as e:
            logger.error(f"Restore failed: {str(e)}")
            return None, [f"Restore failed: {str(e)}"] 