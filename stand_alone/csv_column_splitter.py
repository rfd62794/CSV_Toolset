"""
A standalone script for splitting CSV files based on unique values in a selected column.
Creates separate files for each unique value, preserving headers.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import chardet
import logging
import os
from typing import Optional, Dict, Set
from pathlib import Path
from collections import defaultdict


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


class CSVSplitter:
    """Handles the CSV splitting logic."""
    
    def __init__(self):
        self.file_handler = CSVFileHandler()
        
    def get_unique_values(self, input_file: str, column_index: int,
                         encoding: str) -> Set[str]:
        """Returns set of unique values in the specified column."""
        unique_values = set()
        with open(input_file, 'r', newline='', encoding=encoding) as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                try:
                    value = row[column_index].strip()
                    if value:  # Only include non-empty values
                        unique_values.add(value)
                except IndexError:
                    logger.warning(f"Row has fewer columns than expected: {row}")
        return unique_values

    def split_file(self, input_file: str, column_index: int, encoding: str,
                   progress_callback: Optional[callable] = None) -> Dict[str, int]:
        """
        Splits CSV file based on unique values in specified column.
        Returns dictionary of value: row_count pairs.
        """
        try:
            logger.info(f"Starting file splitting: {input_file}")
            
            # Create output directory
            input_path = Path(input_file)
            output_dir = input_path.parent / "Split"
            output_dir.mkdir(exist_ok=True)
            
            # Read headers
            headers = self.file_handler.read_headers(input_file, encoding)
            total_rows = self.file_handler.count_rows(input_file, encoding)
            
            # Initialize row counters and file handlers
            value_counts = defaultdict(int)
            output_files = {}
            output_writers = {}
            processed_rows = 0
            
            with open(input_file, 'r', newline='', encoding=encoding) as infile:
                reader = csv.reader(infile)
                next(reader)  # Skip header since we already have it
                
                # Process each row
                for row in reader:
                    try:
                        value = row[column_index].strip()
                        if not value:
                            continue
                            
                        # Create new file for this value if it doesn't exist
                        if value not in output_files:
                            safe_value = "".join(c for c in value if c.isalnum())
                            output_name = f"{input_path.stem}_matching_{safe_value}{input_path.suffix}"
                            output_path = output_dir / output_name
                            
                            output_files[value] = open(output_path, 'w', newline='', encoding=encoding)
                            output_writers[value] = csv.writer(output_files[value])
                            output_writers[value].writerow(headers)
                            logger.info(f"Created new file for value: {value}")
                        
                        # Write row to appropriate file
                        output_writers[value].writerow(row)
                        value_counts[value] += 1
                        
                    except IndexError:
                        logger.warning(f"Skipping row with insufficient columns: {row}")
                    
                    processed_rows += 1
                    if progress_callback and processed_rows % 100 == 0:
                        progress = (processed_rows / total_rows) * 100
                        progress_callback(progress)
                        logger.debug(f"Progress: {progress:.1f}%")
            
            # Close all output files
            for f in output_files.values():
                f.close()
            
            logger.info(f"Split complete. Created {len(value_counts)} files")
            return dict(value_counts)
            
        except Exception as e:
            logger.error(f"Error splitting file: {str(e)}", exc_info=True)
            raise


class GUI:
    """Handles the graphical user interface."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CSV Column Splitter")
        self.splitter = CSVSplitter()
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
        
        # Results text
        self.results_frame = ttk.LabelFrame(main_frame, text="Results")
        self.results_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.results_text = tk.Text(self.results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(pady=5, fill="both", expand=True)
        
        # Process button
        tk.Button(main_frame, text="Split File",
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
        """Handles the file splitting workflow."""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first.")
            return
            
        selected_index = self.column_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a column.")
            return
            
        try:
            # Get column index
            column_index = selected_index[0]
            
            # Reset progress and clear results
            self.progress_var.set(0)
            self.status_var.set("Processing...")
            self.results_text.delete(1.0, tk.END)
            self.root.update_idletasks()
            
            # Split the file
            value_counts = self.splitter.split_file(
                self.input_file, column_index, self.encoding, self.update_progress
            )
            
            # Display results
            self.status_var.set("Split complete")
            results = ["Split Results:"]
            for value, count in sorted(value_counts.items()):
                results.append(f"• Value '{value}': {count} rows")
            
            self.results_text.insert(tk.END, "\n".join(results))
            
            # Show success message
            output_dir = Path(self.input_file).parent / "Split"
            messagebox.showinfo(
                "Success",
                f"Files have been created in:\n{output_dir}"
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