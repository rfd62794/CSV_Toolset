import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from .base_tool import BaseToolFrame
from .processors.order_processor import OrderProcessor

class OrderReverserFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = OrderProcessor()
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Order Reverser"
        
    def create_tool_specific_widgets(self):
        # Options frame
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add option for header handling
        self.header_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame,
            text="Preserve header row",
            variable=self.header_var,
            command=self.update_preview
        ).pack(padx=5, pady=5)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create preview text widget
        self.preview_text = tk.Text(
            self.preview_frame,
            wrap=tk.NONE,
            height=20,
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
            text="Reverse Order",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to preview update
        self.file_path_var.trace_add('write', self.update_preview)
        
    def update_preview(self, *args):
        """Updates the preview when a file is selected or options change"""
        if self.input_file:
            try:
                self.update_progress(0, "Generating preview...")
                
                preview_data = self.processor.preview_data(
                    self.input_file,
                    preserve_header=self.header_var.get()
                )
                
                # Update preview text
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete('1.0', tk.END)
                
                # Show original data
                self.preview_text.insert('1.0', "Original Data:\n")
                self.preview_text.insert(tk.END, "First 5 rows:\n")
                self.preview_text.insert(tk.END, preview_data['original']['first'].to_string())
                self.preview_text.insert(tk.END, "\n\nLast 5 rows:\n")
                self.preview_text.insert(tk.END, preview_data['original']['last'].to_string())
                
                # Show reversed data
                self.preview_text.insert(tk.END, "\n\nReversed Data:\n")
                self.preview_text.insert(tk.END, "First 5 rows:\n")
                self.preview_text.insert(tk.END, preview_data['reversed']['first'].to_string())
                self.preview_text.insert(tk.END, "\n\nLast 5 rows:\n")
                self.preview_text.insert(tk.END, preview_data['reversed']['last'].to_string())
                
                self.preview_text.config(state=tk.DISABLED)
                self.status_var.set("Ready to reverse order")
                
            except Exception as e:
                self.show_error(f"Failed to generate preview: {str(e)}")
        
    def process_file(self):
        """Reverses the order of rows in the CSV file"""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
            
        try:
            self.update_progress(0, "Reading file...")
            df = pd.read_csv(self.input_file)
            
            self.update_progress(33, "Reversing order...")
            
            # Reverse the order
            df_reversed = self.processor.reverse_order(
                df,
                preserve_header=self.header_var.get()
            )
            
            self.update_progress(66, "Saving results...")
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                "reversed"
            )
            
            # Save the reversed data
            df_reversed.to_csv(output_file, index=False)
            
            self.update_progress(100, 
                f"Complete! Reversed {len(df):,} rows. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 