from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable, List
from ..utils.file_manager import FileManager
from ..utils.data_writer import DataWriter
from ..utils.config import ToolConfig

class BaseToolFrame(ttk.Frame, ABC):
    """Base class for tool frames"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.load_config()
        self.create_widgets()
    
    @classmethod
    def get_tool_name(cls) -> str:
        """Gets tool name"""
        raise NotImplementedError
    
    @classmethod
    def get_dependencies(cls) -> List[str]:
        """Gets tool dependencies"""
        return []
    
    def create_widgets(self):
        """Creates tool widgets"""
        raise NotImplementedError
    
    def load_config(self):
        """Loads tool configuration"""
        try:
            config = self.parent.tool_manager.get_tool_config(self.get_tool_name())
            self.apply_config(config)
        except Exception as e:
            print(f"Error loading configuration: {e}")
    
    def save_config(self):
        """Saves tool configuration"""
        try:
            config = self.get_config()
            self.parent.tool_manager.save_tool_config(self.get_tool_name(), config)
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def get_config(self) -> dict:
        """Gets current tool configuration"""
        return {}
    
    def apply_config(self, config: dict):
        """Applies loaded configuration"""
        pass 