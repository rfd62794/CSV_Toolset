import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ..base.tool_frame import BaseToolFrame
from ..processors.appender_processor import AppenderProcessor
from ..widgets.list_selector import ListSelector

class AppenderFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = AppenderProcessor()
        self.secondary_file = None
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Column Appender"
        
    def create_tool_specific_widgets(self):
        # Secondary file selection
        self.secondary_frame = ttk.LabelFrame(self, text="Secondary File")
        self.secondary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.secondary_path_var = tk.StringVar()
        ttk.Entry(
            self.secondary_frame,
            textvariable=self.secondary_path_var,
            state='readonly',
            width=50
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            self.secondary_frame,
            text="Browse",
            command=self.browse_secondary
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Key column selection
        self.keys_frame = ttk.LabelFrame(self, text="Key Columns")
        self.keys_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Primary key selection
        primary_frame = ttk.Frame(self.keys_frame)
        primary_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(primary_frame, text="Primary Key:").pack(side=tk.LEFT)
        self.primary_key_selector = ListSelector(
            primary_frame,
            select_mode=tk.SINGLE
        )
        self.primary_key_selector.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Secondary key selection
        secondary_frame = ttk.Frame(self.keys_frame)
        secondary_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(secondary_frame, text="Secondary Key:").pack(side=tk.LEFT)
        self.secondary_key_selector = ListSelector(
            secondary_frame,
            select_mode=tk.SINGLE
        )
        self.secondary_key_selector.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Columns to add selection
        self.columns_frame = ttk.LabelFrame(self, text="Columns to Add")
        self.columns_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.columns_selector = ListSelector(
            self.columns_frame,
            title="Select columns to add from secondary file"
        )
        self.columns_selector.pack(fill=tk.BOTH, expand=True)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Append Columns",
            command=self.process_file,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selections to updates
        self.file_path_var.trace_add('write', self.update_primary_columns)
        self.secondary_path_var.trace_add('write', self.update_secondary_columns)
    
    def browse_secondary(self):
        """Opens file dialog for secondary file"""
        file_path = filedialog.askopenfilename(
            title="Select Secondary CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            valid, error = self.file_manager.validate_csv_file(file_path)
            if not valid:
                messagebox.showerror("Error", error)
                return
                
            self.secondary_file = file_path
            self.secondary_path_var.set(file_path)
    
    def update_primary_columns(self, *args):
        """Updates primary key selection when file is selected"""
        if self.input_file:
            try:
                columns = self.processor.get_columns(self.input_file)
                self.primary_key_selector.set_items(columns)
                self.check_ready()
            except Exception as e:
                self.show_error(str(e))
    
    def update_secondary_columns(self, *args):
        """Updates secondary columns when file is selected"""
        if self.secondary_file:
            try:
                columns = self.processor.get_columns(self.secondary_file)
                self.secondary_key_selector.set_items(columns)
                self.columns_selector.set_items(columns)
                self.check_ready()
            except Exception as e:
                self.show_error(str(e))
    
    def check_ready(self):
        """Enables process button if all selections are made"""
        if (self.input_file and self.secondary_file and 
            self.primary_key_selector.get_selected() and
            self.secondary_key_selector.get_selected()):
            self.process_btn.config(state=tk.NORMAL)
        else:
            self.process_btn.config(state=tk.DISABLED)
    
    def process_file(self):
        """Appends columns from secondary file"""
        if not self.columns_selector.get_selected():
            messagebox.showwarning("Warning", "Please select columns to add")
            return
            
        try:
            # Process files
            result, stats = self.processor.process_file(
                self.input_file,
                self.secondary_file,
                self.primary_key_selector.get_selected()[0],
                self.secondary_key_selector.get_selected()[0],
                self.columns_selector.get_selected(),
                progress_callback=self.update_progress
            )
            
            if not isinstance(result, pd.DataFrame):
                self.show_error(stats)  # stats contains error message
                return
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                f"appended_{stats['columns_added']}cols"
            )
            
            # Save results
            success, error = self.writer.write_csv(result, output_file)
            if not success:
                raise Exception(error)
            
            self.update_progress(100,
                f"Complete! Added {stats['columns_added']} columns. "
                f"Matched {stats['matched_rows']:,} of {stats['rows_before']:,} rows. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 