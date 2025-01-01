import tkinter as tk
from tkinter import ttk, filedialog
from typing import Optional, Callable
from ..utils.file_manager import FileManager

class FileSelector(ttk.LabelFrame):
    """Reusable file selection widget"""
    
    def __init__(self, master, title="Select File", 
                 on_file_selected: Optional[Callable[[str], None]] = None):
        super().__init__(master, text=title)
        
        self.file_manager = FileManager()
        self.on_file_selected = on_file_selected
        self.file_path: Optional[str] = None
        
        self.path_var = tk.StringVar()
        self.create_widgets()
    
    def create_widgets(self):
        """Creates the file selection widgets"""
        ttk.Entry(
            self,
            textvariable=self.path_var,
            state='readonly',
            width=50
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            self,
            text="Browse",
            command=self.browse_file
        ).pack(side=tk.LEFT, padx=5, pady=5)
    
    def browse_file(self):
        """Opens file dialog"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            valid, error = self.file_manager.validate_csv_file(file_path)
            if not valid:
                messagebox.showerror("Error", error)
                return
                
            self.file_path = file_path
            self.path_var.set(file_path)
            
            if self.on_file_selected:
                self.on_file_selected(file_path)
    
    def get_file(self) -> Optional[str]:
        """Gets selected file path"""
        return self.file_path 