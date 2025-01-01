import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from .base_tool import BaseToolFrame
from .processors.column_appender_processor import ColumnAppenderProcessor

class ColumnAppenderFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = ColumnAppenderProcessor()
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Column Appender"
        
    def get_column_options(self):
        """Gets current column options from UI"""
        return {
            'column_name': self.name_var.get(),
            'default_value': self.value_var.get() or '',
            'position': self.position_var.get()
        }
        
    def create_tool_specific_widgets(self):
        # Column details frame
        self.details_frame = ttk.LabelFrame(self, text="New Column Details")
        self.details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Column name entry
        name_frame = ttk.Frame(self.details_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(name_frame, text="Column Name:").pack(side=tk.LEFT)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            name_frame,
            textvariable=self.name_var,
            width=30
        )
        self.name_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Value entry
        value_frame = ttk.Frame(self.details_frame)
        value_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(value_frame, text="Default Value:").pack(side=tk.LEFT)
        self.value_var = tk.StringVar()
        self.value_entry = ttk.Entry(
            value_frame,
            textvariable=self.value_var,
            width=30
        )
        self.value_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Options frame
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add option for position
        position_frame = ttk.Frame(self.options_frame)
        position_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.position_var = tk.StringVar(value="end")
        ttk.Label(position_frame, text="Column Position:").pack(side=tk.LEFT)
        
        positions = [
            ("At End", "end"),
            ("At Start", "start")
        ]
        
        for text, value in positions:
            ttk.Radiobutton(
                position_frame,
                text=text,
                value=value,
                variable=self.position_var
            ).pack(side=tk.LEFT, padx=5)
            
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Preview text widget
        self.preview_text = tk.Text(
            self.preview_frame,
            wrap=tk.NONE,
            height=10,
            width=50
        )
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(
            self.preview_frame,
            orient=tk.VERTICAL,
            command=self.preview_text.yview
        )
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = ttk.Scrollbar(
            self.preview_frame,
            orient=tk.HORIZONTAL,
            command=self.preview_text.xview
        )
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.preview_text.config(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
            state=tk.DISABLED
        )
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Add Column",
            command=self.process_file,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection and input changes to preview update
        self.file_path_var.trace_add('write', self.update_preview)
        self.name_var.trace_add('write', self.update_preview)
        self.value_var.trace_add('write', self.update_preview)
        self.position_var.trace_add('write', self.update_preview)
        
    def update_preview(self, *args):
        """Updates the preview when inputs change"""
        if self.input_file and self.name_var.get():
            try:
                self.update_progress(0, "Generating preview...")
                df = pd.read_csv(self.input_file, nrows=5)
                
                # Validate column name
                is_valid, error = self.processor.validate_column_name(
                    df,
                    self.name_var.get()
                )
                
                if not is_valid:
                    self.show_error(error)
                    self.process_btn.config(state=tk.DISABLED)
                    return
                
                # Generate preview
                options = self.get_column_options()
                preview_df = self.processor.preview_data(df, **options)
                
                # Update preview text
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete('1.0', tk.END)
                self.preview_text.insert('1.0', "Preview (first 5 rows):\n\n")
                self.preview_text.insert(tk.END, preview_df.to_string())
                self.preview_text.config(state=tk.DISABLED)
                
                # Enable process button
                self.process_btn.config(state=tk.NORMAL)
                
            except Exception as e:
                self.show_error(f"Failed to generate preview: {str(e)}")
                self.process_btn.config(state=tk.DISABLED)
        
    def process_file(self):
        """Adds the new column to the CSV file"""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
            
        column_name = self.name_var.get()
        if not column_name:
            messagebox.showwarning("Warning", "Please enter a column name")
            return
            
        try:
            self.update_progress(0, "Reading file...")
            df = pd.read_csv(self.input_file)
            
            # Validate column name
            is_valid, error = self.processor.validate_column_name(df, column_name)
            if not is_valid:
                if "already exists" in error:
                    if not messagebox.askyesno("Warning", f"Column '{column_name}' already exists. Overwrite?"):
                        return
                else:
                    messagebox.showwarning("Warning", error)
                    return
            
            self.update_progress(33, "Adding column...")
            
            # Add the new column
            options = self.get_column_options()
            df_modified = self.processor.add_column(df, **options)
            
            self.update_progress(66, "Saving results...")
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                f"added_{column_name}"
            )
            
            # Save the modified data
            df_modified.to_csv(output_file, index=False)
            
            self.update_progress(100, 
                f"Complete! Added column '{column_name}'. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 