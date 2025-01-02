import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.splitter_processor import SplitterProcessor
from ..widgets.config_panel import ConfigPanel

class SplitterFrame(BaseToolFrame):
    """Tool for splitting CSV files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Splitter"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Split Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add split type selection
        self.config_panel.add_choice_option(
            'split_type',
            'Split Method',
            choices=['Row Count', 'Percentage', 'Column Value'],
            callback=self._on_split_type_changed
        )
        
        # Row count options
        self.config_panel.add_numeric_option(
            'row_count',
            'Rows per File',
            default=1000,
            min_val=1
        )
        
        # Percentage options
        self.config_panel.add_numeric_option(
            'percentage',
            'Split Percentage',
            default=50,
            min_val=1,
            max_val=99
        )
        
        # Column value options
        self.config_panel.add_choice_option(
            'split_column',
            'Split Column',
            choices=[],  # Will be populated when file is loaded
            callback=self._on_column_changed
        )
        
        # Common options
        self.config_panel.add_boolean_option(
            'keep_headers',
            'Include Headers in Each File',
            default=True
        )
        
        self.config_panel.add_text_option(
            'output_pattern',
            'Output Filename Pattern',
            default='split_{n}'
        ) 