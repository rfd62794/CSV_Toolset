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
            min_val=1,
            callback=self._on_size_changed
        )
        
        self.config_panel.add_boolean_option(
            'keep_proportion',
            'Maintain Proportions',
            default=True,
            callback=self._on_proportion_changed
        )
        
        # Stratification options
        self.config_panel.add_choice_option(
            'strat_column',
            'Stratify By Column',
            choices=[],  # Will be populated when file is loaded
            callback=self._on_strat_column_changed
        )
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Sample Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_tree = ttk.Treeview(self.preview_frame)
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Create Sample",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
    
    def _on_sample_type_changed(self, value: str):
        """Handles sample type change"""
        # Show/hide stratification options
        if value == 'Stratified':
            self.config_panel.show_option('strat_column')
        else:
            self.config_panel.hide_option('strat_column')
        self.save_config()
        self.update_preview()
    
    def _on_size_changed(self, value: int):
        """Handles sample size change"""
        self.save_config()
        self.update_preview()
    
    def _on_proportion_changed(self, value: bool):
        """Handles proportion option change"""
        self.save_config()
        self.update_preview()
    
    def _on_strat_column_changed(self, value: str):
        """Handles stratification column change"""
        self.save_config()
        self.update_preview()
    
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