import tkinter as tk
from tkinter import ttk
import pandas as pd
from ..widgets.file_selector import FileSelector

class BaseToolFrame(ttk.Frame):
    """Base class for tool frames"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.input_file = None
        # Get tool_manager from the main application window
        self.tool_manager = self.get_tool_manager()
        self.create_widgets()
    
    @classmethod
    def get_dependencies(cls) -> list:
        """Gets tool dependencies - override if needed"""
        return []
    
    def get_tool_manager(self):
        """Traverses widget hierarchy to find tool_manager"""
        widget = self
        while widget:
            if hasattr(widget, 'tool_manager'):
                return widget.tool_manager
            widget = widget.master
        return None
    
    @classmethod
    def get_tool_name(cls) -> str:
        """Gets the display name of the tool"""
        raise NotImplementedError
    
    def create_widgets(self):
        """Creates the tool's widgets"""
        # Add file selector
        self.file_selector = FileSelector(
            self,
            label_text="Input File",
            multiple=False
        )
        self.file_selector.pack(fill=tk.X, padx=5, pady=5)
        
        # Add file change callback
        self.file_selector.on_file_selected = self._on_file_selected
        
        # Create tool-specific widgets
        self.create_tool_widgets()

    def _on_file_selected(self, file_path: str):
        """Handles file selection"""
        self.input_file = file_path
        if hasattr(self, 'update_preview'):
            self.update_preview()

    def create_tool_widgets(self):
        """Creates tool-specific widgets - to be overridden by subclasses"""
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
            if self.tool_manager:
                self.tool_manager.save_tool_config(
                    self.get_tool_name(),
                    config
                )
            else:
                print("Warning: No tool_manager found, configuration not saved") 