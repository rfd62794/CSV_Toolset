from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable
from ..utils.file_manager import FileManager
from ..utils.data_writer import DataWriter
from ..utils.config import ToolConfig

class BaseToolFrame(ttk.Frame, ABC):
    """Base class for all tool frames"""
    
    def __init__(self, master):
        super().__init__(master)
        
        self.file_manager = FileManager()
        self.writer = DataWriter()
        self.config = ToolConfig()
        
        self.input_file: Optional[str] = None
        self.file_path_var = tk.StringVar()
        
        self.status_var = tk.StringVar(value="Select a file to begin")
        self.progress_var = tk.IntVar(value=0)
        
        self.create_common_widgets()
        
    @classmethod
    @abstractmethod
    def get_tool_name(cls) -> str:
        """Returns the display name of the tool"""
        pass
    
    def create_common_widgets(self):
        """Creates widgets common to all tools"""
        # File selection frame
        file_frame = ttk.LabelFrame(self, text="Input File")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Entry(
            file_frame,
            textvariable=self.file_path_var,
            state='readonly',
            width=50
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            file_frame,
            text="Browse",
            command=self.browse_file
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Status and progress frame
        status_frame = ttk.Frame(self)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        ttk.Label(
            status_frame,
            textvariable=self.status_var
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            mode='determinate',
            length=200
        ).pack(side=tk.RIGHT, padx=5)
    
    def browse_file(self):
        """Opens file dialog for CSV selection"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            valid, error = self.file_manager.validate_csv_file(file_path)
            if not valid:
                self.show_error(error)
                return
                
            self.input_file = file_path
            self.file_path_var.set(file_path)
    
    def update_progress(self, percent: int, message: Optional[str] = None):
        """Updates progress bar and status message"""
        self.progress_var.set(percent)
        if message:
            self.status_var.set(message)
        self.update()
    
    def show_error(self, message: str):
        """Shows error message"""
        messagebox.showerror("Error", message)
        self.status_var.set("Error: " + message)
    
    def show_warning(self, message: str):
        """Shows warning message"""
        messagebox.showwarning("Warning", message)
    
    def create_tool_specific_widgets(self):
        """Override this method to create tool-specific widgets"""
        raise NotImplementedError 