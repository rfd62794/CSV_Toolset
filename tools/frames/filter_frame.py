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
            'Filter Operator',
            choices=[
                'Equals',
                'Not Equals',
                'Contains',
                'Starts With',
                'Ends With',
                'Greater Than',
                'Less Than',
                'Is Null',
                'Is Not Null'
            ],
            callback=self._on_operator_changed
        )
        
        self.config_panel.add_text_option(
            'filter_value',
            'Filter Value',
            callback=self._on_value_changed
        )
        
        self.config_panel.add_boolean_option(
            'case_sensitive',
            'Case Sensitive',
            default=False
        )
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Filter Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_tree = ttk.Treeview(self.preview_frame)
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
    
    def _on_column_changed(self, value: str):
        self.update_preview()
        self.save_config()
    
    def _on_operator_changed(self, value: str):
        self.update_preview()
        self.save_config()
    
    def _on_value_changed(self, value: str):
        self.update_preview()
        self.save_config() 