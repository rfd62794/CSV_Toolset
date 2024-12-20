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
import psutil

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

def estimate_row_size(filename, encoding, sample_size=100):
    """
    Estimates the average row size by reading a sample of rows.

    Args:
      filename (str): The path to the CSV file.
      encoding (str): The file encoding.
      sample_size (int): The number of rows to sample.

    Returns:
      int: Estimated average row size in bytes.
    """
    with open(filename, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        sample_rows = [next(reader) for _ in range(sample_size)]
        total_size = sum(len(','.join(row).encode(encoding)) for row in sample_rows)
        average_row_size = total_size / sample_size
    return average_row_size

def estimate_total_rows(filename, encoding):
    """
    Estimates the total number of rows in the CSV file.

    Args:
      filename (str): The path to the CSV file.
      encoding (str): The file encoding.

    Returns:
      int: Estimated total number of rows.
    """
    with open(filename, 'r', encoding=encoding) as f:
        return sum(1 for _ in f) - 1  # Subtract 1 for the header row

def estimate_chunk_size(filename, encoding):
    """
    Estimates an optimal chunk size based on file size and available system memory.

    Args:
      filename (str): The path to the CSV file.
      encoding (str): The file encoding.

    Returns:
      int: Estimated chunk size in number of rows.
    """
    available_memory = psutil.virtual_memory().available
    average_row_size = estimate_row_size(filename, encoding)
    # Use up to 5% of available memory for processing to reduce chunk size
    max_memory_usage = available_memory * 0.05
    # Calculate the number of rows that can fit in the max memory usage
    chunk_size = int(max_memory_usage / average_row_size)
    # Ensure the chunk size is within a reasonable range
    chunk_size = min(max(chunk_size, 1000), 100000)  # Set a minimum and maximum limit
    return chunk_size

def analyze_data(filename, encoding):
    chunk_size = estimate_chunk_size(filename, encoding)
    print(f"Using chunk size: {chunk_size} rows")
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
            # Define patterns for different data types
            patterns = {
                'date': [
                    r'\d{4}-\d{2}-\d{2}',  # Date (YYYY-MM-DD)
                    r'\d{2}/\d{2}/\d{4}'   # Date (MM/DD/YYYY)
                ],
                'email': [
                    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                ],
                'url': [
                    r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
                ],
                'phone': [
                    r'(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US Phone number
                    r'^(?:\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'  # International Phone number
                ],
                'postcode': [
                    r'^(?:[A-Z]{1,2}\d{1,2}[A-Z]?)\s*\d[A-Z]{2}$'  # UK Postcode
                ],
                'boolean': [
                    r'^(true|false)$',  # Boolean
                ],
                'time': [
                    r'\d{2}:\d{2}(:\d{2})?'  # Time (HH:MM or HH:MM:SS)
                ]
            }

            # Check each pattern list
            for data_type, pattern_list in patterns.items():
                for pattern in pattern_list:
                    if re.match(pattern, value, re.IGNORECASE):
                        return data_type

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
    if 'values' in stats:
        stats['median'] = statistics.median(stats['values'])
        stats['std_dev'] = statistics.stdev(stats['values']) if len(stats['values']) > 1 else 0

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

def prompt_user_for_output():
    print("\nWould you like to save the analysis results?")
    print("1. JSON format")
    print("2. Text format")
    print("3. Both")
    print("4. None")
    choice = input("Enter your choice (1/2/3/4): ")
    return choice

def get_output_file_path(file_type):
    while True:
        file_path = input(f"Enter the destination path for {file_type} output (e.g., /path/to/results.{file_type}): ")
        if os.path.isdir(os.path.dirname(file_path)) or os.path.dirname(file_path) == '':
            return file_path
        else:
            print("Invalid directory. Please enter a valid path.")

def save_results(file_size, encoding, column_names, num_rows, 
                 data_types, unique_values, null_counts, value_counts, numeric_stats):
    choice = prompt_user_for_output()
    if choice == '1' or choice == '3':
        output_file_json = get_output_file_path('json')
        print_stats_to_json(file_size, encoding, column_names, num_rows, 
                            data_types, unique_values, null_counts, value_counts, numeric_stats, output_file_json)
        print(f"Results saved to {output_file_json}")

    if choice == '2' or choice == '3':
        output_file_txt = get_output_file_path('txt')
        print_stats_to_text(file_size, encoding, column_names, num_rows, 
                            data_types, unique_values, null_counts, value_counts, numeric_stats, output_file_txt)
        print(f"Results saved to {output_file_txt}")

def print_stats_to_text(file_size, encoding, column_names, num_rows, 
                        data_types, unique_values, null_counts, value_counts, numeric_stats, output_file):
    with open(output_file, 'w') as f:
        f.write("--- File Stats ---\n")
        f.write(f"File size: {file_size} bytes\n")
        f.write(f"Detected encoding: {encoding}\n\n")
        
        f.write("--- Data Stats ---\n")
        f.write(f"Column names: {column_names}\n")
        f.write(f"Number of rows: {num_rows}\n\n")
        
        f.write("Data types (with pattern matching):\n")
        for col, types in data_types.items():
            type_names = [t.__name__ if isinstance(t, type) else t for t in types]
            f.write(f"  {col}: {', '.join(type_names)}\n")
        
        f.write("\nUnique values:\n")
        for col, values in unique_values.items():
            f.write(f"  {col}: {len(values)}\n")
        
        f.write("\nNull value counts:\n")
        for col, count in null_counts.items():
            f.write(f"  {col}: {count}\n")
        
        f.write("\nMost frequent values:\n")
        for col, counts in value_counts.items():
            top_5_values = counts.most_common(5)
            f.write(f"  {col}: {top_5_values}\n")
        
        f.write("\nNumeric column statistics:\n")
        for col, stats in numeric_stats.items():
            if 'values' in stats:
                stats['median'] = statistics.median(stats['values'])
                stats['std_dev'] = statistics.stdev(stats['values']) if len(stats['values']) > 1 else 0
            f.write(f"  {col}: {stats}\n")

def print_static_info(filename, file_size, encoding, column_names, num_rows):
    # File metadata
    file_stats = os.stat(filename)
    last_modified = time.ctime(file_stats.st_mtime)
    creation_time = time.ctime(file_stats.st_ctime)

    print("\n--- Static Information ---")
    print(f"File size: {file_size} bytes")
    print(f"Detected encoding: {encoding}")
    print(f"Last modified: {last_modified}")
    print(f"Creation time: {creation_time}")
    print(f"Number of columns: {len(column_names)}")
    print(f"Number of rows: {num_rows}")

def print_data_completeness_summary(null_counts, num_rows):
    print("\n--- Data Completeness Summary ---")
    for col, null_count in null_counts.items():
        completeness = (1 - null_count / num_rows) * 100
        print(f"{col}: {completeness:.2f}% complete")

def print_top_frequent_values(value_counts, top_n=5):
    print("\n--- Top Frequent Values ---")
    for col, counts in value_counts.items():
        top_values = counts.most_common(top_n)
        print(f"{col}: {top_values}")

def csv_stats(filename, pause_after_print=True):
    """
    Main function to orchestrate the CSV analysis.

    Args:
      filename (str): The path to the CSV file.
      pause_after_print (bool): Whether to pause after printing stats.
    """
    try:
        file_size, encoding = get_file_info(filename)
        start_time = time.time()
        data_types, unique_values, null_counts, value_counts, numeric_stats, num_rows = analyze_data(filename, encoding)
        if num_rows == 0:
            print("The CSV file is empty.")
            return
        column_names = list(data_types.keys())
        elapsed_time = time.time() - start_time
        print(f"\nData analysis completed in {elapsed_time:.2f} seconds")

        # Print static information
        print_static_info(filename, file_size, encoding, column_names, num_rows)

        # Print data completeness summary
        print_data_completeness_summary(null_counts, num_rows)

        # Print top frequent values
        print_top_frequent_values(value_counts)

        save_results(file_size, encoding, column_names, num_rows,
                     data_types, unique_values, null_counts, value_counts, numeric_stats)

        if pause_after_print:
            input("Press Enter to continue...")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except UnicodeDecodeError:
        print("Error: Unable to decode the file with the detected encoding.")
    except csv.Error as e:
        print(f"CSV parsing error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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

def analyze_data_with_pandas(filename, encoding):
    df = pd.read_csv(filename, encoding=encoding)
    column_names = df.columns.tolist()
    num_rows = len(df)
    # Further analysis can be done using pandas methods
    return column_names, num_rows

if __name__ == "__main__":
    browse_file()