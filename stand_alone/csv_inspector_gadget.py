import csv
import os
import chardet
from collections import defaultdict, Counter
import tkinter as tk
from tkinter import filedialog
import time
import pandas as pd

def csv_stats(filename):
    """
    Gathers and prints comprehensive statistics about a CSV file, including 
    advanced stats, with progress updates.

    Args:
      filename (str): The path to the CSV file.
    """
    try:
        # File size
        file_size = os.path.getsize(filename)

        # Encoding detection
        with open(filename, 'rb') as f:
            rawdata = f.read()
            result = chardet.detect(rawdata)
            encoding = result['encoding']

        # ---  Data Analysis ---
        with open(filename, 'r', encoding=encoding) as f:
            reader = csv.reader(f)
            column_names = next(reader)

            num_rows = 0
            data_types = defaultdict(set)
            unique_values = defaultdict(set)
            null_counts = defaultdict(int)
            value_counts = defaultdict(Counter)  # For value frequency analysis
            numeric_stats = defaultdict(dict)  # For numeric columns

            start_time = time.time()

            for row in reader:
                num_rows += 1
                for i, value in enumerate(row):
                    # Data type sniffing
                    try:
                        int(value)
                        data_types[column_names[i]].add(int)
                        numeric_stats[column_names[i]].setdefault('sum', 0)
                        numeric_stats[column_names[i]]['sum'] += int(value)
                    except ValueError:
                        try:
                            float(value)
                            data_types[column_names[i]].add(float)
                            numeric_stats[column_names[i]].setdefault('sum', 0.0)
                            numeric_stats[column_names[i]]['sum'] += float(value)
                        except ValueError:
                            data_types[column_names[i]].add(str)

                    # Unique values, null count, and value counts
                    unique_values[column_names[i]].add(value)
                    if value == '' or value is None:
                        null_counts[column_names[i]] += 1
                    value_counts[column_names[i]][value] += 1

                # Progress update
                if num_rows % 10000 == 0:
                    elapsed_time = time.time() - start_time
                    print(f"Processed {num_rows} rows ({elapsed_time:.2f} seconds)")

        # --- Print Stats ---
        print("\n--- File Stats ---")
        print(f"File size: {file_size} bytes")
        print(f"Detected encoding: {encoding}")

        print("\n--- Data Stats ---")
        print(f"Column names: {column_names}")
        print(f"Number of rows: {num_rows}")

        print("\nData types:")
        for col, types in data_types.items():
            print(f"  {col}: {', '.join([t.__name__ for t in types])}")

        print("\nUnique values:")
        for col, values in unique_values.items():
            print(f"  {col}: {len(values)}")

        print("\nNull value counts:")
        for col, count in null_counts.items():
            print(f"  {col}: {count}")

        # --- Advanced Stats ---
        print("\n--- Advanced Stats ---")

        print("\nMost frequent values:")
        for col, counts in value_counts.items():
            top_5_values = counts.most_common(5)
            print(f"  {col}: {top_5_values}")

        print("\nNumeric column statistics:")
        for col, stats in numeric_stats.items():
            stats['mean'] = stats['sum'] / num_rows
            print(f"  {col}: {stats}")

        # --- Pandas Analysis (for additional insights) ---
        print("\n--- Pandas Analysis ---")
        try:
            df = pd.read_csv(filename, encoding=encoding)
            print(df.describe().to_markdown(numalign="left", stralign="left"))
        except Exception as e:
            print(f"Error during Pandas analysis: {e}")

        # Prompt user after printing stats
        input("Press Enter to continue...")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def browse_file():
    """Opens a file dialog to select a CSV file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        csv_stats(file_path)
    else:
        print("No file selected.")

if __name__ == "__main__":
    browse_file()