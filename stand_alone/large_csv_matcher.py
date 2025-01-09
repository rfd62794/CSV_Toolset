#!/usr/bin/env python3
"""Large CSV Data Matcher - Optimized for matching and appending data between large CSV files."""
import csv
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Generator
import chardet
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import mmap
import io
import os
from datetime import datetime

class ChunkProcessor:
    """Handles processing of CSV chunks efficiently."""
    
    def __init__(self, chunk_size: int = 1024 * 1024):  # 1MB chunks
        self.chunk_size = chunk_size
        
    def process_source_chunk(self, chunk: str, col_idx: int, data_idx: int) -> Dict[str, str]:
        """Process a chunk of source data."""
        result = {}
        for row in csv.reader(io.StringIO(chunk)):
            if len(row) > max(col_idx, data_idx):
                key = row[col_idx].strip()
                if key:
                    result[key] = row[data_idx]
        return result

    @staticmethod
    def merge_chunk_results(results: List[Dict[str, str]]) -> Dict[str, str]:
        """Merge chunk processing results."""
        merged = {}
        for result in results:
            merged.update(result)
        return merged

class LargeCSVDataMatcher:
    """GUI application for matching and appending data between large CSV files."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Large CSV Data Matcher")
        self.root.geometry("800x700")
        
        # File paths and data
        self.source_path: Optional[Path] = None
        self.target_path: Optional[Path] = None
        self.source_headers: List[str] = []
        self.target_headers: List[str] = []
        self.source_encoding: str = 'utf-8'
        self.target_encoding: str = 'utf-8'
        
        # Performance settings
        self.chunk_size = 1024 * 1024  # 1MB chunks
        self.max_workers = max(1, mp.cpu_count() - 1)  # Leave one CPU free
        self.processor = ChunkProcessor(self.chunk_size)
        
        self._create_widgets()
        self._center_window()
        
    def _detect_encoding(self, file_path: Path, sample_size: int = 1024 * 1024) -> str:
        """Detect file encoding using chardet with limited sample size."""
        # Try common encodings first
        common_encodings = ['utf-8', 'utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']
        for encoding in common_encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read(sample_size)
                    return encoding
            except UnicodeDecodeError:
                continue

        # If common encodings fail, use chardet
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(sample_size)
                result = chardet.detect(raw_data)
                if result['encoding'] and result['confidence'] > 0.7:
                    return result['encoding']
        except Exception:
            pass

        # Default to utf-8 with error handling
        return 'utf-8'
            
    def _read_headers(self, file_path: Path) -> Tuple[List[str], str]:
        """Read CSV headers efficiently."""
        encoding = self._detect_encoding(file_path)
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                # Read only first line for headers
                headers = next(csv.reader(f))
                return headers, encoding
        except Exception:
            # Fallback encodings
            for enc in ['utf-8', 'utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=enc, newline='') as f:
                        headers = next(csv.reader(f))
                        return headers, enc
                except Exception:
                    continue
            raise ValueError("Could not read file with any supported encoding")
            
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
        
        # Performance settings
        perf_frame = ttk.LabelFrame(main_frame, text="Performance Settings", padding="5")
        perf_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        
        ttk.Label(perf_frame, text="Chunk Size (MB):").grid(row=0, column=0, padx=5)
        self.chunk_size_var = tk.StringVar(value="1")
        ttk.Entry(perf_frame, textvariable=self.chunk_size_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(perf_frame, text="Worker Processes:").grid(row=0, column=2, padx=5)
        self.workers_var = tk.StringVar(value=str(self.max_workers))
        ttk.Entry(perf_frame, textvariable=self.workers_var, width=10).grid(row=0, column=3, padx=5)
        
        # Output options
        output_frame = ttk.LabelFrame(main_frame, text="Output Options", padding="5")
        output_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=60).grid(row=0, column=0, padx=5)
        ttk.Button(output_frame, text="Browse", command=self._select_output).grid(row=0, column=1, padx=5)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="5")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Process button
        ttk.Button(main_frame, text="Match and Append Data", command=self._process_files).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=6, column=0, columnspan=2)
        
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
            headers, encoding = self._read_headers(self.source_path)
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
            headers, encoding = self._read_headers(self.target_path)
            self.target_headers = headers
            self.target_encoding = encoding
            self.target_col_combo['values'] = self.target_headers
            if self.target_headers:
                self.target_col_combo.set(self.target_headers[0])
            self.status_var.set(f"Target file loaded (Encoding: {encoding})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load target file: {str(e)}")
            
    def _get_file_chunks(self, file_path: Path, encoding: str) -> Generator[str, None, None]:
        """Generate chunks of file content efficiently."""
        with open(file_path, 'r', encoding=encoding, errors='replace', newline='') as f:
            # Skip header
            next(f)
            
            chunk = []
            chunk_size = 0
            for line in f:
                chunk.append(line)
                chunk_size += len(line.encode(encoding))  # Use encoded size
                if chunk_size >= self.chunk_size:
                    yield ''.join(chunk)
                    chunk = []
                    chunk_size = 0
            
            if chunk:
                yield ''.join(chunk)
                
    def _process_source_file(self) -> Dict[str, str]:
        """Process source file in chunks using multiprocessing."""
        source_col_idx = self.source_headers.index(self.source_col_var.get())
        source_data_idx = self.source_headers.index(self.source_data_var.get())
        
        chunks = list(self._get_file_chunks(self.source_path, self.source_encoding))
        total_chunks = len(chunks)
        processed_chunks = 0
        
        results = []
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(
                    self.processor.process_source_chunk,
                    chunk,
                    source_col_idx,
                    source_data_idx
                )
                for chunk in chunks
            ]
            
            for future in futures:
                results.append(future.result())
                processed_chunks += 1
                self.progress_var.set((processed_chunks / total_chunks) * 50)
                self.root.update_idletasks()
                
        return self.processor.merge_chunk_results(results)
        
    def _process_target_file(self, source_data: Dict[str, str]):
        """Process target file and create output."""
        target_col_idx = self.target_headers.index(self.target_col_var.get())
        new_header = self.target_headers + [f"Matched_{self.source_data_var.get()}"]
        
        total_size = os.path.getsize(self.target_path)
        processed_size = 0
        
        with open(self.target_path, 'r', encoding=self.target_encoding, errors='replace', newline='') as fin, \
             open(self.output_path_var.get(), 'w', encoding='utf-8', errors='replace', newline='') as fout:
            
            reader = csv.reader(fin)
            writer = csv.writer(fout)
            
            # Write header
            next(reader)
            writer.writerow(new_header)
            
            # Process rows
            for row in reader:
                if len(row) > target_col_idx:
                    key = row[target_col_idx].strip()
                    matched_data = source_data.get(key, "")
                    writer.writerow(row + [matched_data])
                else:
                    writer.writerow(row + [""])
                    
                processed_size += sum(len(field.encode(self.target_encoding)) + 1 for field in row)
                self.progress_var.set(50 + (processed_size / total_size) * 50)
                self.root.update_idletasks()
                
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
            
        try:
            chunk_size = float(self.chunk_size_var.get())
            if chunk_size <= 0:
                raise ValueError
            self.chunk_size = int(chunk_size * 1024 * 1024)
        except ValueError:
            messagebox.showerror("Error", "Invalid chunk size")
            return False
            
        try:
            workers = int(self.workers_var.get())
            if workers <= 0:
                raise ValueError
            self.max_workers = min(workers, mp.cpu_count())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of workers")
            return False
            
        return True
        
    def _process_files(self):
        """Match and append data between files."""
        if not self._validate_inputs():
            return
            
        try:
            self.status_var.set("Processing source file...")
            self.progress_var.set(0)
            
            # Process source file
            start_time = datetime.now()
            source_data = self._process_source_file()
            
            self.status_var.set("Processing target file...")
            
            # Process target file
            self._process_target_file(source_data)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.progress_var.set(100)
            self.status_var.set(f"Processing complete in {duration:.1f} seconds")
            messagebox.showinfo("Success", "Data matching and appending completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process files: {str(e)}")
            self.status_var.set("Error occurred")
            
    def run(self):
        """Start the application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    if sys.platform == 'win32':
        # Set up multiprocessing for Windows
        mp.freeze_support()
    
    app = LargeCSVDataMatcher()
    app.run()

if __name__ == "__main__":
    main() 