"""JSON schema for preferences validation."""
from typing import Dict, Any

PREFERENCES_SCHEMA = {
    "type": "object",
    "required": ["version", "preferences", "categories", "timestamp"],
    "properties": {
        "version": {
            "type": "string",
            "pattern": r"^\d+\.\d+$",
            "description": "Preferences format version"
        },
        "preferences": {
            "type": "object",
            "patternProperties": {
                "^[A-Za-z ]+$": {
                    "type": "boolean",
                    "description": "Tool visibility state"
                }
            },
            "additionalProperties": False,
            "description": "Tool visibility preferences"
        },
        "categories": {
            "type": "object",
            "patternProperties": {
                "^[A-Za-z ]+$": {
                    "type": "object",
                    "required": ["desc", "icon", "tools"],
                    "properties": {
                        "desc": {
                            "type": "string",
                            "minLength": 1,
                            "description": "Category description"
                        },
                        "icon": {
                            "type": "string",
                            "pattern": r"^[\u2600-\u26FF\u2700-\u27BF\u1F300-\u1F9FF]$",
                            "description": "Category emoji icon"
                        },
                        "tools": {
                            "type": "object",
                            "patternProperties": {
                                "^[A-Za-z ]+$": {
                                    "type": "string",
                                    "minLength": 1,
                                    "description": "Tool description"
                                }
                            },
                            "additionalProperties": False,
                            "description": "Tools in this category"
                        }
                    },
                    "additionalProperties": False,
                    "description": "Category configuration"
                }
            },
            "additionalProperties": False,
            "description": "Tool categories"
        },
        "timestamp": {
            "type": "string",
            "pattern": r"^\d{8}_\d{6}$",
            "description": "Last modification timestamp (YYYYMMDD_HHMMSS)"
        }
    },
    "additionalProperties": False
} 