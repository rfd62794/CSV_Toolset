import csv
import os
import chardet
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
import time

def csv_stats(filename):
    """
    Gathers and prints statistics about a CSV file, including advanced stats,
    with progress updates in the console. Prints all stats after processing.

    Args:
      filename: The path to the CSV file.
    """
    try:
        # File size
        file_size = os.path.getsize(filename)

        # Encoding detection
        with open(filename, 'rb') as f:
            rawdata = f.read()
            result = chardet.detect(rawdata)
            encoding = result['encoding']

        # Column names, number of rows, data types, unique values, null counts
        with open(filename, 'r', encoding=encoding) as f:
            reader = csv.reader(f)
            column_names = next(reader)  # Get the first row as column names

            num_rows = 0
            data_types = defaultdict(set)
            unique_values = defaultdict(set)
            null_counts = defaultdict(int)

            start_time = time.time()  # Start time for progress tracking

            for row in reader:
                num_rows += 1
                for i, value in enumerate(row):
                    # Data type sniffing
                    try:
                        int(value)
                        data_types[column_names[i]].add(int)
                    except ValueError:
                        try:
                            float(value)
                            data_types[column_names[i]].add(float)
                        except ValueError:
                            data_types[column_names[i]].add(str)

                    # Unique values and null count
                    unique_values[column_names[i]].add(value)
                    if value == '' or value is None:
                        null_counts[column_names[i]] += 1

                # Progress update
                if num_rows % 10000 == 0:  # Update every 10,000 rows
                    elapsed_time = time.time() - start_time
                    print(f"Processed {num_rows} rows ({elapsed_time:.2f} seconds)")

        # Print all stats after processing
        print(f"\nFile size: {file_size} bytes")
        print(f"Detected encoding: {encoding}")
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