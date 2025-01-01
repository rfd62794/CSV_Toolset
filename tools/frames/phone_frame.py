import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from ..base.tool_frame import BaseToolFrame
from ..processors.phone_processor import PhoneProcessor
from ..widgets.options_frame import OptionsFrame
from ..widgets.list_selector import ListSelector

class PhoneFrame(BaseToolFrame):
    """Frame for extracting phone numbers from CSV columns"""
    
    def __init__(self, master):
        super().__init__(master)
        self.processor = PhoneProcessor()
        self.create_tool_specific_widgets()
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Phone Extractor"
    
    def create_tool_specific_widgets(self):
        """Creates the phone extractor specific widgets"""
        # Column selection
        self.column_frame = ttk.LabelFrame(self, text="Column Selection")
        self.column_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.column_selector = ListSelector(
            self.column_frame,
            "Select columns to search for phone numbers:"
        )
        self.column_selector.pack(fill=tk.X, padx=5, pady=5)
        
        # Options frame
        self.options = OptionsFrame(self)
        self.options.pack(fill=tk.X, padx=10, pady=5)
        
        # Add options
        self.options.add_checkbox(
            'keep_original',
            "Keep original columns",
            default=True
        )
        
        self.options.add_checkbox(
            'format_numbers',
            "Format phone numbers",
            default=True
        )
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Extract Phone Numbers",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to column update
        self.file_path_var.trace_add('write', self.update_columns)
    
    def update_columns(self, *args):
        """Updates available columns when file is selected"""
        if self.input_file:
            try:
                columns = self.processor.get_columns(self.input_file)
                self.column_selector.set_options(columns)
            except Exception as e:
                self.show_error(str(e))
    
    def process_file(self):
        """Processes the selected file"""
        if not self.input_file:
            self.show_warning("Please select a file first")
            return
            
        selected_columns = self.column_selector.get_selected()
        if not selected_columns:
            self.show_warning("Please select at least one column")
            return
            
        try:
            # Process file
            result, stats = self.processor.process_file(
                self.input_file,
                columns=selected_columns,
                keep_original=self.options.get_option('keep_original'),
                format_numbers=self.options.get_option('format_numbers'),
                progress_callback=self.update_progress
            )
            
            if not isinstance(result, pd.DataFrame):
                self.show_error(stats)  # stats contains error message
                return
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                "phones"
            )
            
            # Save results
            success, error = self.writer.write_csv(result, output_file)
            if not success:
                raise Exception(error)
            
            self.update_progress(100,
                f"Complete! Found {stats['phones_found']:,} phone numbers. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 