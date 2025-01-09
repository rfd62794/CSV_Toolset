"""Preferences validation and error handling utilities."""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

class PreferencesValidator:
    """Validates and sanitizes preferences data."""
    
    REQUIRED_FIELDS = ["preferences", "timestamp", "categories"]
    TOOL_STATES = [True, False]
    
    @classmethod
    def validate_preferences(cls, data: Dict[str, Any]) -> List[str]:
        """
        Validate preferences data structure and content.
        Returns a list of validation errors, empty if valid.
        """
        errors = []
        
        # Check basic structure
        if not isinstance(data, dict):
            errors.append("Preferences must be a dictionary")
            return errors
            
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"Missing required field: {field}")
                
        # Validate preferences
        if "preferences" in data:
            prefs = data["preferences"]
            if not isinstance(prefs, dict):
                errors.append("Preferences must be a dictionary")
            else:
                for tool, state in prefs.items():
                    if not isinstance(tool, str):
                        errors.append(f"Invalid tool name: {tool}")
                    if state not in cls.TOOL_STATES:
                        errors.append(f"Invalid state for {tool}: {state}")
                        
        # Validate categories
        if "categories" in data:
            cats = data["categories"]
            if not isinstance(cats, dict):
                errors.append("Categories must be a dictionary")
            else:
                for cat, info in cats.items():
                    if not isinstance(info, dict):
                        errors.append(f"Invalid category info for {cat}")
                    else:
                        required = ["desc", "icon", "tools"]
                        for field in required:
                            if field not in info:
                                errors.append(f"Missing {field} in category {cat}")
                                
        return errors
        
    @classmethod
    def sanitize_preferences(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and normalize preferences data.
        Returns sanitized data or raises ValueError if invalid.
        """
        errors = cls.validate_preferences(data)
        if errors:
            raise ValueError("\n".join(errors))
            
        sanitized = {
            "preferences": {},
            "categories": data.get("categories", {}),
            "timestamp": data.get("timestamp", "")
        }
        
        # Sanitize preferences
        prefs = data.get("preferences", {})
        for tool, state in prefs.items():
            sanitized["preferences"][str(tool)] = bool(state)
            
        return sanitized
        
    @classmethod
    def load_and_validate(cls, path: Path) -> Optional[Dict[str, Any]]:
        """
        Load preferences from file and validate.
        Returns validated preferences or None if invalid/not found.
        """
        try:
            if not path.exists():
                logger.warning(f"Preferences file not found: {path}")
                return None
                
            with open(path) as f:
                data = json.load(f)
                
            errors = cls.validate_preferences(data)
            if errors:
                logger.error("Preferences validation failed:\n" + "\n".join(errors))
                return None
                
            return cls.sanitize_preferences(data)
            
        except Exception as e:
            logger.error(f"Failed to load preferences: {str(e)}")
            return None
            
    @classmethod
    def save_validated(cls, path: Path, data: Dict[str, Any]) -> bool:
        """
        Validate and save preferences to file.
        Returns True if successful, False otherwise.
        """
        try:
            sanitized = cls.sanitize_preferences(data)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(sanitized, f, indent=2)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save preferences: {str(e)}")
            return False 