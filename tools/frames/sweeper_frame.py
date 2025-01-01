import tkinter as tk
from tkinter import ttk, messagebox
from ..base.tool_frame import BaseToolFrame
from ..processors.sweeper_processor import SweeperProcessor
from ..widgets.list_selector import ListSelector

class SweeperFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = SweeperProcessor()
        self.create_tool_specific_widgets()
        
    @classmethod
    def get_tool_name(cls) -> str:
        return "Column Sweeper"
        
    def create_tool_specific_widgets(self):
        # Column selection area
        self.column_frame = ttk.LabelFrame(self, text="Column Selection")
        self.column_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Use common list selector widget
        self.column_selector = ListSelector(
            self.column_frame,
            title="Select columns to check for missing data"
        )
        self.column_selector.pack(fill=tk.BOTH, expand=True)
        
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
                columns = self.processor.get_columns(self.input_file)
                self.column_selector.set_items(columns)
                self.process_btn.config(state=tk.NORMAL)
                self.status_var.set("Select columns and click 'Remove Rows'")
            except Exception as e:
                self.show_error(f"Failed to read columns: {str(e)}")
                self.process_btn.config(state=tk.DISABLED)
    
    def process_file(self):
        """Removes rows with missing data in selected columns"""
        selected_columns = self.column_selector.get_selected()
        if not selected_columns:
            messagebox.showwarning("Warning", "Please select at least one column")
            return
            
        try:
            # Process file and get results
            df_clean, stats = self.processor.process_file(
                self.input_file,
                selected_columns,
                treat_empty_as_null=self.empty_var.get(),
                progress_callback=self.update_progress
            )
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                f"swept_{len(selected_columns)}cols"
            )
            
            # Save the cleaned data
            success, error = self.writer.write_csv(df_clean, output_file)
            if not success:
                raise Exception(error)
            
            self.update_progress(100, 
                f"Complete! Removed {stats['rows_removed']:,} rows. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 