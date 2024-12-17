import tkinter as tk
from tkinter import filedialog
import csv
import os

def select_csv_file():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("CSV files", "*.csv*"), ("all files","*.*")))
    if filename:
        file_label.config(text=filename)

def add_column():
    column_name = column_entry.get()
    filler_value = filler_entry.get()

    if not column_name or not filename:
        error_label.config(text="Please select a file and enter a column name.")
        return

    encodings_to_try = ['utf-8', 'ascii', 'latin-1', 'iso-8859-1', 'cp1252']  # List of encodings to try

    for encoding in encodings_to_try:
        try:
            with open(filename, 'r', encoding=encoding) as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                header = data[0]
                header.append(column_name)
                for row in data[1:]:
                    row.append(filler_value)

            # Generate the new filename
            base_filename = os.path.splitext(filename)[0]
            new_filename = f"{base_filename}_{column_name}.csv"

            with open(new_filename, 'w', newline='', encoding=encoding) as csvfile:  # Use the same encoding for writing
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerows(data[1:])

            error_label.config(text="Column added successfully!")
            return  # Exit the loop if successful

        except UnicodeDecodeError:
            continue  # Try the next encoding if UnicodeDecodeError occurs

    # If none of the encodings worked
    error_label.config(text="Could not determine file encoding.")

root = tk.Tk()
root.title("CSV Column Appender")

select_button = tk.Button(root, text="Select CSV File", command=select_csv_file)
select_button.pack(pady=10)

file_label = tk.Label(root, text="No file selected")
file_label.pack()

column_label = tk.Label(root, text="Enter Column Name:")
column_label.pack()

column_entry = tk.Entry(root)
column_entry.pack()

filler_label = tk.Label(root, text="Enter Filler Value (optional):")
filler_label.pack()

filler_entry = tk.Entry(root)
filler_entry.pack()

add_button = tk.Button(root, text="Add Column", command=add_column)
add_button.pack(pady=10)

error_label = tk.Label(root, text="", fg="red")
error_label.pack()

root.mainloop()