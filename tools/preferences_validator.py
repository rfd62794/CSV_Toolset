"""Preferences validation system with performance monitoring."""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from .utils.performance_monitor import PerformanceMonitor

class PreferencesValidator:
    """Validates and sanitizes preferences data."""
    
    _monitor = PerformanceMonitor()
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        """Validates preferences data structure."""
        with cls._monitor.monitor_operation("PreferencesValidator", "validate"):
            try:
                # Version validation
                if not cls._validate_version(data):
                    return False
                
                # Preferences validation
                if not cls._validate_preferences(data):
                    return False
                
                # Categories validation
                if not cls._validate_categories(data):
                    return False
                
                # Timestamp validation
                if not cls._validate_timestamp(data):
                    return False
                
                return True
            except Exception as e:
                cls._monitor.log_error("validation_error", str(e))
                return False
    
    @classmethod
    def sanitize(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitizes preferences data."""
        with cls._monitor.monitor_operation("PreferencesValidator", "sanitize"):
            try:
                sanitized = data.copy()
                
                # Sanitize version
                if "version" not in sanitized or not cls._validate_version(sanitized):
                    sanitized["version"] = "2.0"
                
                # Sanitize preferences
                if "preferences" not in sanitized:
                    sanitized["preferences"] = {}
                sanitized["preferences"] = {
                    str(k): bool(v)
                    for k, v in sanitized["preferences"].items()
                    if k and str(k).strip()
                }
                
                # Sanitize categories
                if "categories" not in sanitized:
                    sanitized["categories"] = {}
                sanitized["categories"] = cls._sanitize_categories(sanitized["categories"])
                
                # Sanitize timestamp
                if "timestamp" not in sanitized or not cls._validate_timestamp(sanitized):
                    sanitized["timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                return sanitized
            except Exception as e:
                cls._monitor.log_error("sanitization_error", str(e))
                return cls._get_default_preferences()
    
    @classmethod
    def load_and_validate(cls, path: Path) -> Optional[Dict[str, Any]]:
        """Loads and validates preferences from file."""
        with cls._monitor.monitor_operation("PreferencesValidator", "load_and_validate"):
            try:
                if not path.exists():
                    return None
                
                data = json.loads(path.read_text())
                if not cls.validate(data):
                    data = cls.sanitize(data)
                return data
            except Exception as e:
                cls._monitor.log_error("load_error", str(e))
                return None
    
    @classmethod
    def save_validated(cls, path: Path, data: Dict[str, Any]) -> bool:
        """Saves validated preferences to file."""
        with cls._monitor.monitor_operation("PreferencesValidator", "save_validated"):
            try:
                if not cls.validate(data):
                    data = cls.sanitize(data)
                
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(data, indent=2))
                return True
            except Exception as e:
                cls._monitor.log_error("save_error", str(e))
                return False
    
    @staticmethod
    def _validate_version(data: Dict[str, Any]) -> bool:
        """Validates version field."""
        return (
            "version" in data and
            isinstance(data["version"], str) and
            data["version"] in ["1.0", "1.1", "1.2", "2.0"]
        )
    
    @staticmethod
    def _validate_preferences(data: Dict[str, Any]) -> bool:
        """Validates preferences structure."""
        return (
            "preferences" in data and
            isinstance(data["preferences"], dict) and
            all(
                isinstance(k, str) and isinstance(v, bool)
                for k, v in data["preferences"].items()
            )
        )
    
    @staticmethod
    def _validate_categories(data: Dict[str, Any]) -> bool:
        """Validates categories structure."""
        if "categories" not in data or not isinstance(data["categories"], dict):
            return False
            
        for cat_info in data["categories"].values():
            if not isinstance(cat_info, dict):
                return False
            if not all(k in cat_info for k in ["desc", "icon", "tools"]):
                return False
            if not isinstance(cat_info["tools"], dict):
                return False
        return True
    
    @staticmethod
    def _validate_timestamp(data: Dict[str, Any]) -> bool:
        """Validates timestamp format."""
        return (
            "timestamp" in data and
            isinstance(data["timestamp"], str) and
            len(data["timestamp"]) == 15 and
            data["timestamp"][8] == "_"
        )
    
    @staticmethod
    def _sanitize_categories(categories: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitizes categories structure."""
        sanitized = {}
        for cat, info in categories.items():
            if not cat or not str(cat).strip():
                continue
                
            if not isinstance(info, dict):
                info = {}
                
            sanitized[str(cat)] = {
                "desc": str(info.get("desc", "Category description")),
                "icon": str(info.get("icon", "📁")),
                "tools": {
                    str(k): str(v)
                    for k, v in info.get("tools", {}).items()
                    if k and str(k).strip()
                }
            }
        return sanitized
    
    @staticmethod
    def _get_default_preferences() -> Dict[str, Any]:
        """Returns default preferences structure."""
        return {
            "version": "2.0",
            "preferences": {},
            "categories": {},
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
        } 