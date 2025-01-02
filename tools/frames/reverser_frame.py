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
            default=True,
            callback=self._on_header_changed
        )
        
        self.config_panel.add_boolean_option(
            'keep_index',
            'Keep Index Column',
            default=False,
            callback=self._on_index_changed
        )
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_tree = ttk.Treeview(self.preview_frame)
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Reverse Data",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
    
    def _on_reverse_type_changed(self, value: str):
        """Handles reverse type change"""
        self.save_config()
        self.update_preview()
    
    def _on_header_changed(self, value: bool):
        """Handles header option change"""
        self.save_config()
        self.update_preview()
    
    def _on_index_changed(self, value: bool):
        """Handles index option change"""
        self.save_config()
        self.update_preview()
    
    def update_preview(self):
        """Updates the preview display"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = ReverserProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            preview_data = self.processor.preview_reverse(df, config)
            
            # Clear current preview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
            
            # Update columns
            self.preview_tree['columns'] = preview_data.columns.tolist()
            for col in preview_data.columns:
                self.preview_tree.heading(col, text=col)
            
            # Add preview rows
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
                    f"Successfully reversed data. "
                    f"Output saved to: {result['output_file']}"
                )
            else:
                self.show_error(result['error'])
                
        except Exception as e:
            self.show_error(f"Error processing file: {str(e)}") 