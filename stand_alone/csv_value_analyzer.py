#!/usr/bin/env python3
"""CSV Value Analyzer - Analyze unique values and their frequencies in CSV columns."""
import csv
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter
import chardet

class CSVValueAnalyzer:
    """GUI application for analyzing unique values in CSV columns."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CSV Value Analyzer")
        self.root.geometry("800x600")
        
        # File path and data
        self.file_path: Optional[Path] = None
        self.headers: List[str] = []
        self.file_encoding: str = 'utf-8'
        
        # Results
        self.unique_values: Dict[str, int] = {}
        self.value_counts: Dict[str, int] = {}
        
        self._create_widgets()
        self._center_window()
        
    def _detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding using chardet."""
        # Try common encodings first
        common_encodings = ['utf-8', 'utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']
        for encoding in common_encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read(1024)
                    return encoding
            except UnicodeDecodeError:
                continue

        # If common encodings fail, use chardet
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(1024)
                result = chardet.detect(raw_data)
                if result['encoding'] and result['confidence'] > 0.7:
                    return result['encoding']
        except Exception:
            pass

        # Default to utf-8 with error handling
        return 'utf-8'
            
    def _create_widgets(self):
        """Create GUI elements."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="CSV File Selection", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=60).grid(row=0, column=0, padx=5)
        ttk.Button(file_frame, text="Browse", command=self._select_file).grid(row=0, column=1, padx=5)
        
        # Column selection
        col_frame = ttk.Frame(file_frame)
        col_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Label(col_frame, text="Select Column:").grid(row=0, column=0, padx=5)
        self.col_var = tk.StringVar()
        self.col_combo = ttk.Combobox(col_frame, textvariable=self.col_var, state="readonly", width=40)
        self.col_combo.grid(row=0, column=1, padx=5)
        
        # Analysis button
        ttk.Button(main_frame, text="Analyze Values", command=self._analyze_values).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Results
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="5")
        results_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=5)
        
        # Summary
        summary_frame = ttk.Frame(results_frame)
        summary_frame.grid(row=0, column=0, sticky="ew", pady=5)
        
        ttk.Label(summary_frame, text="Total Unique Values:").grid(row=0, column=0, padx=5)
        self.unique_count_var = tk.StringVar(value="0")
        ttk.Label(summary_frame, textvariable=self.unique_count_var).grid(row=0, column=1, padx=5)
        
        # Value list with scrollbar
        self.results_text = tk.Text(results_frame, height=20, width=80)
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Export button
        ttk.Button(main_frame, text="Export Results", command=self._export_results).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        results_frame.columnconfigure(0, weight=1)
        
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def _select_file(self):
        """Select CSV file."""
        path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.file_path = Path(path)
            self.file_path_var.set(str(self.file_path))
            self._load_headers()
            
    def _load_headers(self):
        """Load headers from CSV file."""
        try:
            self.file_encoding = self._detect_encoding(self.file_path)
            with open(self.file_path, 'r', encoding=self.file_encoding, errors='replace', newline='') as f:
                reader = csv.reader(f)
                self.headers = next(reader)
                self.col_combo['values'] = self.headers
                if self.headers:
                    self.col_combo.set(self.headers[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            
    def _analyze_values(self):
        """Analyze unique values in selected column."""
        if not self.file_path or not self.col_var.get():
            messagebox.showerror("Error", "Please select a file and column")
            return
            
        try:
            # Reset results
            self.unique_values = {}
            self.value_counts = {}
            self.results_text.delete('1.0', tk.END)
            
            # Get column index
            col_idx = self.headers.index(self.col_var.get())
            
            # Process file
            counter = Counter()
            with open(self.file_path, 'r', encoding=self.file_encoding, errors='replace', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) > col_idx:
                        value = row[col_idx].strip()
                        if value:  # Skip empty values
                            counter[value] += 1
            
            # Update results
            self.value_counts = dict(counter)
            self.unique_count_var.set(str(len(counter)))
            
            # Display results
            self.results_text.insert('1.0', "Value Frequencies:\n\n")
            
            # Sort by frequency (highest to lowest)
            sorted_items = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
            
            # Calculate max lengths for formatting
            max_value_len = max(len(str(value)) for value, _ in sorted_items) if sorted_items else 0
            max_count_len = max(len(str(count)) for _, count in sorted_items) if sorted_items else 0
            
            # Display with aligned columns
            for value, count in sorted_items:
                line = f"{value:<{max_value_len}} : {count:>{max_count_len}} instances\n"
                self.results_text.insert(tk.END, line)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze values: {str(e)}")
            
    def _export_results(self):
        """Export analysis results to CSV."""
        if not self.value_counts:
            messagebox.showerror("Error", "No results to export")
            return
            
        try:
            output_path = filedialog.asksaveasfilename(
                title="Save Analysis Results",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Value", "Count"])
                    
                    # Sort by frequency (highest to lowest)
                    sorted_items = sorted(self.value_counts.items(), key=lambda x: (-x[1], x[0]))
                    writer.writerows(sorted_items)
                    
                messagebox.showinfo("Success", "Results exported successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {str(e)}")
            
    def run(self):
        """Start the application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    app = CSVValueAnalyzer()
    app.run()

if __name__ == "__main__":
    main() 