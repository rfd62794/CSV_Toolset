"""Preferences validation and sanitization utilities."""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import jsonschema
from .schemas.preferences_schema import PREFERENCES_SCHEMA

logger = logging.getLogger(__name__)

class PreferencesValidator:
    """Validates and sanitizes preferences data."""
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        """
        Validate preferences data against schema.
        Returns True if valid, False otherwise.
        """
        try:
            jsonschema.validate(instance=data, schema=PREFERENCES_SCHEMA)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during validation: {str(e)}")
            return False
    
    @classmethod
    def sanitize(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize preferences data to ensure it meets schema requirements.
        Returns sanitized data.
        """
        sanitized = data.copy()
        
        # Ensure required fields exist
        if "version" not in sanitized:
            sanitized["version"] = "1.0"
        if "preferences" not in sanitized:
            sanitized["preferences"] = {}
        if "categories" not in sanitized:
            sanitized["categories"] = {}
        if "timestamp" not in sanitized:
            sanitized["timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")
            
        # Sanitize preferences
        prefs = sanitized["preferences"]
        sanitized["preferences"] = {
            name: bool(state)
            for name, state in prefs.items()
            if isinstance(name, str) and name.strip()
        }
        
        # Sanitize categories
        cats = sanitized["categories"]
        sanitized_cats = {}
        for name, cat in cats.items():
            if not isinstance(name, str) or not name.strip():
                continue
                
            if not isinstance(cat, dict):
                cat = {}
                
            sanitized_cat = {
                "desc": str(cat.get("desc", "Category description")),
                "icon": str(cat.get("icon", "📁")),
                "tools": {}
            }
            
            tools = cat.get("tools", {})
            if isinstance(tools, dict):
                sanitized_cat["tools"] = {
                    tool: str(desc)
                    for tool, desc in tools.items()
                    if isinstance(tool, str) and tool.strip()
                }
                
            sanitized_cats[name] = sanitized_cat
            
        sanitized["categories"] = sanitized_cats
        
        return sanitized
    
    @classmethod
    def load_and_validate(cls, path: Path) -> Optional[Dict[str, Any]]:
        """
        Load preferences from file, validate, and sanitize if needed.
        Returns None if file cannot be loaded or data is invalid.
        """
        try:
            if not path.exists():
                logger.warning(f"Preferences file not found: {path}")
                return None
                
            with open(path) as f:
                data = json.load(f)
                
            # Try validation first
            if cls.validate(data):
                return data
                
            # If validation fails, try sanitizing
            sanitized = cls.sanitize(data)
            if cls.validate(sanitized):
                logger.info("Preferences data sanitized successfully")
                return sanitized
                
            logger.error("Failed to validate preferences even after sanitization")
            return None
            
        except Exception as e:
            logger.error(f"Error loading preferences: {str(e)}")
            return None
    
    @classmethod
    def save_validated(cls, path: Path, data: Dict[str, Any]) -> bool:
        """
        Save preferences after validation.
        Returns True if successful, False otherwise.
        """
        try:
            # Sanitize and validate
            sanitized = cls.sanitize(data)
            if not cls.validate(sanitized):
                return False
                
            # Save to file
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(sanitized, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Error saving preferences: {str(e)}")
            return False 