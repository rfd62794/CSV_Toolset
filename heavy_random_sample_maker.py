import csv
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import random

def create_sample_csv():
    """
    Creates a sample CSV file with randomly selected rows of user-specified size 
    or the full file if the requested size is larger than the original, 
    appending the actual size to the original filename.
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
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Get the header row
            # Convert to list to get length and allow multiple passes
            all_rows = list(reader)
            
        # Randomly select indices (without replacement)
        selected_indices = random.sample(range(len(all_rows)), actual_sample_size - 1)  # -1 for header
        
        # Write the randomly selected rows to the output file
        with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # Write header
            
            # Write the randomly selected rows
            for index in selected_indices:
                writer.writerow(all_rows[index])
                
        messagebox.showinfo("Success", f"Random sample CSV file created at {output_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to create CSV file: {e}")



if __name__ == "__main__":
    create_sample_csv()