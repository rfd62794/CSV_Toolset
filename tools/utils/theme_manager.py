import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
from .settings_manager import SettingsManager

class ThemeManager:
    """Manages application theming and styles"""
    
    THEMES = {
        'light': {
            'bg': '#ffffff',
            'fg': '#000000',
            'select_bg': '#0078d7',
            'select_fg': '#ffffff',
            'button_bg': '#f0f0f0',
            'error': '#ff0000',
            'success': '#008000',
            'warning': '#ffa500'
        },
        'dark': {
            'bg': '#2d2d2d',
            'fg': '#ffffff',
            'select_bg': '#0078d7',
            'select_fg': '#ffffff',
            'button_bg': '#3d3d3d',
            'error': '#ff6b6b',
            'success': '#4caf50',
            'warning': '#ffd700'
        }
    }
    
    def __init__(self):
        self.settings = SettingsManager()
        self.current_theme = self.settings.get_setting('theme', 'light')
        self._setup_styles()
    
    def _setup_styles(self):
        """Sets up ttk styles"""
        style = ttk.Style()
        theme = self.THEMES[self.current_theme]
        
        # Configure common styles
        style.configure('TFrame', background=theme['bg'])
        style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        style.configure('TButton', background=theme['button_bg'])
        
        # Tool-specific styles
        style.configure('Tool.TFrame', padding=5)
        style.configure('Tool.TLabelframe', padding=5)
        style.configure('Header.TLabel', font=('TkDefaultFont', 12, 'bold'))
        
        # Status styles
        style.configure('Success.TLabel', foreground=theme['success'])
        style.configure('Error.TLabel', foreground=theme['error'])
        style.configure('Warning.TLabel', foreground=theme['warning'])
    
    def set_theme(self, theme_name: str):
        """Changes current theme"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            self.settings.set_setting('theme', theme_name)
            self._setup_styles()
    
    def get_color(self, color_name: str) -> str:
        """Gets color from current theme"""
        return self.THEMES[self.current_theme].get(color_name, '') 