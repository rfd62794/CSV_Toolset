import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from tkinter import filedialog
import chardet
import re
import urllib.parse
from functools import partial

class LeadDataUtility:
    def __init__(self):
        # Initialize the main window
        self.window = tk.Tk()
        self.window.title("Universal Lead Data Utility")
        self.df = None
        
        # --- Predefined Output Columns ---
        self.output_columns = [
            "Business Name", "CRM Industry", "CRM Lead Source", "CRM URL", "Date Sold",
            "First Name", "Last Name", "GMB Review Count", "GMB Review Rating",
            "GMB URL Short", "Is Claimed", "NAICS Code", "Phone Type", "SIC Code",
            "SIC Description", "State", "Website URL", "Zip Code"
        ]
        
        self.setup_gui()
    
    def setup_gui(self):
        # Create GUI elements
        self.import_button = ttk.Button(self.window, text="Import CSV", command=self.import_csv)
        self.import_button.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", mode="indeterminate")
        self.progress_bar.pack(pady=10)
        
        self.file_info = tk.StringVar()
        self.file_info_label = ttk.Label(self.window, textvariable=self.file_info)
        self.file_info_label.pack(pady=10)
        
        self.column_mapping_frame = ttk.Frame(self.window)
        self.column_mapping_frame.pack(pady=10)
        
        self.validate_button = ttk.Button(self.window, text="Validate Data", command=self.validate_data_command)
        self.validate_button.pack(pady=10)
        self.validate_button.config(state="disabled")
        
        self.export_button = ttk.Button(self.window, text="Export CSV", command=self.export_csv_command)
        self.export_button.pack(pady=10)
        self.export_button.config(state="disabled")
    
    def validate_url(self, url):
        """Validate a single URL with basic checks to avoid expensive regex"""
        if pd.isna(url) or str(url).strip() == "":
            return True
        
        url = str(url).strip().lower()
        
        # Quick basic checks before attempting regex
        if not any(url.startswith(prefix) for prefix in ('http://', 'https://', 'www.')):
            return False
            
        try:
            # Use urllib for basic URL parsing - much faster than regex
            result = urllib.parse.urlparse(url if url.startswith(('http://', 'https://')) else 'http://' + url)
            return all([result.netloc, '.' in result.netloc])
        except Exception:
            return False

    def validate_data(self, mapped_columns):
        if self.df is None:
            return ["No data loaded"]
            
        validation_messages = []
        total_columns = len([col for col, map_to in mapped_columns.items() if col and map_to])
        processed_columns = 0
        
        # Update progress bar
        self.progress_bar.config(mode="determinate", maximum=total_columns * 100)
        self.progress_bar.start()
        self.window.update()
        
        try:
            for col_name, map_to in mapped_columns.items():
                if not col_name or not map_to or col_name not in self.df.columns:
                    continue
                    
                try:
                    # Update progress for this column
                    self.progress_bar["value"] = processed_columns * 100
                    self.window.update()
                    
                    if map_to == "Business Name":
                        # Process in chunks to prevent UI freezing
                        chunk_size = 1000
                        empty_rows_list = []
                        invalid_chars_list = []
                        
                        for start_idx in range(0, len(self.df), chunk_size):
                            end_idx = min(start_idx + chunk_size, len(self.df))
                            chunk = self.df[col_name].iloc[start_idx:end_idx]
                            
                            # Check for empty or null values
                            empty_rows = chunk.isnull() | (chunk.astype(str).str.strip() == "")
                            if empty_rows.any():
                                empty_rows_list.extend((empty_rows[empty_rows].index + start_idx).tolist())
                            
                            # Check for invalid characters
                            valid_pattern = r"^[A-Za-z0-9\s\-\&\'\.,]+$"
                            invalid_chars = ~chunk.fillna("").astype(str).str.match(valid_pattern)
                            if invalid_chars.any():
                                invalid_chars_list.extend((invalid_chars[invalid_chars].index + start_idx).tolist())
                            
                            # Update progress within column
                            progress = (end_idx - start_idx) / len(self.df) * 100
                            self.progress_bar["value"] = (processed_columns * 100) + progress
                            self.window.update()
                        
                        if empty_rows_list:
                            validation_messages.append(f"Empty Business Names found in rows: {empty_rows_list}")
                        
                        if invalid_chars_list:
                            invalid_examples = self.df[col_name].iloc[invalid_chars_list[:3]].tolist()
                            validation_messages.append(
                                f"Business Names with invalid characters found in {len(invalid_chars_list)} rows.\n"
                                f"Examples of invalid names: {invalid_examples}\n"
                                f"Only letters, numbers, spaces, hyphens, ampersands, apostrophes, periods, and commas are allowed.\n"
                                f"First few invalid rows: {invalid_chars_list[:10]}"
                            )

                    elif map_to in ("CRM URL", "GMB URL Short", "Website URL"):
                        # Process URLs in chunks with optimized validation
                        chunk_size = 1000
                        invalid_rows_list = []
                        
                        for start_idx in range(0, len(self.df), chunk_size):
                            end_idx = min(start_idx + chunk_size, len(self.df))
                            chunk = self.df[col_name].iloc[start_idx:end_idx]
                            
                            # Validate URLs using the optimized method
                            for idx, url in chunk.items():
                                if not self.validate_url(url):
                                    invalid_rows_list.append(idx)
                            
                            # Update progress within column
                            progress = (end_idx - start_idx) / len(self.df) * 100
                            self.progress_bar["value"] = (processed_columns * 100) + progress
                            self.window.update()
                        
                        if invalid_rows_list:
                            invalid_examples = self.df[col_name].iloc[invalid_rows_list[:3]].tolist()
                            validation_messages.append(
                                f"Invalid URL format found in '{map_to}' ({len(invalid_rows_list)} rows).\n"
                                f"Examples of invalid URLs: {invalid_examples}\n"
                                f"URLs should start with http://, https://, or www. and contain a valid domain.\n"
                                f"First few invalid rows: {invalid_rows_list[:10]}"
                            )

                    elif map_to == "Date Sold":
                        # Process dates in chunks
                        chunk_size = 1000
                        invalid_dates_list = []
                        
                        for start_idx in range(0, len(self.df), chunk_size):
                            end_idx = min(start_idx + chunk_size, len(self.df))
                            chunk = self.df[col_name].iloc[start_idx:end_idx]
                            
                            try:
                                pd.to_datetime(chunk, errors='raise')
                            except Exception as e:
                                invalid_dates_list.extend(range(start_idx, end_idx))
                            
                            # Update progress within column
                            progress = (end_idx - start_idx) / len(self.df) * 100
                            self.progress_bar["value"] = (processed_columns * 100) + progress
                            self.window.update()
                        
                        if invalid_dates_list:
                            validation_messages.append(f"Invalid dates found in rows: {invalid_dates_list[:10]}")

                    elif map_to in ("First Name", "Last Name"):
                        # Process names in chunks
                        chunk_size = 1000
                        invalid_rows_list = []
                        
                        for start_idx in range(0, len(self.df), chunk_size):
                            end_idx = min(start_idx + chunk_size, len(self.df))
                            chunk = self.df[col_name].iloc[start_idx:end_idx]
                            
                            invalid_rows = chunk.isnull() | (chunk.astype(str).str.strip() == "")
                            if invalid_rows.any():
                                invalid_rows_list.extend((invalid_rows[invalid_rows].index + start_idx).tolist())
                            
                            # Update progress within column
                            progress = (end_idx - start_idx) / len(self.df) * 100
                            self.progress_bar["value"] = (processed_columns * 100) + progress
                            self.window.update()
                        
                        if invalid_rows_list:
                            validation_messages.append(f"Invalid '{map_to}' found in rows: {invalid_rows_list[:10]}")

                    elif map_to == "GMB Review Count":
                        numeric_data = pd.to_numeric(self.df[col_name], errors='coerce')
                        invalid_rows = numeric_data.isnull() | (numeric_data < 0)
                        if invalid_rows.any():
                            validation_messages.append(f"Invalid 'GMB Review Count' found in rows: {invalid_rows[invalid_rows].index.tolist()}")

                    elif map_to == "GMB Review Rating":
                        numeric_data = pd.to_numeric(self.df[col_name], errors='coerce')
                        invalid_rows = numeric_data.isnull() | (numeric_data < 0) | (numeric_data > 5)
                        if invalid_rows.any():
                            validation_messages.append(f"Invalid 'GMB Review Rating' found in rows: {invalid_rows[invalid_rows].index.tolist()}")

                    processed_columns += 1
                    self.progress_bar["value"] = processed_columns * 100
                    self.window.update()

                except Exception as e:
                    validation_messages.append(f"Error validating {map_to}: {str(e)}")
                
        except Exception as e:
            validation_messages.append(f"Error validating data: {str(e)}")
        
        # Reset progress bar
        self.progress_bar.stop()
        self.progress_bar["value"] = 0
        self.progress_bar.config(mode="indeterminate")
        self.window.update()
                
        return validation_messages

    def import_csv(self):
        try:
            filepath = filedialog.askopenfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            if not filepath:
                return

            with open(filepath, 'rb') as f:
                result = chardet.detect(f.read())
            encoding = result['encoding']

            self.df = pd.read_csv(filepath, encoding=encoding, low_memory=False)
            self.file_info.set(f"File: {filepath}\nRows: {len(self.df)}\nColumns: {len(self.df.columns)}")
            self.display_columns()
            
            # Enable buttons after successful import
            self.validate_button.config(state="normal")
            self.export_button.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error", f"Error importing file:\n{str(e)}")
            self.file_info.set("")

    def display_columns(self):
        for widget in self.column_mapping_frame.winfo_children():
            widget.destroy()

        for i, col in enumerate(self.output_columns):
            ttk.Label(self.column_mapping_frame, text=col).grid(row=i, column=0, padx=5, pady=5)
            options = [""] + sorted(self.df.columns)
            dropdown = ttk.Combobox(self.column_mapping_frame, values=options, state="readonly")
            dropdown.grid(row=i, column=1, padx=5, pady=5)
            
            # Try to auto-match columns
            for df_col in self.df.columns:
                if df_col.lower().replace(" ", "") == col.lower().replace(" ", ""):
                    dropdown.set(df_col)
                    break

    def get_mapped_columns(self):
        mapped_columns = {}
        for i, col in enumerate(self.output_columns):
            dropdown = self.column_mapping_frame.grid_slaves(row=i, column=1)[0]
            if dropdown.get():  # Only include non-empty mappings
                mapped_columns[dropdown.get()] = col
        return mapped_columns

    def validate_data_command(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please import a CSV file first")
            return
            
        # Disable buttons during validation
        self.validate_button.config(state="disabled")
        self.export_button.config(state="disabled")
        self.import_button.config(state="disabled")
        
        try:
            mapped_columns = self.get_mapped_columns()
            validation_messages = self.validate_data(mapped_columns)
            
            if validation_messages:
                validation_window = tk.Toplevel(self.window)
                validation_window.title("Validation Results")
                
                # Make the window scrollable
                container = ttk.Frame(validation_window)
                canvas = tk.Canvas(container)
                scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
                scrollable_frame = ttk.Frame(canvas)
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Add validation messages
                validation_text = tk.Text(scrollable_frame, wrap=tk.WORD, width=80, height=20)
                validation_text.pack(expand=True, fill="both", padx=10, pady=10)
                validation_text.insert("end", "\n".join(validation_messages))
                validation_text.config(state="disabled")
                
                # Pack scrollbar components
                container.pack(expand=True, fill="both")
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
            else:
                messagebox.showinfo("Success", "Data validation successful!")
        
        finally:
            # Re-enable buttons
            self.validate_button.config(state="normal")
            self.export_button.config(state="normal")
            self.import_button.config(state="normal")

    def export_csv_command(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please import a CSV file first")
            return
            
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            if not filepath:
                return

            mapped_columns = self.get_mapped_columns()
            selected_columns = {col: map_to for col, map_to in mapped_columns.items() if map_to}
            
            if not selected_columns:
                messagebox.showwarning("Warning", "No columns mapped for export")
                return
                
            df_export = self.df[list(selected_columns.keys())].rename(columns=selected_columns)
            
            # Add missing columns with None values
            for col in self.output_columns:
                if col not in df_export.columns:
                    df_export[col] = None
                    
            # Reorder columns according to output_columns
            df_export = df_export[self.output_columns]
            df_export.to_csv(filepath, index=False)
            messagebox.showinfo("Success", f"File exported successfully to:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Error", f"Error exporting file:\n{str(e)}")

if __name__ == "__main__":
    app = LeadDataUtility()
    app.window.mainloop()