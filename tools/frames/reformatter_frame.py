import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.reformatter_processor import ReformatterProcessor
from ..widgets.config_panel import ConfigPanel

class ReformatterFrame(BaseToolFrame):
    """Tool for reformatting CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Reformatter"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Format Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add format options
        self.config_panel.add_choice_option(
            'delimiter',
            'Delimiter',
            choices=[',', ';', '\t', '|', ' '],
            callback=self._on_delimiter_changed
        )
        
        self.config_panel.add_choice_option(
            'quoting',
            'Quoting Style',
            choices=['Minimal', 'All', 'Non-numeric', 'None'],
            callback=self._on_quoting_changed
        )
        
        self.config_panel.add_text_option(
            'quote_char',
            'Quote Character',
            default='"'
        )
        
        self.config_panel.add_text_option(
            'escape_char',
            'Escape Character',
            default='\\'
        )
        
        self.config_panel.add_boolean_option(
            'remove_spaces',
            'Remove Extra Spaces',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'standardize_headers',
            'Standardize Headers',
            default=True
        )
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Format Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_text = tk.Text(
            self.preview_frame,
            wrap=tk.NONE,
            height=10
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True) 

    def _on_delimiter_changed(self, value: str):
        """Handles delimiter change"""
        self.update_preview()
        self.save_config()

    def _on_quoting_changed(self, value: str):
        """Handles quoting style change"""
        self.update_preview()
        self.save_config()

    def update_preview(self):
        """Updates the format preview"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = ReformatterProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
            
            # Clear preview
            self.preview_text.delete('1.0', tk.END)
            
            # Get sample rows
            sample = df.head(5)
            
            # Apply formatting
            config = self.config_panel.get_config()
            formatted = self.processor.format_sample(sample, config)
            
            # Show preview
            self.preview_text.insert('1.0', formatted)
            
        except Exception as e:
            self.show_error(f"Preview error: {str(e)}") 