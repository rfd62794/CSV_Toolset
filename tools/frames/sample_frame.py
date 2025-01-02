import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
from ..base.tool_frame import BaseToolFrame
from ..processors.sample_processor import SampleProcessor
from ..widgets.options_frame import OptionsFrame
from ..widgets.tooltip import ToolTip

class SampleFrame(BaseToolFrame):
    """Frame for creating data samples"""
    
    def __init__(self, master):
        super().__init__(master)
        self.processor = SampleProcessor()
        self.create_tool_specific_widgets()
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Sample Maker"
    
    def create_tool_specific_widgets(self):
        # Add tooltips
        self.tooltip = ToolTip(self)
        
        # Sample size frame
        self.size_frame = ttk.LabelFrame(self, text="Sample Size")
        self.size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        size_frame = ttk.Frame(self.size_frame)
        size_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(size_frame, text="Number of rows:").pack(side=tk.LEFT)
        
        # Sample size entry with validation
        vcmd = (self.register(self._validate_size), '%P')
        self.size_var = tk.StringVar(value=str(self.processor.config.SAMPLE_SETTINGS['default_sample_size']))
        size_entry = ttk.Entry(
            size_frame,
            textvariable=self.size_var,
            validate='key',
            validatecommand=vcmd,
            width=10
        )
        size_entry.pack(side=tk.LEFT, padx=5)
        
        self.tooltip.bind_widget(
            size_entry,
            f"Enter a number between {self.processor.config.SAMPLE_SETTINGS['min_sample_size']} "
            f"and {self.processor.config.SAMPLE_SETTINGS['max_sample_size']:,}"
        )
        
        # Method selection
        self.method_frame = ttk.LabelFrame(self, text="Sampling Method")
        self.method_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.method_var = tk.StringVar(value='sequential')
        
        for text, value in self.processor.config.SAMPLE_SETTINGS['sampling_methods']:
            method_btn = ttk.Radiobutton(
                self.method_frame,
                text=text,
                value=value,
                variable=self.method_var,
                command=self._update_strat_visibility
            )
            method_btn.pack(anchor=tk.W, padx=5, pady=2)
            
            # Add tooltips for each method
            tooltips = {
                'sequential': "Takes the first N rows from the file",
                'random': "Takes a random sample of N rows",
                'stratified': "Takes a proportional sample based on groups in a column"
            }
            self.tooltip.bind_widget(method_btn, tooltips[value])
        
        # Stratification options
        self.strat_frame = ttk.Frame(self.method_frame)
        ttk.Label(self.strat_frame, text="Stratify by:").pack(side=tk.LEFT, padx=5)
        
        self.strat_var = tk.StringVar()
        self.strat_combo = ttk.Combobox(
            self.strat_frame,
            textvariable=self.strat_var,
            state='readonly',
            width=30
        )
        self.strat_combo.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(
            self.preview_frame,
            wrap=tk.WORD,
            height=10
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Process button
        self.process_btn = ttk.Button(
            self,
            text="Create Sample",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Bind events
        self.file_path_var.trace_add('write', self._update_columns)
        self.method_var.trace_add('write', self._update_preview)
        self.size_var.trace_add('write', self._update_preview)
        self.strat_var.trace_add('write', self._update_preview)
    
    def _validate_size(self, value: str) -> bool:
        """Validates sample size input"""
        if not value:
            return True
        try:
            size = int(value)
            min_size = self.processor.config.SAMPLE_SETTINGS['min_sample_size']
            return size >= min_size
        except ValueError:
            return False
    
    def _update_columns(self, *args):
        """Updates available columns when file is selected"""
        if self.input_file:
            try:
                columns = self.processor.get_columns(self.input_file)
                self.strat_combo['values'] = columns
                if columns:
                    self.strat_combo.current(0)
                self._update_preview()
            except Exception as e:
                self.show_error(str(e))
    
    def _update_strat_visibility(self, *args):
        """Shows/hides stratification options"""
        if self.method_var.get() == 'stratified':
            self.strat_frame.pack(fill=tk.X, pady=5)
        else:
            self.strat_frame.pack_forget()
        self._update_preview()
    
    def _update_preview(self, *args):
        """Updates preview when options change"""
        if not self.input_file:
            return
            
        try:
            # Get preview data
            preview_df = self.processor.reader.preview_data(self.input_file)
            
            # Get sample options - limit sample size to available rows for preview
            try:
                requested_size = int(self.size_var.get())
                preview_size = min(requested_size, len(preview_df))
            except ValueError:
                preview_size = len(preview_df)
                
            options = {
                'sample_size': preview_size,
                'method': self.method_var.get()
            }
            
            if options['method'] == 'stratified':
                options['strat_column'] = self.strat_var.get()
            
            # Create sample
            sample_df, stats = self.processor._process_data(preview_df, **options)
            
            # Update preview
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert(tk.END, "Original data:\n")
            self.preview_text.insert(tk.END, str(preview_df) + "\n\n")
            self.preview_text.insert(tk.END, "Sample preview:\n")
            self.preview_text.insert(tk.END, str(sample_df) + "\n\n")
            self.preview_text.insert(tk.END, 
                f"Preview showing {preview_size} rows (Full sample will use {requested_size:,} rows)"
            )
            
        except Exception as e:
            if 'sample_size' in str(e):  # Don't show errors for invalid sample sizes during typing
                return
            self.show_error(f"Preview error: {str(e)}")
    
    def process_file(self):
        """Creates a sample from the CSV file"""
        if not self.input_file:
            self.show_warning("Please select a file first")
            return
        
        try:
            # Get options
            sample_size = int(self.size_var.get())
            method = self.method_var.get()
            
            options = {
                'sample_size': sample_size,
                'method': method,
                'progress_callback': self.update_progress
            }
            
            if method == 'stratified':
                options['strat_column'] = self.strat_var.get()
            
            # Process file
            result_df, stats = self.processor.process_file(
                self.input_file,
                **options
            )
            
            # Generate output filename
            method_name = method.replace('_', '-')
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                f"sample_{method_name}_{stats['sampled_rows']}"
            )
            
            # Save results
            success, error = self.writer.write_csv(result_df, output_file)
            if not success:
                raise Exception(error)
            
            # Show success message
            message = (
                f"Complete! Created {method} sample with {stats['sampled_rows']:,} rows "
                f"({stats['sampling_rate']}) from {stats['total_rows']:,} total rows.\n"
                f"Saved to: {output_file}"
            )
            self.update_progress(100, message)
            
        except Exception as e:
            self.show_error(str(e)) 