import tkinter as tk
from tkinter import filedialog
import csv
import chardet

def shorten_data(input_file, output_file, column_index, encoding):
    """
    Shortens the data in the specified column of a CSV file to the first 4 digits.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        column_index (int): Index of the column to shorten (starting from 0).
        encoding (str): Encoding of the CSV file.
    """

    with open(input_file, 'r', newline='', encoding=encoding) as infile, \
         open(output_file, 'w', newline='', encoding=encoding) as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header row unchanged
        header = next(reader)
        writer.writerow(header)

        # Process data rows
        for row in reader:
            try:
                # Shorten the data in the specified column
                row[column_index] = row[column_index][:4]
            except IndexError:
                print(f"Warning: Row '{row}' has fewer columns than expected. Skipping shortening.")
            writer.writerow(row)

def detect_encoding(file_path):
    """
    Detects the encoding of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The detected encoding.
    """

    with open(file_path, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    return result['encoding']

def process_file():
    """
    Handles file selection, column selection, and data shortening.
    """

    # Open file dialog for user to select input file
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    input_file = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if not input_file:
        return  # User canceled file selection

    # Detect file encoding
    encoding = detect_encoding(input_file)
    print(f"Detected encoding: {encoding}")

    # Read column names from the CSV file
    with open(input_file, 'r', newline='', encoding=encoding) as infile:
        reader = csv.reader(infile)
        column_names = next(reader)

    # Display column names for user selection
    print("Available columns:")
    for i, name in enumerate(column_names):
        print(f"{i+1}-{name}")

    while True:
        try:
            column_choice = int(input("Enter the number of the column to shorten: ")) - 1
            if 0 <= column_choice < len(column_names):
                break
            else:
                print("Invalid column number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Construct output filename
    output_file = input_file.rsplit('.', 1)[0] + "_short.csv"

    # Shorten the data in the selected column
    shorten_data(input_file, output_file, column_choice, encoding)

    print(f"Shortened data saved to: {output_file}")

if __name__ == "__main__":
    process_file()