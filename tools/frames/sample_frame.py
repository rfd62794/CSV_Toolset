import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.sample_processor import SampleProcessor
from ..widgets.options_frame import OptionsFrame

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
        # Sample size frame with validation
        self.size_frame = ttk.LabelFrame(self, text="Sample Size")
        self.size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        size_frame = ttk.Frame(self.size_frame)
        size_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(size_frame, text="Number of rows:").pack(side=tk.LEFT)
        
        vcmd = (self.register(self._validate_size), '%P')
        self.size_var = tk.StringVar(value="100")
        self.size_entry = ttk.Entry(
            size_frame,
            textvariable=self.size_var,
            validate='key',
            validatecommand=vcmd,
            width=10
        )
        self.size_entry.pack(side=tk.LEFT, padx=5)
        
        # Method selection
        self.method_frame = ttk.LabelFrame(self, text="Sampling Method")
        self.method_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.method_var = tk.StringVar(value='sequential')
        methods = [
            ("Sequential (first N rows)", "sequential"),
            ("Random sampling", "random"),
            ("Stratified sampling", "stratified")
        ]
        
        for text, value in methods:
            ttk.Radiobutton(
                self.method_frame,
                text=text,
                value=value,
                variable=self.method_var,
                command=self._update_strat_visibility
            ).pack(anchor=tk.W, padx=5, pady=2)
        
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
        
        # Options
        self.options = OptionsFrame(self)
        self.options.pack(fill=tk.X, padx=10, pady=5)
        self.options.add_checkbox(
            'keep_header',
            "Keep header row",
            default=True
        )
        
        # Process button
        self.process_btn = ttk.Button(
            self,
            text="Create Sample",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Bind events
        self.file_path_var.trace_add('write', self._update_columns)
        self.method_var.trace_add('write', self._update_strat_visibility)
    
    def _validate_size(self, value: str) -> bool:
        """Validates sample size input"""
        if not value:
            return True
        try:
            size = int(value)
            return size > 0
        except ValueError:
            return False
    
    def _update_columns(self, *args):
        """Updates available columns for stratification"""
        if self.input_file:
            try:
                columns = self.processor.get_columns(self.input_file)
                self.strat_combo['values'] = columns
                if columns:
                    self.strat_combo.current(0)
            except Exception as e:
                self.show_error(str(e))
    
    def _update_strat_visibility(self, *args):
        """Shows/hides stratification options"""
        if self.method_var.get() == 'stratified':
            self.strat_frame.pack(fill=tk.X, pady=5)
        else:
            self.strat_frame.pack_forget()
    
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