import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.profiler_processor import ProfilerProcessor
from ..widgets.config_panel import ConfigPanel

class ProfilerFrame(BaseToolFrame):
    """Tool for profiling CSV data statistics"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Profiler"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Profile Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add profiling options
        self.config_panel.add_boolean_option(
            'include_stats',
            'Include Statistics',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'include_types',
            'Include Data Types',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'include_nulls',
            'Include Null Analysis',
            default=True
        )
        
        self.config_panel.add_numeric_option(
            'sample_size',
            'Sample Size for Analysis',
            default=1000,
            min_val=100
        )
        
        # Results display
        self.results_frame = ttk.LabelFrame(self, text="Profile Results")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_tree = ttk.Treeview(
            self.results_frame,
            columns=('Column', 'Type', 'Stats', 'Nulls'),
            show='headings'
        )
        
        for col in ('Column', 'Type', 'Stats', 'Nulls'):
            self.results_tree.heading(col, text=col)
            
        self.results_tree.pack(fill=tk.BOTH, expand=True) 