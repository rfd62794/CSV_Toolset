import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
from .base_tool import BaseToolFrame
import os

class InspectorFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "CSV Inspector"
        
    def create_tool_specific_widgets(self):
        # Create stats display area
        self.stats_frame = ttk.LabelFrame(self, text="CSV Statistics")
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create scrolled text widget for stats
        self.stats_text = scrolledtext.ScrolledText(
            self.stats_frame,
            wrap=tk.WORD,
            width=60,
            height=20
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add inspect button
        self.inspect_btn = ttk.Button(
            self,
            text="Inspect CSV",
            command=self.process_file
        )
        self.inspect_btn.pack(pady=10)
        
    def process_file(self):
        if not self.input_file:
            self.show_error("Please select a file first")
            return
            
        try:
            self.update_progress(0, "Reading file...")
            
            # Get basic file info
            file_size = os.path.getsize(self.input_file)
            encoding = self.csv_handler.detect_encoding(self.input_file)
            
            self.update_progress(20, "Analyzing data...")
            
            # Read with pandas for detailed analysis
            df = pd.read_csv(self.input_file, encoding=encoding)
            
            self.update_progress(60, "Generating statistics...")
            
            # Generate stats
            stats = [
                f"File Statistics:",
                f"- Size: {file_size:,} bytes",
                f"- Encoding: {encoding}",
                f"- Rows: {len(df):,}",
                f"- Columns: {len(df.columns):,}",
                "\nColumn Information:",
            ]
            
            for col in df.columns:
                stats.extend([
                    f"\n{col}:",
                    f"- Type: {df[col].dtype}",
                    f"- Unique Values: {df[col].nunique():,}",
                    f"- Null Count: {df[col].isnull().sum():,}",
                ])
                
            self.update_progress(100, "Analysis complete!")
            
            # Display stats
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', '\n'.join(stats))
            
        except Exception as e:
            self.show_error(str(e)) 