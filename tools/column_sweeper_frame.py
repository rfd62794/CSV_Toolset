import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from .base_tool import BaseToolFrame

class ColumnSweeperFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_tool_specific_widgets()
        self.columns = []
        
    def get_tool_name(self):
        return "Column Sweeper"
        
    def create_tool_specific_widgets(self):
        # Column selection area
        self.column_frame = ttk.LabelFrame(self, text="Column Selection")
        self.column_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create listbox for column selection
        self.column_listbox = tk.Listbox(
            self.column_frame,
            selectmode=tk.MULTIPLE,
            exportselection=False
        )
        self.column_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.column_frame,
            orient=tk.VERTICAL,
            command=self.column_listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.column_listbox.config(yscrollcommand=scrollbar.set)
        
        # Options frame
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add option for handling empty values
        self.empty_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame,
            text="Remove rows with empty strings",
            variable=self.empty_var
        ).pack(padx=5, pady=5)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Remove Rows",
            command=self.process_file,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to column update
        self.file_path_var.trace_add('write', self.update_columns)
        
    def update_columns(self, *args):
        """Updates the column listbox when a file is selected"""
        if self.input_file:
            try:
                self.update_progress(0, "Reading columns...")
                df = pd.read_csv(self.input_file, nrows=0)  # Read only header
                
                self.column_listbox.delete(0, tk.END)  # Clear existing items
                for col in df.columns:
                    self.column_listbox.insert(tk.END, col)
                
                self.process_btn.config(state=tk.NORMAL)
                self.status_var.set("Select columns and click 'Remove Rows'")
                
            except Exception as e:
                self.show_error(f"Failed to read columns: {str(e)}")
                self.process_btn.config(state=tk.DISABLED)
        
    def process_file(self):
        """Removes rows with missing data in selected columns"""
        selected_indices = self.column_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one column")
            return
            
        selected_columns = [self.column_listbox.get(i) for i in selected_indices]
        
        try:
            self.update_progress(0, "Reading file...")
            df = pd.read_csv(self.input_file)
            initial_rows = len(df)
            
            self.update_progress(33, "Processing...")
            
            # Remove rows with missing data in selected columns
            if self.empty_var.get():
                # Consider empty strings as missing values
                for col in selected_columns:
                    df = df[df[col].astype(str).str.strip() != '']
            
            df = df.dropna(subset=selected_columns)
            
            self.update_progress(66, "Saving results...")
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                f"swept_{len(selected_columns)}cols"
            )
            
            # Save the processed data
            df.to_csv(output_file, index=False)
            
            rows_removed = initial_rows - len(df)
            self.update_progress(100, 
                f"Complete! Removed {rows_removed:,} rows. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 