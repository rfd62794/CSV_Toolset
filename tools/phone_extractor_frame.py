import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import re
from .base_tool import BaseToolFrame

class PhoneExtractorFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Phone Extractor"
        
    def create_tool_specific_widgets(self):
        # Column selection frame
        self.column_frame = ttk.LabelFrame(self, text="Column Selection")
        self.column_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Column selection combobox
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(
            self.column_frame,
            textvariable=self.column_var,
            state="readonly",
            width=40
        )
        self.column_combo.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Options frame
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Format options
        self.format_var = tk.StringVar(value="standard")
        formats = [
            ("Standard (XXX-XXX-XXXX)", "standard"),
            ("Plain (XXXXXXXXXX)", "plain"),
            ("Parentheses ((XXX) XXX-XXXX)", "parentheses")
        ]
        
        for text, value in formats:
            ttk.Radiobutton(
                self.options_frame,
                text=text,
                value=value,
                variable=self.format_var
            ).pack(padx=5, pady=2, anchor=tk.W)
            
        # Add option for strict mode
        self.strict_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame,
            text="Strict mode (only extract 10-digit numbers)",
            variable=self.strict_var
        ).pack(padx=5, pady=5)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Preview text widget
        self.preview_text = tk.Text(
            self.preview_frame,
            wrap=tk.WORD,
            height=10,
            width=50
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.preview_text.config(state=tk.DISABLED)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Extract Phone Numbers",
            command=self.process_file,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to column update
        self.file_path_var.trace_add('write', self.update_columns)
        # Bind column selection to preview update
        self.column_var.trace_add('write', self.update_preview)
        
    def update_columns(self, *args):
        """Updates the column selection when a file is selected"""
        if self.input_file:
            try:
                self.update_progress(0, "Reading columns...")
                df = pd.read_csv(self.input_file, nrows=0)
                
                self.column_combo['values'] = list(df.columns)
                self.process_btn.config(state=tk.NORMAL)
                self.status_var.set("Select a column and click 'Extract Phone Numbers'")
                
            except Exception as e:
                self.show_error(f"Failed to read columns: {str(e)}")
                self.process_btn.config(state=tk.DISABLED)
                
    def update_preview(self, *args):
        """Updates the preview with sample phone numbers from selected column"""
        if self.input_file and self.column_var.get():
            try:
                self.update_progress(0, "Generating preview...")
                df = pd.read_csv(self.input_file, nrows=5)
                column = self.column_var.get()
                
                # Update preview text
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete('1.0', tk.END)
                
                preview = ["Sample data from selected column:"]
                for value in df[column].head():
                    preview.append(f"Original: {value}")
                    formatted = self.format_phone_number(str(value))
                    if formatted:
                        preview.append(f"Formatted: {formatted}\n")
                    else:
                        preview.append("No valid phone number found\n")
                
                self.preview_text.insert('1.0', '\n'.join(preview))
                self.preview_text.config(state=tk.DISABLED)
                
            except Exception as e:
                self.show_error(f"Failed to generate preview: {str(e)}")
                
    def format_phone_number(self, value):
        """Formats a phone number according to selected format"""
        # Remove all non-numeric characters
        numbers = re.sub(r'\D', '', str(value))
        
        # In strict mode, only accept 10-digit numbers
        if self.strict_var.get() and len(numbers) != 10:
            return None
            
        # If not strict, try to extract last 10 digits
        if len(numbers) > 10:
            numbers = numbers[-10:]
        elif len(numbers) < 10:
            return None
            
        # Format according to selected style
        format_style = self.format_var.get()
        if format_style == "plain":
            return numbers
        elif format_style == "standard":
            return f"{numbers[:3]}-{numbers[3:6]}-{numbers[6:]}"
        else:  # parentheses
            return f"({numbers[:3]}) {numbers[3:6]}-{numbers[6:]}"
        
    def process_file(self):
        """Extracts and formats phone numbers from the selected column"""
        if not self.input_file or not self.column_var.get():
            messagebox.showwarning("Warning", "Please select a file and column")
            return
            
        try:
            self.update_progress(0, "Reading file...")
            df = pd.read_csv(self.input_file)
            column = self.column_var.get()
            
            self.update_progress(33, "Extracting phone numbers...")
            
            # Create new dataframe with just the phone numbers
            phone_numbers = []
            total_rows = len(df)
            
            for idx, value in enumerate(df[column]):
                formatted = self.format_phone_number(value)
                phone_numbers.append(formatted if formatted else '')
                
                if idx % 1000 == 0:  # Update progress periodically
                    self.update_progress(
                        33 + (idx / total_rows * 33),
                        f"Processing row {idx:,} of {total_rows:,}"
                    )
            
            self.update_progress(66, "Saving results...")
            
            # Create output dataframe
            output_df = pd.DataFrame({
                'Original': df[column],
                'Formatted_Phone': phone_numbers
            })
            
            # Generate output filename
            format_type = self.format_var.get()
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                f"phones_{format_type}"
            )
            
            # Save the extracted numbers
            output_df.to_csv(output_file, index=False)
            
            # Count valid numbers
            valid_numbers = sum(1 for num in phone_numbers if num)
            
            self.update_progress(100, 
                f"Complete! Extracted {valid_numbers:,} phone numbers. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e)) 