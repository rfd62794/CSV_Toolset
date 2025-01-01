import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .utils.file_manager import FileManager

class BaseToolFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.file_manager = FileManager()
        self.input_file = None
        self.create_base_widgets()
        
    def create_base_widgets(self):
        # File selection frame
        self.file_frame = ttk.LabelFrame(self, text="File Selection")
        self.file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # File path display
        self.file_path_var = tk.StringVar()
        ttk.Entry(
            self.file_frame,
            textvariable=self.file_path_var,
            state='readonly',
            width=50
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Browse button
        ttk.Button(
            self.file_frame,
            text="Browse",
            command=self.browse_file
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Select a CSV file to begin")
        self.status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Progress bar
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(
            self,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10)
        
    def browse_file(self):
        """Opens file dialog and validates selected file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            # Validate file
            is_valid, error = self.file_manager.validate_csv_file(file_path)
            if not is_valid:
                messagebox.showerror("Error", error)
                return
                
            self.input_file = file_path
            self.file_path_var.set(file_path)
            
    def update_progress(self, value, message=None):
        """Updates progress bar and status message"""
        self.progress_var.set(value)
        if message:
            self.status_var.set(message)
        self.update()
        
    def show_error(self, message):
        """Shows error message and resets progress"""
        messagebox.showerror("Error", message)
        self.update_progress(0, "Error occurred") 