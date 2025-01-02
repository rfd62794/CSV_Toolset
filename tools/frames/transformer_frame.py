import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.transformer_processor import TransformerProcessor
from ..widgets.config_panel import ConfigPanel

class TransformerFrame(BaseToolFrame):
    """Tool for transforming CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Transformer"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Transform Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Column selection
        self.config_panel.add_choice_option(
            'column',
            'Transform Column',
            choices=[],  # Will be populated when file is loaded
            callback=self._on_column_changed
        )
        
        # Transformation options
        transforms = [
            'Uppercase',
            'Lowercase',
            'Title Case',
            'Strip Whitespace',
            'Remove Special Characters',
            'Format Numbers',
            'Format Dates',
            'Custom Regex'
        ]
        
        for transform in transforms:
            self.config_panel.add_boolean_option(
                f'transform_{transform.lower().replace(" ", "_")}',
                transform,
                callback=self._on_transform_changed
            )
        
        # Custom regex option
        self.config_panel.add_text_option(
            'custom_regex',
            'Custom Regex Pattern',
            callback=self._on_regex_changed
        )
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Transform Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_tree = ttk.Treeview(
            self.preview_frame,
            columns=('Original', 'Transformed'),
            show='headings'
        )
        self.preview_tree.heading('Original', text='Original Value')
        self.preview_tree.heading('Transformed', text='Transformed Value')
        self.preview_tree.pack(fill=tk.BOTH, expand=True) 

    def _on_column_changed(self, value: str):
        """Handles column selection change"""
        self.update_preview()
        self.save_config()

    def _on_transform_changed(self, value: bool):
        """Handles transformation option change"""
        self.update_preview()
        self.save_config()

    def _on_regex_changed(self, value: str):
        """Handles custom regex pattern change"""
        self.update_preview()
        self.save_config()

    def update_preview(self):
        """Updates the transform preview"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = TransformerProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
            
            column = self.config_panel.get_config().get('column')
            if not column:
                return
            
            # Clear preview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
            
            # Get sample values
            sample = df[column].head(5)
            transformed = self.processor.transform_sample(
                sample,
                self.config_panel.get_config()
            )
            
            # Update preview
            for orig, trans in zip(sample, transformed):
                self.preview_tree.insert('', tk.END, values=(orig, trans))
            
        except Exception as e:
            self.show_error(f"Preview error: {str(e)}") 