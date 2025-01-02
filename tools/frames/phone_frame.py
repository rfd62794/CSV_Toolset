import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.phone_processor import PhoneProcessor
from ..widgets.config_panel import ConfigPanel
import pandas as pd

class PhoneFrame(BaseToolFrame):
    """Tool for formatting phone numbers"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Phone Formatter"
    
    def create_tool_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Phone Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add configuration options
        self.config_panel.add_choice_option(
            'column',
            'Phone Column',
            choices=[],  # Will be populated when file is loaded
            callback=self._on_column_changed
        )
        
        self.config_panel.add_choice_option(
            'format',
            'Phone Format',
            choices=[
                '(XXX) XXX-XXXX',
                'XXX-XXX-XXXX',
                'XXX.XXX.XXXX',
                'XXXXXXXXXX'
            ],
            callback=self._on_format_changed
        )
        
        self.config_panel.add_boolean_option(
            'keep_original',
            'Keep Original Column',
            default=True,
            callback=self._on_keep_changed
        )
        
        self.config_panel.add_boolean_option(
            'validate_numbers',
            'Validate Numbers',
            default=True,
            callback=self._on_validate_changed
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
            text="Format Numbers",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
    
    def _on_column_changed(self, value: str):
        """Handles column selection change"""
        self.update_preview()
        self.save_config()
    
    def _on_format_changed(self, value: str):
        """Handles format selection change"""
        self.update_preview()
        self.save_config()
    
    def _on_keep_changed(self, value: bool):
        """Handles keep original option change"""
        self.save_config()
        self.update_preview()
    
    def _on_validate_changed(self, value: bool):
        """Handles validation option change"""
        self.save_config()
        self.update_preview()
    
    def _on_file_selected(self, file_path: str):
        """Handles file selection"""
        try:
            # Read column names
            df = pd.read_csv(file_path)
            columns = df.columns.tolist()
            
            # Update column choices
            self.config_panel.update_choices('column', columns)
            
            # Update preview if column is selected
            if self.config_panel.get_config().get('column'):
                self.update_preview()
                
        except Exception as e:
            self.show_error(f"Error reading file: {str(e)}")
    
    def update_preview(self):
        """Updates the preview display"""
        try:
            if not self.input_file:
                return
                
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            column = config.get('column')
            
            if not column:
                return
                
            if column not in df.columns:
                self.show_error(f"Column '{column}' not found in file")
                return
                
            # Get sample data
            preview_data = df.head(5)[[column]].copy()
            
            # Format phone numbers
            if not hasattr(self, 'processor'):
                self.processor = PhoneProcessor()
                
            format_pattern = config.get('format', '(XXX) XXX-XXXX')
            preview_data['Formatted'] = preview_data[column].apply(
                lambda x: self.processor.format_number(x, format_pattern)
            )
            
            # Clear current preview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
                
            # Update columns
            self.preview_tree['columns'] = ['Original', 'Formatted']
            self.preview_tree.heading('Original', text='Original')
            self.preview_tree.heading('Formatted', text='Formatted')
            
            # Add preview rows
            for _, row in preview_data.iterrows():
                self.preview_tree.insert('', tk.END, values=(
                    row[column],
                    row['Formatted']
                ))
                
        except Exception as e:
            self.show_error(f"Preview error: {str(e)}")
    
    def process_file(self):
        """Processes the input file"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = PhoneProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            result = self.processor.process_file(df, config)
            
            if result['success']:
                self.show_success(
                    f"Successfully formatted phone numbers. "
                    f"Output saved to: {result['output_file']}"
                )
            else:
                self.show_error(result['error'])
                
        except Exception as e:
            self.show_error(f"Error processing file: {str(e)}") 