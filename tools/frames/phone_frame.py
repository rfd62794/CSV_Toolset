import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.phone_processor import PhoneProcessor
from ..widgets.config_panel import ConfigPanel

class PhoneFrame(BaseToolFrame):
    """Tool for formatting phone numbers"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Phone Formatter"
    
    def create_widgets(self):
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
            'Output Format',
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
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'validate_numbers',
            'Validate Numbers',
            default=True,
            callback=self._on_validate_changed
        )
        
        # Add validation options
        self.validation_frame = ttk.LabelFrame(self, text="Validation")
        self.validation_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.config_panel.add_choice_option(
            'invalid_handling',
            'Invalid Number Handling',
            choices=['Keep', 'Remove', 'Mark'],
            callback=self._on_invalid_handling_changed
        ) 
    
    def _on_column_changed(self, value: str):
        """Handles column selection change"""
        self.save_config() 