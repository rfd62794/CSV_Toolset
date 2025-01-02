import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..widgets.config_panel import ConfigPanel

class ToolFrameTemplate(BaseToolFrame):
    """Template for tool frames"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Tool Name"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Tool Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add configuration options
        self.config_panel.add_text_option(
            'option1',
            'Option 1',
            callback=self._on_option1_changed
        )
        
        # Load saved configuration
        saved_config = self.parent.tool_manager.get_tool_config(self.get_tool_name())
        if saved_config:
            self.config_panel.set_config(saved_config)
    
    def _on_option1_changed(self, value: str):
        """Handles option change"""
        self.save_config()
    
    def get_config(self) -> dict:
        """Gets current tool configuration"""
        return self.config_panel.get_config() 