import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.inspector_processor import InspectorProcessor
from ..widgets.config_panel import ConfigPanel

class InspectorFrame(BaseToolFrame):
    """Tool for inspecting CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Inspector"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Inspection Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add inspection options
        self.config_panel.add_boolean_option(
            'show_datatypes',
            'Show Data Types',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'show_nulls',
            'Show Null Values',
            default=True
        )
        
        self.config_panel.add_numeric_option(
            'sample_size',
            'Sample Size',
            default=100,
            min_val=1
        )
        
        # Results display
        self.results_tree = ttk.Treeview(
            self,
            columns=('Column', 'Type', 'Nulls', 'Sample'),
            show='headings'
        )
        
        for col in ('Column', 'Type', 'Nulls', 'Sample'):
            self.results_tree.heading(col, text=col)
        
        self.results_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) 