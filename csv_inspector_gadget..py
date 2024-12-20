import csv
import os
import chardet
from collections import defaultdict, Counter
import re
import time
import tkinter as tk
from tkinter import filedialog
import statistics

def get_file_info(filename):
    """
    Gets basic information about the CSV file, including size and encoding.

    Args:
      filename (str): The path to the CSV file.

    Returns:
      tuple: A tuple containing the file size and detected encoding.
    """
    file_size = os.path.getsize(filename)
    with open(filename, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
    return file_size, encoding

def detect_delimiter(filename, encoding):
    with open(filename, 'r', encoding=encoding) as f:
        sample = f.read(1024)
        sniffer = csv.Sniffer()
        return sniffer.sniff(sample).delimiter

def analyze_data(filename, encoding):
    """
    Analyzes the data in the CSV file, including data types, unique values,
    null counts, value counts, and numeric statistics.

    Args:
      filename (str): The path to the CSV file.
      encoding (str): The encoding of the CSV file.

    Returns:
      tuple: A tuple containing dictionaries for data types, unique values, 
             null counts, value counts, numeric stats, and number of rows.
    """
    delimiter = detect_delimiter(filename, encoding)
    with open(filename, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            column_names = next(reader)
        except StopIteration:
            print("Error: The CSV file is empty.")
            return {}, {}, {}, {}, {}, 0

        num_rows = 0
        data_types = defaultdict(set)
        unique_values = defaultdict(set)
        null_counts = defaultdict(int)
        value_counts = defaultdict(Counter)
        numeric_stats = defaultdict(dict)

        for row in reader:
            num_rows += 1
            for i, value in enumerate(row):
                data_types[column_names[i]].add(detect_data_type(value))

                unique_values[column_names[i]].add(value)
                if value == '' or value is None:
                    null_counts[column_names[i]] += 1
                value_counts[column_names[i]][value] += 1

                update_numeric_stats(numeric_stats, column_names[i], value)

    return data_types, unique_values, null_counts, value_counts, numeric_stats, num_rows


def detect_data_type(value):
    """
    Detects the data type of a value using pattern matching.

    Args:
      value (str): The value to analyze.

    Returns:
      str or type: The detected data type.
    """
    try:
        int(value)
        return int
    except ValueError:
        try:
            float(value)
            return float
        except ValueError:
            if re.match(r'\d{4}-\d{2}-\d{2}', value):  # Date (YYYY-MM-DD)
                return 'date'
            elif re.match(r'\d{2}/\d{2}/\d{4}', value):  # Date (MM/DD/YYYY)
                return 'date'
            elif re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', value):  # Email
                return 'email'
            elif re.match(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)', value):  # URL
                return 'url'
            elif re.match(r'(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', value):  # Phone number (US)
                return 'phone'
            elif re.match(r'^(?:\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', value):  # Phone number (International)
                return 'phone'
            elif re.match(r'^(?:[A-Z]{1,2}\d{1,2}[A-Z]?)\s*\d[A-Z]{2}$', value, re.IGNORECASE):  # UK Postcode
                return 'postcode'
            elif value.lower() in ['true', 'false']:  # Boolean
                return 'boolean'
            elif re.match(r'\d{2}:\d{2}(:\d{2})?', value):  # Time (HH:MM or HH:MM:SS)
                return 'time'
            else:
                return str


def update_numeric_stats(numeric_stats, column_name, value):
    """
    Updates the numeric statistics for a column.

    Args:
      numeric_stats (dict): A dictionary to store numeric stats.
      column_name (str): The name of the column.
      value (str): The value to analyze.
    """
    try:
        num_value = int(value)
    except ValueError:
        try:
            num_value = float(value)
        except ValueError:
            return  # Not a numeric value

    numeric_stats[column_name].setdefault('count', 0)
    numeric_stats[column_name]['count'] += 1
    numeric_stats[column_name].setdefault('min', num_value)
    numeric_stats[column_name]['min'] = min(numeric_stats[column_name]['min'], num_value)
    numeric_stats[column_name].setdefault('max', num_value)
    numeric_stats[column_name]['max'] = max(numeric_stats[column_name]['max'], num_value)
    numeric_stats[column_name].setdefault('values', []).append(num_value)


def print_stats(file_size, encoding, column_names, num_rows, 
                data_types, unique_values, null_counts, value_counts, numeric_stats):
    """
    Prints the gathered statistics to the console.

    Args:
      file_size (int): The size of the file in bytes.
      encoding (str): The encoding of the file.
      column_names (list): The names of the columns.
      num_rows (int): The number of rows in the data.
      data_types (dict): The detected data types for each column.
      unique_values (dict): The unique values for each column.
      null_counts (dict): The null value counts for each column.
      value_counts (dict): The value counts for each column.
      numeric_stats (dict): The numeric statistics for each column.
    """
    print("\n--- File Stats ---")
    print(f"File size: {file_size} bytes")
    print(f"Detected encoding: {encoding}")

    print("\n--- Data Stats ---")
    print(f"Column names: {column_names}")
    print(f"Number of rows: {num_rows}")

    print("\nData types (with pattern matching):")
    for col, types in data_types.items():
        type_names = [t.__name__ if isinstance(t, type) else t for t in types]
        print(f"  {col}: {', '.join(type_names)}")

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
        if 'values' in stats:
            stats['median'] = statistics.median(stats['values'])
            stats['std_dev'] = statistics.stdev(stats['values']) if len(stats['values']) > 1 else 0
        print(f"  {col}: {stats}")

    # --- Data Profiling ---
    print("\n--- Data Profiling ---")
    
    print("\nData Completeness:")
    for col in column_names:
        non_null_percent = (1 - (null_counts[col] / num_rows)) * 100 if num_rows > 0 else 0
        print(f"  {col}: {non_null_percent:.2f}%")

    # (You can add more data profiling features here)


def csv_stats(filename):
    """
    Main function to orchestrate the CSV analysis.

    Args:
      filename (str): The path to the CSV file.
    """
    try:
        file_size, encoding = get_file_info(filename)

        start_time = time.time()
        data_types, unique_values, null_counts, value_counts, numeric_stats, num_rows = analyze_data(filename, encoding)
        elapsed_time = time.time() - start_time
        print(f"\nData analysis completed in {elapsed_time:.2f} seconds")

        print_stats(file_size, encoding, column_names, num_rows,
                    data_types, unique_values, null_counts, value_counts, numeric_stats)

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