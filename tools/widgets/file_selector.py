import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional

class FileSelector(ttk.LabelFrame):
    """Widget for file selection"""
    
    def __init__(self, parent, label_text="File", multiple=False):
        super().__init__(parent, text=label_text)
        
        self.multiple = multiple
        self.on_file_selected = None
        
        # Create frame for file selection
        self.file_frame = ttk.Frame(self)
        self.file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add file path entry
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(
            self.file_frame,
            textvariable=self.file_var,
            state='readonly'
        )
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add browse button
        self.browse_btn = ttk.Button(
            self.file_frame,
            text="Browse",
            command=self._browse_file
        )
        self.browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
    
    def _browse_file(self):
        """Opens file browser dialog"""
        if self.multiple:
            files = filedialog.askopenfilenames(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if files:
                self.file_var.set(';'.join(files))
                if self.on_file_selected:
                    self.on_file_selected(files)
        else:
            file = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if file:
                self.file_var.set(file)
                if self.on_file_selected:
                    self.on_file_selected(file)
    
    def get_file(self) -> str:
        """Gets selected file path"""
        return self.file_var.get()
    
    def set_file(self, file_path: str):
        """Sets file path"""
        self.file_var.set(file_path) 