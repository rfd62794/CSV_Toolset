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
        
        # Operation-specific frames
        self.operation_frames = {}
        
        # Rename columns frame
        rename_frame = ttk.Frame(self)
        self.rename_list = ttk.Treeview(
            rename_frame,
            columns=('Original', 'New'),
            show='headings',
            height=5
        )
        self.rename_list.heading('Original', text='Original Name')
        self.rename_list.heading('New', text='New Name')
        self.rename_list.pack(fill=tk.BOTH, expand=True)
        self.operation_frames['Rename Columns'] = rename_frame
        
        # Reorder columns frame
        reorder_frame = ttk.Frame(self)
        self.reorder_list = ttk.Treeview(
            reorder_frame,
            columns=('Column', 'Order'),
            show='headings',
            height=5
        )
        self.reorder_list.heading('Column', text='Column')
        self.reorder_list.heading('Order', text='Order')
        self.reorder_list.pack(fill=tk.BOTH, expand=True)
        self.operation_frames['Reorder Columns'] = reorder_frame
        
        # Add column frame
        add_frame = ttk.Frame(self)
        ttk.Label(add_frame, text="Column Name:").pack(side=tk.LEFT)
        self.new_column_name = ttk.Entry(add_frame)
        self.new_column_name.pack(side=tk.LEFT, padx=5)
        ttk.Label(add_frame, text="Value:").pack(side=tk.LEFT)
        self.column_value = ttk.Entry(add_frame)
        self.column_value.pack(side=tk.LEFT, padx=5)
        self.operation_frames['Add Column'] = add_frame
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Apply Changes",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
    
    def _on_operation_changed(self, operation: str):
        """Handles operation selection change"""
        # Hide all operation frames
        for frame in self.operation_frames.values():
            frame.pack_forget()
            
        # Show selected operation frame
        if operation in self.operation_frames:
            self.operation_frames[operation].pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.save_config() 