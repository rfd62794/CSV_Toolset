import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.merger_processor import MergerProcessor
from ..widgets.config_panel import ConfigPanel

class MergerFrame(BaseToolFrame):
    """Tool for merging CSV files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Merger"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Merge Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add merge type selection
        self.config_panel.add_choice_option(
            'merge_type',
            'Merge Type',
            choices=['append', 'join'],
            callback=self._on_merge_type_changed
        )
        
        # Add join settings (initially hidden)
        self.join_frame = ttk.LabelFrame(self, text="Join Settings")
        
        self.config_panel.add_text_option(
            'join_key',
            'Join Key Column',
            callback=self._on_join_key_changed
        )
        
        self.config_panel.add_choice_option(
            'join_type',
            'Join Type',
            choices=['inner', 'outer', 'left', 'right'],
            callback=self._on_join_type_changed
        )
        
        # Load saved configuration
        saved_config = self.parent.tool_manager.get_tool_config(self.get_tool_name())
        if saved_config:
            self.config_panel.set_config(saved_config)
    
    def _on_merge_type_changed(self, value: str):
        """Handles merge type change"""
        if value == 'join':
            self.join_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.join_frame.pack_forget()
        self.save_config()
    
    def _on_join_key_changed(self, value: str):
        """Handles join key change"""
        self.save_config()
    
    def _on_join_type_changed(self, value: str):
        """Handles join type change"""
        self.save_config()
    
    def get_config(self) -> dict:
        """Gets current tool configuration"""
        return self.config_panel.get_config() 