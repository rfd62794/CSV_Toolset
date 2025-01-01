import tkinter as tk
from tkinter import ttk, messagebox
from .base_tool import BaseToolFrame
from .processors.reformatter_processor import DataReformatter

class ReformatterFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master)
        self.processor = DataReformatter()
        self.create_tool_specific_widgets()
        
    def get_tool_name(self):
        return "Data Reformatter"
        
    def get_cleaning_options(self):
        """Gets current cleaning options from UI"""
        return {
            'remove_null': self.null_var.get(),
            'remove_nonprint': self.nonprint_var.get(),
            'convert_ascii': self.ascii_var.get()
        }
    
    def update_preview(self, *args):
        """Updates the preview when a file is selected"""
        if self.input_file:
            try:
                self.update_progress(0, "Reading file for preview...")
                
                encoding = None
                if self.autodetect_var.get():
                    encoding = self.processor.detect_encoding(self.input_file)
                else:
                    encoding = self.encoding_var.get()
                
                options = self.get_cleaning_options()
                original, cleaned = self.processor.preview_data(
                    self.input_file,
                    options,
                    encoding
                )
                
                # Update preview texts
                self.update_preview_text(original, cleaned)
                self.status_var.set("Ready to clean data")
                
            except Exception as e:
                self.show_error(f"Failed to generate preview: {str(e)}")
    
    def process_file(self):
        """Processes the file using the reformatter"""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
            
        try:
            self.update_progress(0, "Reading file...")
            
            encoding = None
            if self.autodetect_var.get():
                encoding = self.processor.detect_encoding(self.input_file)
            else:
                encoding = self.encoding_var.get()
            
            options = self.get_cleaning_options()
            
            # Process the file with progress updates
            df = self.processor.process_file(
                self.input_file,
                options,
                encoding,
                self.update_progress
            )
            
            self.update_progress(80, "Saving results...")
            
            # Generate output filename and save
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                "cleaned"
            )
            
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            self.update_progress(100, 
                f"Complete! Cleaned {df.size:,} cells. "
                f"Saved to: {output_file}"
            )
            
        except Exception as e:
            self.show_error(str(e))
    
    # ... rest of the UI-specific code ... 