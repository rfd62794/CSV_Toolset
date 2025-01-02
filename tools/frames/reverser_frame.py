import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from ..base.tool_frame import BaseToolFrame
from ..processors.reverser_processor import ReverserProcessor

class ReverserFrame(BaseToolFrame):
    """Frame for reversing row order in CSV files"""
    
    def __init__(self, master):
        super().__init__(master)
        self.processor = ReverserProcessor()
        self.create_tool_specific_widgets()
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Order Reverser"
    
    def create_tool_specific_widgets(self):
        # Options frame
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add header option
        self.header_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame,
            text="Keep header row at top",
            variable=self.header_var
        ).pack(padx=5, pady=5)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Reverse Order",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
    
    def process_file(self):
        """Reverses row order in CSV file"""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
            
        try:
            # Process file
            result_df, stats = self.processor.process_file(
                self.input_file,
                keep_header=self.header_var.get(),
                progress_callback=self.update_progress
            )
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                "reversed"
            )
            
            # Save results
            success, error = self.writer.write_csv(result_df, output_file)
            if not success:
                raise Exception(error)
            
            self.update_progress(100,
                f"Complete! Reversed {stats['total_rows']:,} rows. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 