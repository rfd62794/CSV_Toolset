import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from .base_tool import BaseToolFrame

class OrderReverserFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
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
            variable=self.header_var
        ).pack(padx=5, pady=5)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create preview text widget
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
            text="Reverse Order",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to preview update
        self.file_path_var.trace_add('write', self.update_preview)
        
    def update_preview(self, *args):
        """Updates the preview when a file is selected"""
        if self.input_file:
            try:
                self.update_progress(0, "Reading file for preview...")
                # Read first and last few rows
                df_head = pd.read_csv(self.input_file, nrows=5)
                df_tail = pd.read_csv(self.input_file).tail(5)
                
                # Update preview text
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete('1.0', tk.END)
                
                self.preview_text.insert(tk.END, "First 5 rows:\n")
                self.preview_text.insert(tk.END, df_head.to_string())
                self.preview_text.insert(tk.END, "\n\nLast 5 rows:\n")
                self.preview_text.insert(tk.END, df_tail.to_string())
                
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
            total_rows = len(df)
            
            self.update_progress(33, "Reversing order...")
            
            if self.header_var.get():
                # Preserve header by excluding it from the reversal
                df_reversed = pd.concat([
                    df.iloc[:1],  # Keep header row
                    df.iloc[1:].iloc[::-1]  # Reverse all other rows
                ])
            else:
                # Reverse all rows including header
                df_reversed = df.iloc[::-1]
            
            self.update_progress(66, "Saving results...")
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                "reversed"
            )
            
            # Save the processed data
            df_reversed.to_csv(output_file, index=False)
            
            self.update_progress(100, 
                f"Complete! Reversed {total_rows:,} rows. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 