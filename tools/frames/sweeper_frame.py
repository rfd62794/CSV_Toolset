import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.sweeper_processor import SweeperProcessor
from ..widgets.config_panel import ConfigPanel

class SweeperFrame(BaseToolFrame):
    """Tool for cleaning CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Sweeper"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Cleaning Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add cleaning options
        self.config_panel.add_boolean_option(
            'trim_whitespace',
            'Trim Whitespace',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'remove_duplicates',
            'Remove Duplicate Rows',
            default=False
        )
        
        self.config_panel.add_boolean_option(
            'drop_empty',
            'Drop Empty Columns',
            default=False
        )
        
        self.config_panel.add_choice_option(
            'null_handling',
            'Null Value Handling',
            choices=['Keep', 'Drop', 'Fill'],
            callback=self._on_null_handling_changed
        )
        
        # Add fill value option (initially hidden)
        self.fill_frame = ttk.Frame(self)
        self.config_panel.add_text_option(
            'fill_value',
            'Fill Value',
            default=''
        ) 
    
    def _on_null_handling_changed(self, value: str):
        """Handles null handling option change"""
        self.save_config() 