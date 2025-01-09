#!/usr/bin/env python3
"""CSV Data Matcher - Match and append data between CSV files based on a common column."""
import csv
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import chardet

class CSVDataMatcher:
    """GUI application for matching and appending data between CSV files."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CSV Data Matcher")
        self.root.geometry("800x600")
        
        # File paths and data
        self.source_path: Optional[Path] = None
        self.target_path: Optional[Path] = None
        self.source_headers: List[str] = []
        self.target_headers: List[str] = []
        self.source_encoding: str = 'utf-8'
        self.target_encoding: str = 'utf-8'
        
        self._create_widgets()
        self._center_window()
        
    def _detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding using chardet."""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            # Default to utf-8 if detection fails
            return encoding if encoding else 'utf-8'
            
    def _read_csv_with_encoding(self, file_path: Path) -> Tuple[List[str], str]:
        """Read CSV file with automatic encoding detection."""
        encoding = self._detect_encoding(file_path)
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                reader = csv.reader(f)
                headers = next(reader)
                return headers, encoding
        except UnicodeDecodeError:
            # Fallback encodings if detection fails
            fallback_encodings = ['utf-8', 'utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']
            for enc in fallback_encodings:
                try:
                    with open(file_path, 'r', encoding=enc, newline='') as f:
                        reader = csv.reader(f)
                        headers = next(reader)
                        return headers, enc
                except UnicodeDecodeError:
                    continue
            raise ValueError(f"Could not read file with any supported encoding")
            
    def _create_widgets(self):
        """Create GUI elements."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Source file selection
        source_frame = ttk.LabelFrame(main_frame, text="Source File (Data to Match From)", padding="5")
        source_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.source_path_var = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.source_path_var, width=60).grid(row=0, column=0, padx=5)
        ttk.Button(source_frame, text="Browse", command=self._select_source).grid(row=0, column=1, padx=5)
        
        # Source column selection
        source_cols_frame = ttk.Frame(source_frame)
        source_cols_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Label(source_cols_frame, text="Match Column:").grid(row=0, column=0, padx=5)
        self.source_col_var = tk.StringVar()
        self.source_col_combo = ttk.Combobox(source_cols_frame, textvariable=self.source_col_var, state="readonly")
        self.source_col_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(source_cols_frame, text="Data Column:").grid(row=0, column=2, padx=5)
        self.source_data_var = tk.StringVar()
        self.source_data_combo = ttk.Combobox(source_cols_frame, textvariable=self.source_data_var, state="readonly")
        self.source_data_combo.grid(row=0, column=3, padx=5)
        
        # Target file selection
        target_frame = ttk.LabelFrame(main_frame, text="Target File (File to Update)", padding="5")
        target_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.target_path_var = tk.StringVar()
        ttk.Entry(target_frame, textvariable=self.target_path_var, width=60).grid(row=0, column=0, padx=5)
        ttk.Button(target_frame, text="Browse", command=self._select_target).grid(row=0, column=1, padx=5)
        
        # Target column selection
        target_cols_frame = ttk.Frame(target_frame)
        target_cols_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Label(target_cols_frame, text="Match Column:").grid(row=0, column=0, padx=5)
        self.target_col_var = tk.StringVar()
        self.target_col_combo = ttk.Combobox(target_cols_frame, textvariable=self.target_col_var, state="readonly")
        self.target_col_combo.grid(row=0, column=1, padx=5)
        
        # Output options
        output_frame = ttk.LabelFrame(main_frame, text="Output Options", padding="5")
        output_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=60).grid(row=0, column=0, padx=5)
        ttk.Button(output_frame, text="Browse", command=self._select_output).grid(row=0, column=1, padx=5)
        
        # Process button
        ttk.Button(main_frame, text="Match and Append Data", command=self._process_files).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=2)
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def _select_source(self):
        """Select source CSV file."""
        path = filedialog.askopenfilename(
            title="Select Source CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.source_path = Path(path)
            self.source_path_var.set(str(self.source_path))
            self._load_source_headers()
            
    def _select_target(self):
        """Select target CSV file."""
        path = filedialog.askopenfilename(
            title="Select Target CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.target_path = Path(path)
            self.target_path_var.set(str(self.target_path))
            self._load_target_headers()
            
    def _select_output(self):
        """Select output file location."""
        path = filedialog.asksaveasfilename(
            title="Save Output CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.output_path_var.set(path)
            
    def _load_source_headers(self):
        """Load headers from source CSV file."""
        try:
            headers, encoding = self._read_csv_with_encoding(self.source_path)
            self.source_headers = headers
            self.source_encoding = encoding
            self.source_col_combo['values'] = self.source_headers
            self.source_data_combo['values'] = self.source_headers
            if self.source_headers:
                self.source_col_combo.set(self.source_headers[0])
                self.source_data_combo.set(self.source_headers[-1])
            self.status_var.set(f"Source file loaded (Encoding: {encoding})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load source file: {str(e)}")
            
    def _load_target_headers(self):
        """Load headers from target CSV file."""
        try:
            headers, encoding = self._read_csv_with_encoding(self.target_path)
            self.target_headers = headers
            self.target_encoding = encoding
            self.target_col_combo['values'] = self.target_headers
            if self.target_headers:
                self.target_col_combo.set(self.target_headers[0])
            self.status_var.set(f"Target file loaded (Encoding: {encoding})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load target file: {str(e)}")
            
    def _process_files(self):
        """Match and append data between files."""
        if not self._validate_inputs():
            return
            
        try:
            # Load source data into dictionary
            source_data = self._load_source_data()
            
            # Process target file and create output
            self._create_output_file(source_data)
            
            messagebox.showinfo("Success", "Data matching and appending completed successfully!")
            self.status_var.set("Processing complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process files: {str(e)}")
            self.status_var.set("Error occurred")
            
    def _validate_inputs(self) -> bool:
        """Validate user inputs before processing."""
        if not self.source_path or not self.target_path:
            messagebox.showerror("Error", "Please select both source and target files")
            return False
            
        if not self.output_path_var.get():
            messagebox.showerror("Error", "Please select output file location")
            return False
            
        if not self.source_col_var.get() or not self.target_col_var.get():
            messagebox.showerror("Error", "Please select match columns for both files")
            return False
            
        if not self.source_data_var.get():
            messagebox.showerror("Error", "Please select data column from source file")
            return False
            
        return True
        
    def _load_source_data(self) -> Dict[str, str]:
        """Load source data into dictionary for matching."""
        source_data = {}
        source_col_idx = self.source_headers.index(self.source_col_var.get())
        source_data_idx = self.source_headers.index(self.source_data_var.get())
        
        with open(self.source_path, 'r', encoding=self.source_encoding, newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) > max(source_col_idx, source_data_idx):
                    key = row[source_col_idx].strip()
                    if key:  # Only store non-empty keys
                        source_data[key] = row[source_data_idx]
                        
        return source_data
        
    def _create_output_file(self, source_data: Dict[str, str]):
        """Create output file with matched and appended data."""
        target_col_idx = self.target_headers.index(self.target_col_var.get())
        new_header = self.target_headers + [f"Matched_{self.source_data_var.get()}"]
        
        with open(self.target_path, 'r', encoding=self.target_encoding, newline='') as fin, \
             open(self.output_path_var.get(), 'w', encoding='utf-8', newline='') as fout:
            reader = csv.reader(fin)
            writer = csv.writer(fout)
            
            next(reader)  # Skip header
            writer.writerow(new_header)
            
            for row in reader:
                if len(row) > target_col_idx:
                    key = row[target_col_idx].strip()
                    matched_data = source_data.get(key, "")
                    writer.writerow(row + [matched_data])
                else:
                    writer.writerow(row + [""])
                    
    def run(self):
        """Start the application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    app = CSVDataMatcher()
    app.run()

if __name__ == "__main__":
    main() 