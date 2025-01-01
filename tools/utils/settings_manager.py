import json
from pathlib import Path
from typing import Any, Dict
from .config import ToolConfig

class SettingsManager:
    """Manages user settings and preferences"""
    
    def __init__(self):
        self.config = ToolConfig()
        self.settings_file = Path.home() / 'CSVToolkit' / 'settings.json'
        self.settings: Dict[str, Any] = {}
        self.load_settings()
    
    def load_settings(self):
        """Loads settings from file"""
        if self.settings_file.exists():
            try:
                self.settings = json.loads(self.settings_file.read_text())
            except Exception:
                self.settings = {}
        self._set_defaults()
    
    def _set_defaults(self):
        """Sets default settings if not present"""
        defaults = {
            'default_encoding': 'utf-8',
            'preview_rows': 5,
            'recent_files': [],
            'output_directory': str(self.config.get_output_dir()),
            'dark_mode': False
        }
        
        for key, value in defaults.items():
            if key not in self.settings:
                self.settings[key] = value
    
    def save_settings(self):
        """Saves settings to file"""
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        self.settings_file.write_text(json.dumps(self.settings, indent=2))
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Gets setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Sets setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def add_recent_file(self, file_path: str):
        """Adds file to recent files list"""
        recent = self.settings.get('recent_files', [])
        if file_path in recent:
            recent.remove(file_path)
        recent.insert(0, file_path)
        self.settings['recent_files'] = recent[:10]  # Keep last 10
        self.save_settings() 