import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.reverser_processor import ReverserProcessor
from ..widgets.config_panel import ConfigPanel

class ReverserFrame(BaseToolFrame):
    """Tool for reversing CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Reverser"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Reverse Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add configuration options
        self.config_panel.add_choice_option(
            'reverse_type',
            'Reverse Type',
            choices=['Rows', 'Columns', 'Both'],
            callback=self._on_reverse_type_changed
        )
        
        self.config_panel.add_boolean_option(
            'keep_header',
            'Keep Header Row',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'keep_index',
            'Keep Index Column',
            default=False
        )
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_tree = ttk.Treeview(self.preview_frame)
        self.preview_tree.pack(fill=tk.BOTH, expand=True) 
    
    def _on_reverse_type_changed(self, value: str):
        """Handles reverse type change"""
        self.save_config() 