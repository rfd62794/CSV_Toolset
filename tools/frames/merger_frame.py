import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.merger_processor import MergerProcessor
from ..widgets.config_panel import ConfigPanel
from ..widgets.file_selector import FileSelector

class MergerFrame(BaseToolFrame):
    """Tool for merging multiple CSV files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Merger"
    
    def create_widgets(self):
        # File selection for additional files
        self.file_selector = FileSelector(
            self,
            "Additional Files",
            multiple=True
        )
        self.file_selector.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configuration panel
        self.config_panel = ConfigPanel(self, "Merge Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add merge options
        self.config_panel.add_choice_option(
            'merge_type',
            'Merge Type',
            choices=['Append', 'Join'],
            callback=self._on_merge_type_changed
        )
        
        self.config_panel.add_choice_option(
            'join_type',
            'Join Type',
            choices=['Inner', 'Outer', 'Left', 'Right'],
            callback=self._on_join_type_changed
        )
        
        self.config_panel.add_text_option(
            'key_column',
            'Join Key Column'
        )
        
        self.config_panel.add_boolean_option(
            'match_columns',
            'Match Column Names',
            default=True
        )
    
    def _on_merge_type_changed(self, value: str):
        """Handles merge type change"""
        join_options_visible = (value == 'Join')
        if join_options_visible:
            self.config_panel.show_option('join_type')
            self.config_panel.show_option('key_column')
        else:
            self.config_panel.hide_option('join_type')
            self.config_panel.hide_option('key_column')
        self.save_config()
    
    def _on_join_type_changed(self, value: str):
        """Handles join type change"""
        self.save_config()
    
    def get_config(self) -> dict:
        """Gets current tool configuration"""
        return self.config_panel.get_config() 