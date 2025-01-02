import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
from ..base.tool_frame import BaseToolFrame
from ..processors.reverser_processor import ReverserProcessor
from ..widgets.tooltip import ToolTip

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
        # Add tooltips for better UX
        self.tooltip = ToolTip(self)
        
        # Add preview option
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add header option with tooltip
        self.header_var = tk.BooleanVar(value=True)
        header_btn = ttk.Checkbutton(
            self.options_frame,
            text="Keep header row at top",
            variable=self.header_var
        )
        header_btn.pack(padx=5, pady=5)
        self.tooltip.bind_widget(
            header_btn,
            "Keep the first row (header) in place while reversing all other rows"
        )
        
        # Add preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.preview_text = ScrolledText(
            self.preview_frame,
            wrap=tk.WORD,
            height=10
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Reverse Order",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Bind events
        self.file_path_var.trace_add('write', self.update_preview)
        self.header_var.trace_add('write', self.update_preview)
    
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
    
    def update_preview(self, *args):
        """Updates preview when file is selected"""
        if self.input_file:
            try:
                # Show first few rows of original and reversed data
                preview_df = self.processor.reader.preview_data(self.input_file)
                reversed_df, _ = self.processor.process_data(
                    preview_df,
                    keep_header=self.header_var.get()
                )
                
                self.preview_text.delete('1.0', tk.END)
                self.preview_text.insert(tk.END, "Original data:\n")
                self.preview_text.insert(tk.END, str(preview_df) + "\n\n")
                self.preview_text.insert(tk.END, "Reversed data:\n")
                self.preview_text.insert(tk.END, str(reversed_df))
                
            except Exception as e:
                self.show_error(f"Preview error: {str(e)}") 