import tkinter as tk
from tkinter import filedialog
import csv
import os

def reformat_csv(input_filename, output_filename):
    """
    Reformats a CSV file with potential non-plain-text characters.

    Args:
      input_filename: The path to the input CSV file.
      output_filename: The path to the output CSV file.
    """

    with open(input_filename, 'r', encoding='utf-8', errors='replace') as infile, \
         open(output_filename, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Clean up each field in the row
            cleaned_row = [field.encode('ascii', errors='ignore').decode('ascii') for field in row]
            writer.writerow(cleaned_row)

def browse_file():
    """Opens a file dialog for the user to select a CSV file."""

    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a CSV file",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )
    if filename:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)

def process_file():
    """Processes the selected file and saves the reformatted data."""

    input_filename = input_entry.get()
    # Construct the output filename with "_gentle" added
    base, ext = os.path.splitext(input_filename)
    output_filename = f"{base}_gentle{ext}"
    reformat_csv(input_filename, output_filename)
    result_label.config(text=f"Reformatted data saved to {output_filename}")

# Create the main window
window = tk.Tk()
window.title("CSV Reformatter")

# Input file selection
input_label = tk.Label(window, text="Select input CSV file:")
input_label.grid(row=0, column=0, padx=5, pady=5)

input_entry = tk.Entry(window, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Process button
process_button = tk.Button(window, text="Process", command=process_file)
process_button.grid(row=1, column=1, padx=5, pady=5)

# Result label
result_label = tk.Label(window, text="")
result_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

window.mainloop()