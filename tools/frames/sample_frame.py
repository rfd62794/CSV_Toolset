import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.sample_processor import SampleProcessor
from ..widgets.config_panel import ConfigPanel

class SampleFrame(BaseToolFrame):
    """Tool for sampling CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Sampler"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Sampling Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add sampling options
        self.config_panel.add_choice_option(
            'sample_type',
            'Sampling Method',
            choices=['Random', 'Systematic', 'Stratified'],
            callback=self._on_sample_type_changed
        )
        
        self.config_panel.add_numeric_option(
            'sample_size',
            'Sample Size',
            default=100,
            min_val=1
        )
        
        # Add stratification options (initially hidden)
        self.strat_frame = ttk.LabelFrame(self, text="Stratification")
        self.config_panel.add_text_option(
            'strat_column',
            'Stratify By Column'
        ) 