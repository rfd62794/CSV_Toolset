import tkinter as tk
from tkinter import ttk, filedialog
from ..csv_utils import CSVHandler, FileManager

class BaseToolFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.csv_handler = CSVHandler()
        self.file_manager = FileManager()
        
        # Common attributes
        self.input_file = None
        self.output_file = None
        
        # Create common layout
        self.create_base_layout()
        
    def create_base_layout(self):
        """Creates the basic layout common to all tools"""
        # Title area
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill=tk.X, padx=10, pady=(5, 15))
        
        self.title_label = ttk.Label(
            self.title_frame,
            text=self.get_tool_name(),
            font=('Helvetica', 14, 'bold')
        )
        self.title_label.pack(side=tk.LEFT)
        
        # File selection area
        self.file_frame = ttk.LabelFrame(self, text="File Selection")
        self.file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(
            self.file_frame,
            textvariable=self.file_path_var,
            width=50
        )
        self.file_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.browse_btn = ttk.Button(
            self.file_frame,
            text="Browse",
            command=self.browse_file
        )
        self.browse_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Progress area
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(
            self.progress_frame,
            textvariable=self.status_var
        )
        self.status_label.pack(fill=tk.X)
        
    def get_tool_name(self):
        """Override this in subclasses to set tool name"""
        return "CSV Tool"
        
    def browse_file(self):
        """Opens file dialog and sets the selected file path"""
        filename = filedialog.askopenfilename(
            title=f"Select CSV File for {self.get_tool_name()}",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
            self.input_file = filename
            
    def update_progress(self, value, status=""):
        """Updates progress bar and status message"""
        self.progress_var.set(value)
        if status:
            self.status_var.set(status)
        self.update_idletasks()
        
    def show_error(self, message):
        """Displays error message"""
        self.status_var.set(f"Error: {message}")
        
    def process_file(self):
        """Override this in subclasses to implement tool-specific processing"""
        raise NotImplementedError 