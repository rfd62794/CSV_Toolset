import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.column_manager_processor import ColumnManagerProcessor
from ..widgets.config_panel import ConfigPanel

class ColumnManagerFrame(BaseToolFrame):
    """Tool for managing CSV columns"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Column Manager"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Column Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add column operations
        self.config_panel.add_choice_option(
            'operation',
            'Operation',
            choices=[
                'Rename Columns',
                'Reorder Columns',
                'Remove Columns',
                'Add Column',
                'Split Column',
                'Combine Columns'
            ],
            callback=self._on_operation_changed
        )
        
        # Column selection
        self.columns_frame = ttk.LabelFrame(self, text="Column Selection")
        self.columns_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Column list with checkboxes
        self.columns_tree = ttk.Treeview(
            self.columns_frame,
            columns=('Column', 'Action'),
            show='headings'
        )
        self.columns_tree.heading('Column', text='Column')
        self.columns_tree.heading('Action', text='Action')
        self.columns_tree.pack(fill=tk.BOTH, expand=True) 