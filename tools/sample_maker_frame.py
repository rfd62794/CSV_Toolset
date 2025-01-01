import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from .base_tool import BaseToolFrame
from .processors.sample_processor import SampleProcessor

class SampleMakerFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = SampleProcessor()
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Sample Maker"
        
    def get_sample_options(self):
        """Gets current sampling options from UI"""
        return {
            'random': self.random_var.get(),
            'keep_header': self.header_var.get()
        }
        
    def create_tool_specific_widgets(self):
        # Sample size frame
        self.size_frame = ttk.LabelFrame(self, text="Sample Size")
        self.size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add size entry with validation
        vcmd = (self.register(self.validate_size), '%P')
        self.size_var = tk.StringVar()
        self.size_entry = ttk.Entry(
            self.size_frame,
            textvariable=self.size_var,
            validate='key',
            validatecommand=vcmd,
            width=15
        )
        self.size_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add "rows" label
        ttk.Label(self.size_frame, text="rows").pack(side=tk.LEFT, padx=(0, 5), pady=5)
        
        # Options frame
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add option for random sampling
        self.random_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.options_frame,
            text="Random sampling",
            variable=self.random_var
        ).pack(padx=5, pady=5)
        
        # Add option to keep header
        self.header_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame,
            text="Keep header row",
            variable=self.header_var
        ).pack(padx=5, pady=5)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="File Info")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Info text widget
        self.info_text = tk.Text(
            self.preview_frame,
            wrap=tk.WORD,
            height=6,
            width=50
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.info_text.config(state=tk.DISABLED)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Create Sample",
            command=self.process_file,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to info update
        self.file_path_var.trace_add('write', self.update_file_info)
        
    def validate_size(self, value):
        """Validates that the size entry contains only digits"""
        if value == "":
            return True
        return value.isdigit()
        
    def update_file_info(self, *args):
        """Updates the file information display when a file is selected"""
        if self.input_file:
            try:
                self.update_progress(0, "Reading file info...")
                
                file_info = self.processor.get_file_info(self.input_file)
                
                # Update info text
                self.info_text.config(state=tk.NORMAL)
                self.info_text.delete('1.0', tk.END)
                
                info = [
                    f"Total rows: {file_info['total_rows']:,}",
                    f"Number of columns: {file_info['num_columns']}",
                    f"\nEnter the desired sample size (1 to {file_info['total_rows']:,})",
                    "\nNote: Header row will be preserved by default"
                ]
                
                self.info_text.insert('1.0', '\n'.join(info))
                self.info_text.config(state=tk.DISABLED)
                
                self.process_btn.config(state=tk.NORMAL)
                self.status_var.set("Ready to create sample")
                
            except Exception as e:
                self.show_error(f"Failed to read file info: {str(e)}")
                self.process_btn.config(state=tk.DISABLED)
        
    def process_file(self):
        """Creates a sample CSV file with the specified number of rows"""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
            
        sample_size = self.size_var.get()
        if not sample_size:
            messagebox.showwarning("Warning", "Please enter a sample size")
            return
            
        try:
            # Validate sample size
            is_valid, error = self.processor.validate_sample_size(
                self.input_file,
                sample_size
            )
            
            if not is_valid:
                messagebox.showwarning("Warning", error)
                return
                
            sample_size = int(sample_size)
            self.update_progress(33, "Creating sample...")
            
            # Get sampling options and create sample
            options = self.get_sample_options()
            df_sample = self.processor.create_sample(
                self.input_file,
                sample_size,
                **options
            )
            
            self.update_progress(66, "Saving sample...")
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                f"sample_{sample_size}"
            )
            
            # Save the sample
            df_sample.to_csv(output_file, index=False)
            
            self.update_progress(100, 
                f"Complete! Created sample with {sample_size:,} rows. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 