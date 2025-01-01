import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import chardet
from .base_tool import BaseToolFrame

class ReformatterFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Data Reformatter"
        
    def create_tool_specific_widgets(self):
        # Options frame
        self.options_frame = ttk.LabelFrame(self, text="Cleaning Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add cleaning options
        self.create_cleaning_options()
        
        # Encoding frame
        self.encoding_frame = ttk.LabelFrame(self, text="Encoding")
        self.encoding_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add encoding options
        self.create_encoding_options()
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create preview with both original and cleaned text
        self.create_preview_area()
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Clean and Reformat",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to preview update
        self.file_path_var.trace_add('write', self.update_preview)
        
    def create_cleaning_options(self):
        """Creates the cleaning options checkboxes"""
        # Remove non-printable characters
        self.nonprint_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame,
            text="Remove non-printable characters",
            variable=self.nonprint_var
        ).pack(padx=5, pady=2, anchor=tk.W)
        
        # Remove null bytes
        self.null_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame,
            text="Remove null bytes",
            variable=self.null_var
        ).pack(padx=5, pady=2, anchor=tk.W)
        
        # Convert to ASCII
        self.ascii_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.options_frame,
            text="Convert to ASCII (remove non-ASCII characters)",
            variable=self.ascii_var
        ).pack(padx=5, pady=2, anchor=tk.W)
        
    def create_encoding_options(self):
        """Creates the encoding selection options"""
        # Auto-detect encoding
        self.autodetect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.encoding_frame,
            text="Auto-detect input encoding",
            variable=self.autodetect_var,
            command=self.toggle_encoding_input
        ).pack(padx=5, pady=2, anchor=tk.W)
        
        # Manual encoding selection
        manual_frame = ttk.Frame(self.encoding_frame)
        manual_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(manual_frame, text="Input encoding:").pack(side=tk.LEFT)
        
        self.encoding_var = tk.StringVar(value='utf-8')
        self.encoding_combo = ttk.Combobox(
            manual_frame,
            textvariable=self.encoding_var,
            values=['utf-8', 'ascii', 'latin-1', 'cp1252', 'utf-16'],
            width=15,
            state='disabled'
        )
        self.encoding_combo.pack(side=tk.LEFT, padx=(5, 0))
        
    def create_preview_area(self):
        """Creates the split preview area showing before/after"""
        preview_paned = ttk.PanedWindow(self.preview_frame, orient=tk.HORIZONTAL)
        preview_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Original text preview
        original_frame = ttk.LabelFrame(preview_paned, text="Original")
        preview_paned.add(original_frame, weight=1)
        
        self.original_text = tk.Text(
            original_frame,
            wrap=tk.NONE,
            height=10,
            width=40
        )
        self.original_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        orig_y_scroll = ttk.Scrollbar(
            original_frame,
            orient=tk.VERTICAL,
            command=self.original_text.yview
        )
        orig_y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.original_text.config(yscrollcommand=orig_y_scroll.set)
        
        # Cleaned text preview
        cleaned_frame = ttk.LabelFrame(preview_paned, text="Cleaned")
        preview_paned.add(cleaned_frame, weight=1)
        
        self.cleaned_text = tk.Text(
            cleaned_frame,
            wrap=tk.NONE,
            height=10,
            width=40
        )
        self.cleaned_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        clean_y_scroll = ttk.Scrollbar(
            cleaned_frame,
            orient=tk.VERTICAL,
            command=self.cleaned_text.yview
        )
        clean_y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.cleaned_text.config(yscrollcommand=clean_y_scroll.set)
        
        # Configure both text widgets as read-only
        self.original_text.config(state=tk.DISABLED)
        self.cleaned_text.config(state=tk.DISABLED)
        
    def toggle_encoding_input(self):
        """Enables/disables manual encoding selection"""
        state = 'disabled' if self.autodetect_var.get() else 'readonly'
        self.encoding_combo.config(state=state)
        
    def clean_text(self, text):
        """Applies the selected cleaning operations to text"""
        if not text:
            return text
            
        result = str(text)
        
        if self.null_var.get():
            result = result.replace('\x00', '')
            
        if self.nonprint_var.get():
            result = ''.join(c for c in result if c.isprintable())
            
        if self.ascii_var.get():
            result = result.encode('ascii', errors='ignore').decode('ascii')
            
        return result
        
    def update_preview(self, *args):
        """Updates the preview when a file is selected"""
        if self.input_file:
            try:
                self.update_progress(0, "Reading file for preview...")
                
                # Detect encoding if auto-detect is enabled
                encoding = None
                if self.autodetect_var.get():
                    with open(self.input_file, 'rb') as f:
                        raw_data = f.read()
                        result = chardet.detect(raw_data)
                        encoding = result['encoding']
                else:
                    encoding = self.encoding_var.get()
                
                # Read first few rows
                df = pd.read_csv(self.input_file, nrows=5, encoding=encoding)
                
                # Update preview texts
                self.original_text.config(state=tk.NORMAL)
                self.cleaned_text.config(state=tk.NORMAL)
                
                self.original_text.delete('1.0', tk.END)
                self.cleaned_text.delete('1.0', tk.END)
                
                # Show original and cleaned versions
                original = df.to_string()
                cleaned = self.clean_text(original)
                
                self.original_text.insert('1.0', original)
                self.cleaned_text.insert('1.0', cleaned)
                
                self.original_text.config(state=tk.DISABLED)
                self.cleaned_text.config(state=tk.DISABLED)
                
                self.status_var.set("Ready to clean data")
                
            except Exception as e:
                self.show_error(f"Failed to generate preview: {str(e)}")
        
    def process_file(self):
        """Cleans and reformats the entire CSV file"""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
            
        try:
            self.update_progress(0, "Reading file...")
            
            # Determine encoding
            encoding = None
            if self.autodetect_var.get():
                with open(self.input_file, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']
            else:
                encoding = self.encoding_var.get()
            
            # Read the CSV file
            df = pd.read_csv(self.input_file, encoding=encoding)
            total_cells = df.size
            processed_cells = 0
            
            self.update_progress(20, "Cleaning data...")
            
            # Clean each cell in the dataframe
            for col in df.columns:
                df[col] = df[col].apply(self.clean_text)
                processed_cells += len(df)
                self.update_progress(
                    20 + (processed_cells / total_cells * 60),
                    f"Cleaning column: {col}"
                )
            
            self.update_progress(80, "Saving results...")
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                "cleaned"
            )
            
            # Save the cleaned data
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            self.update_progress(100, 
                f"Complete! Cleaned {total_cells:,} cells. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 