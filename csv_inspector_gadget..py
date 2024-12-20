import csv
import os
import chardet
from collections import defaultdict, Counter
import re
import time
import tkinter as tk
from tkinter import filedialog
import statistics
import pandas as pd

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
            process_row(row, column_names, data_types, unique_values, null_counts, value_counts, numeric_stats)

    return data_types, unique_values, null_counts, value_counts, numeric_stats, num_rows

def process_row(row, column_names, data_types, unique_values, null_counts, value_counts, numeric_stats):
    for i, value in enumerate(row):
        process_value(value, column_names[i], data_types, unique_values, null_counts, value_counts, numeric_stats)

def process_value(value, column_name, data_types, unique_values, null_counts, value_counts, numeric_stats):
    detected_type = detect_data_type(value)
    data_types[column_name].add(detected_type)
    unique_values[column_name].add(value)
    if value == '' or value is None:
        null_counts[column_name] += 1
    value_counts[column_name][value] += 1
    update_numeric_stats(numeric_stats, column_name, value)

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
    num_value = convert_to_numeric(value)
    if num_value is not None:
        update_stats(numeric_stats[column_name], num_value)
        numeric_stats[column_name].setdefault('values', []).append(num_value)

def convert_to_numeric(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return None

def update_stats(stats, num_value):
    stats.setdefault('count', 0)
    stats['count'] += 1
    stats.setdefault('min', num_value)
    stats['min'] = min(stats['min'], num_value)
    stats.setdefault('max', num_value)
    stats['max'] = max(stats['max'], num_value)
    stats.setdefault('values', []).append(num_value)

def print_stats(file_size, encoding, column_names, num_rows, 
                data_types, unique_values, null_counts, value_counts, numeric_stats):
    print_file_info(file_size, encoding)
    print_data_overview(column_names, num_rows)
    print_data_types(data_types)
    print_unique_values(unique_values)
    print_null_counts(null_counts)
    print_value_counts(value_counts)
    print_numeric_stats(numeric_stats)
    print_data_completeness(column_names, null_counts, num_rows)

def print_file_info(file_size, encoding):
    print("\n--- File Stats ---")
    print(f"File size: {file_size} bytes")
    print(f"Detected encoding: {encoding}")

def print_data_overview(column_names, num_rows):
    print("\n--- Data Stats ---")
    print(f"Column names: {column_names}")
    print(f"Number of rows: {num_rows}")

def print_data_types(data_types):
    print("\nData types (with pattern matching):")
    for col, types in data_types.items():
        type_names = [t.__name__ if isinstance(t, type) else t for t in types]
        print(f"  {col}: {', '.join(type_names)}")

def print_unique_values(unique_values):
    print("\nUnique values:")
    for col, values in unique_values.items():
        print(f"  {col}: {len(values)}")

def print_null_counts(null_counts):
    print("\nNull value counts:")
    for col, count in null_counts.items():
        print(f"  {col}: {count}")

def print_value_counts(value_counts):
    print("\nMost frequent values:")
    for col, counts in value_counts.items():
        top_5_values = counts.most_common(5)
        print(f"  {col}: {top_5_values}")

def print_numeric_stats(numeric_stats):
    print("\nNumeric column statistics:")
    for col, stats in numeric_stats.items():
        if 'values' in stats:
            stats['median'] = statistics.median(stats['values'])
            stats['std_dev'] = statistics.stdev(stats['values']) if len(stats['values']) > 1 else 0
        print(f"  {col}: {stats}")

def print_data_completeness(column_names, null_counts, num_rows):
    print("\nData Completeness:")
    for col in column_names:
        non_null_percent = (1 - (null_counts[col] / num_rows)) * 100 if num_rows > 0 else 0
        print(f"  {col}: {non_null_percent:.2f}%")

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