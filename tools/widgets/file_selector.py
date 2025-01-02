import tkinter as tk
from tkinter import ttk, filedialog
from typing import Optional, Callable
from ..utils.file_manager import FileManager

class FileSelector(ttk.Frame):
    """Reusable file selection widget"""
    
    def __init__(self, parent, label_text="Select File", multiple=False):
        super().__init__(parent)
        self.multiple = multiple
        
        ttk.Label(self, text=label_text).pack(side=tk.LEFT, padx=5)
        
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(
            self,
            textvariable=self.file_var,
            state='readonly'
        )
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Button(
            self,
            text="Browse",
            command=self._browse_file
        ).pack(side=tk.LEFT)
        
        self.selected_files = []
    
    def _browse_file(self):
        """Opens file browser"""
        if self.multiple:
            files = tk.filedialog.askopenfilenames(
                filetypes=[("CSV files", "*.csv")]
            )
            if files:
                self.selected_files = list(files)
                self.file_var.set(f"{len(files)} files selected")
        else:
            filename = tk.filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv")]
            )
            if filename:
                self.selected_files = [filename]
                self.file_var.set(filename)
    
    def get_files(self):
        """Gets selected files"""
        return self.selected_files 