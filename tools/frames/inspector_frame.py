import tkinter as tk
from tkinter import ttk, scrolledtext
from ..base.tool_frame import BaseToolFrame
from ..processors.inspector_processor import InspectorProcessor
from ..utils.stats_formatter import StatsFormatter

class InspectorFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = InspectorProcessor()
        self.stats_formatter = StatsFormatter()
        self.create_tool_specific_widgets()
        
    @classmethod
    def get_tool_name(cls) -> str:
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
        """Analyzes and displays CSV statistics"""
        if not self.input_file:
            self.show_error("Please select a file first")
            return
            
        try:
            # Analyze the data with progress updates
            stats = self.processor.analyze_data(
                self.input_file,
                self.update_progress
            )
            
            # Format and display the statistics
            formatted_stats = self.stats_formatter.format_full_stats(stats)
            
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', formatted_stats)
            
        except Exception as e:
            self.show_error(str(e)) 