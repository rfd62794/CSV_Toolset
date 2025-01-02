import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.validator_processor import ValidatorProcessor
from ..widgets.config_panel import ConfigPanel

class ValidatorFrame(BaseToolFrame):
    """Tool for validating CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Validator"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Validation Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add validation rules
        self.config_panel.add_boolean_option(
            'check_datatypes',
            'Check Data Types',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'check_nulls',
            'Check for Null Values',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'check_duplicates',
            'Check for Duplicates',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'check_ranges',
            'Check Value Ranges',
            default=False,
            callback=self._on_range_check_changed
        )
        
        # Range settings
        self.range_frame = ttk.LabelFrame(self, text="Range Settings")
        
        # Results display
        self.results_frame = ttk.LabelFrame(self, text="Validation Results")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_tree = ttk.Treeview(
            self.results_frame,
            columns=('Rule', 'Status', 'Details'),
            show='headings'
        )
        for col in ('Rule', 'Status', 'Details'):
            self.results_tree.heading(col, text=col)
        
        self.results_tree.pack(fill=tk.BOTH, expand=True) 