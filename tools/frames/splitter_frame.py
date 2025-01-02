import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.splitter_processor import SplitterProcessor
from ..widgets.config_panel import ConfigPanel
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

class SplitterFrame(BaseToolFrame):
    """Tool for splitting CSV files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Splitter"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Split Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add split options
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

        # Add output preview
        self.preview_frame = ttk.LabelFrame(self, text="Output Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_tree = ttk.Treeview(
            self.preview_frame,
            columns=('File', 'Rows'),
            show='headings'
        )
        self.preview_tree.heading('File', text='Output File')
        self.preview_tree.heading('Rows', text='Row Count')
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Split File",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)

    def _on_split_type_changed(self, value: str):
        """Handles split type change"""
        # Show/hide relevant options based on split type
        if value == 'Row Count':
            self.config_panel.show_option('row_count')
            self.config_panel.hide_option('percentage')
            self.config_panel.hide_option('split_column')
        elif value == 'Percentage':
            self.config_panel.hide_option('row_count')
            self.config_panel.show_option('percentage')
            self.config_panel.hide_option('split_column')
        else:  # Column Value
            self.config_panel.hide_option('row_count')
            self.config_panel.hide_option('percentage')
            self.config_panel.show_option('split_column')
        self.save_config()

    def _on_column_changed(self, value: str):
        """Handles column selection change"""
        self.save_config() 

    def process_file(self):
        """Processes the input file"""
        if not hasattr(self, 'processor'):
            self.processor = SplitterProcessor()
            
        try:
            config = self.config_panel.get_config()
            result = self.processor.process_file(self.input_file, config)
            
            if result['success']:
                self.show_success(f"Split into {len(result['files_created'])} files")
                self.update_preview(result['files_created'])
            else:
                self.show_error(result['error'])
                
        except Exception as e:
            self.show_error(f"Error processing file: {str(e)}")
    
    def update_preview(self, files: List[str]):
        """Updates the preview with created files"""
        # Clear previous preview
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
            
        # Add new files
        for file_path in files:
            try:
                df = pd.read_csv(file_path)
                self.preview_tree.insert('', tk.END, values=(
                    Path(file_path).name,
                    len(df)
                ))
            except Exception as e:
                print(f"Error reading {file_path}: {e}") 