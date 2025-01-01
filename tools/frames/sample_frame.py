import tkinter as tk
from tkinter import ttk, messagebox
from ..base.tool_frame import BaseToolFrame
from ..processors.sample_processor import SampleProcessor

class SampleFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = SampleProcessor()
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Sample Maker"
        
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
        
        # Add sampling options
        self.random_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.options_frame,
            text="Use random sampling",
            variable=self.random_var
        ).pack(padx=5, pady=2)
        
        self.header_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame,
            text="Keep header row",
            variable=self.header_var
        ).pack(padx=5, pady=2)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Create Sample",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
    
    def validate_size(self, value):
        """Validates sample size input"""
        if not value:
            return True
        try:
            size = int(value)
            return size > 0
        except ValueError:
            return False
    
    def process_file(self):
        """Creates a sample from the CSV file"""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
            
        sample_size = self.size_var.get()
        if not sample_size:
            messagebox.showwarning("Warning", "Please enter a sample size")
            return
            
        try:
            # Process file and get results
            df_sample, stats = self.processor.process_file(
                self.input_file,
                sample_size,
                random=self.random_var.get(),
                keep_header=self.header_var.get(),
                progress_callback=self.update_progress
            )
            
            if not df_sample:
                self.show_error(stats)  # stats contains error message
                return
            
            # Generate output filename
            method = 'random' if self.random_var.get() else 'seq'
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                f"sample_{sample_size}_{method}"
            )
            
            # Save the sample
            success, error = self.writer.write_csv(df_sample, output_file)
            if not success:
                raise Exception(error)
            
            self.update_progress(100, 
                f"Complete! Created {stats['sampling_method']} sample with "
                f"{stats['sample_size']:,} rows. Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 