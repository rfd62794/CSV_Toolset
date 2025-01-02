import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.filter_processor import FilterProcessor
from ..widgets.config_panel import ConfigPanel

class FilterFrame(BaseToolFrame):
    """Tool for filtering CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Filter"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Filter Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add filter options
        self.config_panel.add_choice_option(
            'column',
            'Filter Column',
            choices=[],  # Will be populated when file is loaded
            callback=self._on_column_changed
        )
        
        self.config_panel.add_choice_option(
            'operator',
            'Operator',
            choices=['equals', 'not_equals', 'greater_than', 'less_than', 
                    'contains', 'starts_with', 'ends_with'],
            callback=self._on_operator_changed
        )
        
        self.config_panel.add_text_option(
            'filter_value',
            'Filter Value',
            callback=self._on_value_changed
        ) 