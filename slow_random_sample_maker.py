import csv
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import random

def create_sample_csv():
    """
    Creates a sample CSV file with randomly selected rows using reservoir sampling,
    which maintains constant memory usage regardless of input file size.
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
            total_rows = sum(1 for row in reader) + 1  # +1 to include the header
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read CSV file: {e}")
        return
    
    # Get desired sample size from user
    while True:
        try:
            sample_size = simpledialog.askinteger("Input", f"Enter the desired sample size (max {total_rows}):")
            if sample_size is None:  # User canceled
                return
            if sample_size > 0:
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

    try:
        # First pass: read header and create temporary file
        temp_file_path = output_file_path + '.tmp'
        
        with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
             open(temp_file_path, 'w', newline='', encoding='utf-8') as temp_file:
            
            reader = csv.reader(infile)
            writer = csv.writer(temp_file)
            
            header = next(reader)  # Skip header in count
            
            # Reservoir sampling algorithm
            reservoir = []
            for i, row in enumerate(reader):
                if i < actual_sample_size - 1:  # -1 because we don't count header
                    reservoir.append(row)
                else:
                    j = random.randint(0, i)
                    if j < actual_sample_size - 1:
                        reservoir[j] = row

            # Write header and reservoir to temp file
            writer.writerow(header)
            writer.writerows(reservoir)

        # Replace original output file with temp file
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        os.rename(temp_file_path, output_file_path)
        
        messagebox.showinfo("Success", f"Random sample CSV file created at {output_file_path}")

    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        messagebox.showerror("Error", f"Failed to create CSV file: {e}")

if __name__ == "__main__":
    create_sample_csv()