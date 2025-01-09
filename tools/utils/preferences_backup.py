"""Preferences backup and restore system with versioning."""
import json
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from .performance_monitor import PerformanceMonitor

class PreferencesBackup:
    """Manages preferences backup and restore operations."""
    
    _monitor = PerformanceMonitor()
    
    def __init__(self, backup_dir: Path):
        """Initialize backup system with directory."""
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.max_backups = 10  # Keep last 10 backups
        self.backup_format = "%Y%m%d_%H%M%S"
    
    def create_backup(self, preferences: Dict[str, Any]) -> bool:
        """Create a new backup of preferences."""
        with self._monitor.monitor_operation("PreferencesBackup", "create"):
            try:
                # Generate backup filename with timestamp
                timestamp = datetime.now().strftime(self.backup_format)
                backup_file = self.backup_dir / f"preferences_{timestamp}.json"
                
                # Save backup with metadata
                backup_data = {
                    "timestamp": timestamp,
                    "version": preferences.get("version", "unknown"),
                    "data": preferences,
                    "checksum": self._calculate_checksum(preferences)
                }
                
                backup_file.write_text(json.dumps(backup_data, indent=2))
                self._cleanup_old_backups()
                return True
                
            except Exception as e:
                self._monitor.log_error("backup_error", str(e))
                return False
    
    def restore_backup(self, timestamp: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Restore preferences from backup."""
        with self._monitor.monitor_operation("PreferencesBackup", "restore"):
            try:
                # Get backup file to restore
                backup_file = self._get_backup_file(timestamp)
                if not backup_file:
                    return None
                
                # Load and verify backup
                backup_data = json.loads(backup_file.read_text())
                if not self._verify_backup(backup_data):
                    return None
                
                return backup_data["data"]
                
            except Exception as e:
                self._monitor.log_error("restore_error", str(e))
                return None
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List available backups with metadata."""
        with self._monitor.monitor_operation("PreferencesBackup", "list"):
            try:
                backups = []
                for file in sorted(self.backup_dir.glob("preferences_*.json")):
                    try:
                        data = json.loads(file.read_text())
                        backups.append({
                            "timestamp": data["timestamp"],
                            "version": data["version"],
                            "size": file.stat().st_size,
                            "path": str(file)
                        })
                    except Exception:
                        continue
                return backups
            except Exception as e:
                self._monitor.log_error("list_error", str(e))
                return []
    
    def verify_all_backups(self) -> List[Tuple[str, bool]]:
        """Verify integrity of all backups."""
        with self._monitor.monitor_operation("PreferencesBackup", "verify"):
            results = []
            for file in self.backup_dir.glob("preferences_*.json"):
                try:
                    data = json.loads(file.read_text())
                    is_valid = self._verify_backup(data)
                    results.append((data["timestamp"], is_valid))
                except Exception:
                    results.append((str(file), False))
            return results
    
    def _get_backup_file(self, timestamp: Optional[str] = None) -> Optional[Path]:
        """Get backup file by timestamp or latest."""
        try:
            if timestamp:
                backup_file = self.backup_dir / f"preferences_{timestamp}.json"
                return backup_file if backup_file.exists() else None
            
            # Get latest backup if no timestamp specified
            backups = sorted(self.backup_dir.glob("preferences_*.json"))
            return backups[-1] if backups else None
            
        except Exception as e:
            self._monitor.log_error("get_backup_error", str(e))
            return None
    
    def _cleanup_old_backups(self):
        """Remove old backups keeping only max_backups."""
        try:
            backups = sorted(self.backup_dir.glob("preferences_*.json"))
            if len(backups) > self.max_backups:
                for old_backup in backups[:-self.max_backups]:
                    old_backup.unlink()
        except Exception as e:
            self._monitor.log_error("cleanup_error", str(e))
    
    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate checksum of preferences data."""
        try:
            # Simple checksum for now, could be enhanced with better algorithm
            return str(hash(json.dumps(data, sort_keys=True)))
        except Exception as e:
            self._monitor.log_error("checksum_error", str(e))
            return ""
    
    def _verify_backup(self, backup_data: Dict[str, Any]) -> bool:
        """Verify backup data integrity."""
        try:
            # Verify required fields
            required_fields = ["timestamp", "version", "data", "checksum"]
            if not all(field in backup_data for field in required_fields):
                return False
            
            # Verify checksum
            current_checksum = self._calculate_checksum(backup_data["data"])
            return current_checksum == backup_data["checksum"]
            
        except Exception as e:
            self._monitor.log_error("verify_error", str(e))
            return False 