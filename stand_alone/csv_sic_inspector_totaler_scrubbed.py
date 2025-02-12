import os
import re
import csv
import logging
import datetime
import tkinter as tk
from tkinter import filedialog

def extract_sic_and_row_count(folder_path, log_file):
    """
    Extracts SIC code and row count from CSV files and logs the results.
    """

    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(message)s')  # Simplified log format
    logger = logging.getLogger(__name__)

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and "combined_matching_" in filename:
            match = re.search(r"combined_matching_(\d+)", filename)
            if match:
                sic_code = match.group(1)
            else:
                logger.warning(f"Filename {filename} does not match expected pattern.")
                continue

            filepath = os.path.join(folder_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    row_count = sum(1 for row in reader) - 1
                    logger.info(f"SIC Code {sic_code} - Row Count {row_count}")  # Specific format

            except FileNotFoundError:
                logger.error(f"File not found: {filepath}")
            except Exception as e:
                logger.error(f"Error processing file {filename}: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory(title="Select folder containing CSV files")

    if not folder_path:
        print("No folder selected. Exiting.")
        sys.exit(1)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(folder_path, f"sic_row_counts_{timestamp}.log")
    extract_sic_and_row_count(folder_path, log_file)
    print(f"SIC codes and row counts logged to: {log_file}")