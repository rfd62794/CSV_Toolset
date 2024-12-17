import csv
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

def create_sample_csv():
    """
    Creates a sample CSV file with user-specified size or the full file 
    if the requested size is larger than the original, appending the 
    actual size to the original filename.
    """

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get input file path from user
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )

    if not file_path:  # User canceled
        return

    # Get total number of rows in the CSV
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Get the header row
            total_rows = sum(1 for row in reader) + 1 # +1 to include the header
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read CSV file: {e}")
        return
    
    # Get desired sample size from user
    while True:
        try:
            sample_size = simpledialog.askinteger("Input", f"Enter the desired sample size (max {total_rows}):")
            if sample_size is None:  # User canceled
                return
            if sample_size > 0 :
                break
            else:
                messagebox.showerror("Error", "Sample size must be a positive integer.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a positive integer.")


    # Determine the actual sample size (cannot exceed the total number of rows)
    actual_sample_size = min(sample_size, total_rows)


    # Construct output file path with actual sample size in the name
    filename, ext = os.path.splitext(os.path.basename(file_path))
    output_file_path = os.path.join(
        os.path.dirname(file_path), f"{filename}_sample_{actual_sample_size}{ext}"
    )

    # Read and write the appropriate number of rows to the sample file
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            writer.writerow(next(reader)) # write header

            for i in range(actual_sample_size -1): # -1 as we already wrote the header
                try:
                    row = next(reader)
                    writer.writerow(row)
                except StopIteration:
                    break  # Stop if we reach the end of the input file
                
        messagebox.showinfo("Success", f"Sample CSV file created at {output_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to create CSV file: {e}")



if __name__ == "__main__":
    create_sample_csv()