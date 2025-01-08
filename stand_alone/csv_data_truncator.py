"""
A standalone script for truncating data in CSV files to a specified length.
Follows SOLID principles and PEP 8 guidelines.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import chardet
import logging
import os
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class CSVFileHandler:
    """Handles CSV file operations including encoding detection and I/O."""
    
    ENCODINGS_TO_TRY = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    
    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """
        Detects the encoding of a file with multiple fallback options.
        Returns the first working encoding.
        """
        logger.info(f"Detecting encoding for file: {file_path}")
        
        # Try chardet first
        try:
            with open(file_path, 'rb') as f:
                rawdata = f.read()
            detected = chardet.detect(rawdata)
            if detected['confidence'] > 0.7:
                encoding = detected['encoding']
                logger.info(f"Chardet detected encoding: {encoding} with confidence: {detected['confidence']}")
                if CSVFileHandler._test_encoding(file_path, encoding):
                    return encoding
        except Exception as e:
            logger.warning(f"Chardet detection failed: {str(e)}")

        # Try common encodings
        for encoding in CSVFileHandler.ENCODINGS_TO_TRY:
            logger.info(f"Trying encoding: {encoding}")
            if CSVFileHandler._test_encoding(file_path, encoding):
                logger.info(f"Successfully found working encoding: {encoding}")
                return encoding
        
        # Default to utf-8 if nothing else works
        logger.warning("No encoding detected, defaulting to utf-8")
        return 'utf-8'

    @staticmethod
    def _test_encoding(file_path: str, encoding: str) -> bool:
        """Tests if an encoding can successfully read the file."""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                # Try to read first few lines
                for _ in range(5):
                    f.readline()
            return True
        except Exception:
            return False

    @staticmethod
    def read_headers(file_path: str, encoding: str) -> list:
        """Reads and returns the header row from a CSV file."""
        logger.info("Reading headers from file")
        with open(file_path, 'r', newline='', encoding=encoding) as f:
            return next(csv.reader(f))

    @staticmethod
    def count_rows(file_path: str, encoding: str) -> int:
        """Counts the total number of rows in the CSV file."""
        logger.info("Counting total rows")
        with open(file_path, 'r', newline='', encoding=encoding) as f:
            return sum(1 for _ in f) - 1  # Subtract 1 for header


class DataTruncator:
    """Handles the data truncation logic."""
    
    @staticmethod
    def truncate_data(row: list, column_index: int, length: int) -> list:
        """Truncates data in the specified column to the given length."""
        try:
            original = row[column_index]
            row[column_index] = str(row[column_index])[:length]
            if len(original) > length:
                logger.debug(f"Truncated value from {original} to {row[column_index]}")
        except IndexError:
            logger.warning(f"Row has fewer columns than expected: {row}")
        return row


class CSVProcessor:
    """Coordinates CSV processing operations."""
    
    def __init__(self):
        self.file_handler = CSVFileHandler()
        self.truncator = DataTruncator()

    def process_file(self, input_file: str, output_file: str,
                    column_index: int, length: int, encoding: str,
                    progress_callback: Optional[callable] = None) -> bool:
        """Processes the CSV file, truncating data in the specified column."""
        try:
            logger.info(f"Starting file processing: {input_file}")
            total_rows = self.file_handler.count_rows(input_file, encoding)
            processed_rows = 0
            
            with open(input_file, 'r', newline='', encoding=encoding) as infile, \
                 open(output_file, 'w', newline='', encoding=encoding) as outfile:
                
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                
                # Write header row unchanged
                header = next(reader)
                writer.writerow(header)
                logger.info(f"Processing column: {header[column_index]}")
                
                # Process data rows
                for row in reader:
                    processed_row = self.truncator.truncate_data(row, column_index, length)
                    writer.writerow(processed_row)
                    
                    processed_rows += 1
                    if progress_callback and processed_rows % 100 == 0:
                        progress = (processed_rows / total_rows) * 100
                        progress_callback(progress)
                        logger.debug(f"Progress: {progress:.1f}%")
            
            logger.info(f"Processing complete. Processed {processed_rows} rows")
            return True
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}", exc_info=True)
            return False


class GUI:
    """Handles the graphical user interface."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CSV Data Truncator")
        self.processor = CSVProcessor()
        self.setup_ui()
        
        # Instance variables
        self.input_file: Optional[str] = None
        self.encoding: Optional[str] = None
        self.columns: list = []
        
        logger.info("GUI initialized")

    def setup_ui(self):
        """Sets up the user interface components."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        tk.Button(main_frame, text="Select CSV File",
                 command=self.select_file).pack(pady=10)
        
        # Column selection
        self.column_frame = ttk.LabelFrame(main_frame, text="Select Column")
        self.column_frame.pack(pady=10, padx=10, fill="x")
        
        self.column_listbox = tk.Listbox(self.column_frame, height=5)
        self.column_listbox.pack(pady=5, fill="x")
        
        # Length input
        length_frame = ttk.LabelFrame(main_frame, text="Truncation Length")
        length_frame.pack(pady=10, padx=10, fill="x")
        
        self.length_var = tk.StringVar(value="4")
        length_entry = ttk.Entry(length_frame, textvariable=self.length_var)
        length_entry.pack(pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            main_frame, variable=self.progress_var, maximum=100
        )
        self.progress.pack(pady=10, fill="x")
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.pack(pady=5)
        
        # Process button
        tk.Button(main_frame, text="Process File",
                 command=self.process_file).pack(pady=10)

    def update_progress(self, value: float):
        """Updates the progress bar and processes pending events."""
        self.progress_var.set(value)
        self.status_var.set(f"Processing: {value:.1f}%")
        self.root.update_idletasks()

    def select_file(self):
        """Handles file selection and column loading."""
        self.input_file = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if self.input_file:
            try:
                self.status_var.set("Detecting file encoding...")
                self.root.update_idletasks()
                
                self.encoding = CSVFileHandler.detect_encoding(self.input_file)
                self.columns = CSVFileHandler.read_headers(
                    self.input_file, self.encoding)
                
                # Update column listbox
                self.column_listbox.delete(0, tk.END)
                for i, col in enumerate(self.columns):
                    self.column_listbox.insert(tk.END, f"{i+1}-{col}")
                
                self.status_var.set(f"Loaded file with encoding: {self.encoding}")
                logger.info(f"File loaded: {self.input_file}")
                    
            except Exception as e:
                logger.error(f"Failed to load file: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                self.status_var.set("Error loading file")

    def process_file(self):
        """Handles the file processing workflow."""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first.")
            return
            
        selected_index = self.column_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a column.")
            return
            
        try:
            # Get column index and truncation length
            column_index = selected_index[0]
            length = int(self.length_var.get())
            
            # Construct output filename
            output_file = self.input_file.rsplit('.', 1)[0] + "_truncated.csv"
            
            # Reset progress
            self.progress_var.set(0)
            self.status_var.set("Processing...")
            self.root.update_idletasks()
            
            # Process the file
            success = self.processor.process_file(
                self.input_file, output_file, column_index, length,
                self.encoding, self.update_progress
            )
            
            if success:
                self.status_var.set("Processing complete")
                messagebox.showinfo(
                    "Success",
                    f"Data processed and saved to:\n{output_file}"
                )
            else:
                self.status_var.set("Processing failed")
                messagebox.showerror(
                    "Error",
                    "Failed to process file. Check console for details."
                )
                
        except ValueError:
            logger.error("Invalid truncation length entered")
            messagebox.showerror(
                "Error",
                "Please enter a valid number for truncation length."
            )
        except Exception as e:
            logger.error(f"Error during processing: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error during processing")

    def run(self):
        """Starts the GUI application."""
        logger.info("Starting application")
        self.root.mainloop()


if __name__ == "__main__":
    app = GUI()
    app.run() 