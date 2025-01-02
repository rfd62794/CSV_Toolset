import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.sample_processor import SampleProcessor
from ..widgets.config_panel import ConfigPanel
from ..widgets.file_selector import FileSelector
import pandas as pd

class SampleFrame(BaseToolFrame):
    """Tool for sampling CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Sampler"
    
    def create_widgets(self):
        # Add file selector
        self.file_selector = FileSelector(
            self,
            "Input CSV File",
            multiple=False
        )
        self.file_selector.pack(fill=tk.X, padx=5, pady=5)
        self.file_selector.on_file_selected = self._on_file_selected
        
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
        
        self.config_panel.add_number_option(
            'sample_size',
            'Sample Size',
            min_val=1,
            default=100,
            callback=self._on_sample_size_changed
        )
        
        # Add stratification options (initially hidden)
        self.config_panel.add_choice_option(
            'strat_column',
            'Stratification Column',
            choices=[],
            visible=False,
            callback=self._on_strat_column_changed
        )
        
        # Create preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create preview tree
        self.preview_tree = ttk.Treeview(self.preview_frame, show='headings')
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.preview_frame,
            orient="vertical",
            command=self.preview_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Create Sample",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
    
    def _on_file_selected(self, file_path: str):
        """Handles file selection"""
        try:
            # Set input file
            self.input_file = file_path
            
            # Read column names for stratification
            df = pd.read_csv(file_path)
            columns = df.columns.tolist()
            
            # Update stratification column choices
            self.config_panel.update_choices('strat_column', columns)
            
            # Update preview
            self.update_preview()
            
        except Exception as e:
            self.show_error(f"Error reading file: {str(e)}")
    
    def _on_sample_type_changed(self, value: str):
        """Handles sampling method change"""
        # Show/hide stratification options
        if value == 'Stratified':
            self.config_panel.show_option('strat_column')
        else:
            self.config_panel.hide_option('strat_column')
        
        self.update_preview()
        self.save_config()
    
    def _on_sample_size_changed(self, value: str):
        """Handles sample size change"""
        self.update_preview()
        self.save_config()
    
    def _on_strat_column_changed(self, value: str):
        """Handles stratification column change"""
        self.update_preview()
        self.save_config()
    
    def update_preview(self):
        """Updates the sample preview"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = SampleProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            preview_data = self.processor.preview_sample(df, config)
            
            # Clear current preview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
            
            # Update columns
            self.preview_tree['columns'] = preview_data.columns.tolist()
            for col in preview_data.columns:
                self.preview_tree.heading(col, text=col)
            
            # Add sample rows
            for idx, row in preview_data.iterrows():
                self.preview_tree.insert('', tk.END, values=row.tolist())
                
        except Exception as e:
            self.show_error(f"Preview error: {str(e)}")
    
    def process_file(self):
        """Processes the input file"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = SampleProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            result = self.processor.process_file(df, config)
            
            if result['success']:
                self.show_success(
                    f"Created sample with {result['rows']} rows. "
                    f"Saved to: {result['output_file']}"
                )
            else:
                self.show_error(result['error'])
                
        except Exception as e:
            self.show_error(f"Error processing file: {str(e)}") 