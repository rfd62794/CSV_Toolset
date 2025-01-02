import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.appender_processor import AppenderProcessor
from ..widgets.config_panel import ConfigPanel
from ..widgets.file_selector import FileSelector

class AppenderFrame(BaseToolFrame):
    """Tool for appending CSV files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Appender"
    
    def create_widgets(self):
        # File selection for additional files
        self.file_selector = FileSelector(
            self,
            "Additional Files",
            multiple=True
        )
        self.file_selector.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configuration panel
        self.config_panel = ConfigPanel(self, "Append Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add configuration options
        self.config_panel.add_boolean_option(
            'ignore_headers',
            'Ignore Headers in Additional Files',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'match_columns',
            'Match Column Order',
            default=True,
            callback=self._on_match_columns_changed
        )
        
        self.config_panel.add_choice_option(
            'missing_values',
            'Missing Column Handling',
            choices=['Fill NA', 'Skip File', 'Error'],
            callback=self._on_missing_handling_changed
        )
        
        # Load saved configuration
        saved_config = self.parent.tool_manager.get_tool_config(self.get_tool_name())
        if saved_config:
            self.config_panel.set_config(saved_config) 