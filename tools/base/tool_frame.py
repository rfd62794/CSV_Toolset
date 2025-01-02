import tkinter as tk
from tkinter import ttk
import pandas as pd

class BaseToolFrame(ttk.Frame):
    """Base class for tool frames"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.input_file = None
        self.create_widgets()
    
    @classmethod
    def get_tool_name(cls) -> str:
        """Gets the display name of the tool"""
        raise NotImplementedError
    
    def create_widgets(self):
        """Creates the tool's widgets"""
        raise NotImplementedError
    
    def read_input_file(self) -> pd.DataFrame:
        """Reads the input CSV file"""
        if not self.input_file:
            self.show_error("No input file selected")
            return None
        try:
            return pd.read_csv(self.input_file)
        except Exception as e:
            self.show_error(f"Error reading file: {str(e)}")
            return None
    
    def show_error(self, message: str):
        """Shows error message"""
        if hasattr(self, 'error_label'):
            self.error_label.destroy()
        self.error_label = ttk.Label(
            self,
            text=message,
            foreground='red'
        )
        self.error_label.pack(pady=5)
    
    def show_success(self, message: str):
        """Shows success message"""
        if hasattr(self, 'error_label'):
            self.error_label.destroy()
        self.error_label = ttk.Label(
            self,
            text=message,
            foreground='green'
        )
        self.error_label.pack(pady=5)
    
    def save_config(self):
        """Saves tool configuration"""
        if hasattr(self, 'config_panel'):
            config = self.config_panel.get_config()
            self.parent.tool_manager.save_tool_config(
                self.get_tool_name(),
                config
            ) 