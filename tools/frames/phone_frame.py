import tkinter as tk
from tkinter import ttk, messagebox
from ..base.tool_frame import BaseToolFrame
from ..processors.phone_processor import PhoneProcessor
from ..widgets.list_selector import ListSelector

class PhoneFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = PhoneProcessor()
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Phone Extractor"
        
    def create_tool_specific_widgets(self):
        # Column selection
        self.column_frame = ttk.LabelFrame(self, text="Source Column")
        self.column_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.column_selector = ListSelector(
            self.column_frame,
            title="Select column containing phone numbers",
            select_mode=tk.SINGLE
        )
        self.column_selector.pack(fill=tk.X, expand=True)
        
        # Options frame
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Pattern selection
        ttk.Label(self.options_frame, text="Pattern:").pack(anchor=tk.W, padx=5)
        self.pattern_var = tk.StringVar(value='us')
        for text, value in [("US Numbers", "us"), ("International", "international")]:
            ttk.Radiobutton(
                self.options_frame,
                text=text,
                value=value,
                variable=self.pattern_var
            ).pack(anchor=tk.W, padx=20)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Extract Numbers",
            command=self.process_file,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to column update
        self.file_path_var.trace_add('write', self.update_columns)
        
    def update_columns(self, *args):
        """Updates column list when file is selected"""
        if self.input_file:
            try:
                columns = self.processor.reader.get_columns(self.input_file)
                self.column_selector.set_items(columns)
                self.process_btn.config(state=tk.NORMAL)
            except Exception as e:
                self.show_error(str(e))
                self.process_btn.config(state=tk.DISABLED)
    
    def process_file(self):
        """Extracts phone numbers from selected column"""
        selected = self.column_selector.get_selected()
        if not selected:
            messagebox.showwarning("Warning", "Please select a source column")
            return
            
        try:
            # Process file
            result, stats = self.processor.process_file(
                self.input_file,
                selected[0],
                pattern_type=self.pattern_var.get(),
                progress_callback=self.update_progress
            )
            
            if not isinstance(result, pd.DataFrame):
                self.show_error(stats)  # stats contains error message
                return
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                "phones_extracted"
            )
            
            # Save results
            success, error = self.writer.write_csv(result, output_file)
            if not success:
                raise Exception(error)
            
            self.update_progress(100,
                f"Complete! Found {stats['numbers_found']:,} phone numbers "
                f"({stats['success_rate']}). Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 