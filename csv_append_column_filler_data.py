import tkinter as tk
from tkinter import filedialog
import csv
import os
import chardet

def select_csv_file():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a CSV File",
                                          filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    if filename:
        file_label.config(text=filename)

def select_csv_folder():
    global filename
    filename = filedialog.askdirectory(initialdir="/", title="Select a Folder")
    if filename:
        file_label.config(text=filename)

def select_destination_folder():
    global destination_folder
    destination_folder = filedialog.askdirectory(initialdir="/", title="Select Destination Folder")
    if destination_folder:
        destination_label.config(text=destination_folder)

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def add_column():
    column_name = column_entry.get()
    filler_value = filler_entry.get()

    if not column_name or not filename:
        error_label.config(text="Please select a file/folder and enter a column name.")
        return

    encodings_to_try = ['utf-8', 'ascii', 'latin-1', 'iso-8859-1', 'cp1252']

    files_to_process = []
    if os.path.isdir(filename):
        for root, _, files in os.walk(filename):
            for file in files:
                if file.endswith('.csv'):
                    files_to_process.append(os.path.join(root, file))
    else:
        files_to_process.append(filename)

    for file in files_to_process:
        detected_encoding = detect_encoding(file)
        try:
            with open(file, 'r', encoding=detected_encoding) as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                header = data[0]
                header.append(column_name)
                for row in data[1:]:
                    row.append(filler_value)

            base_filename = os.path.splitext(os.path.basename(file))[0]
            new_filename = f"{base_filename}_{column_name.replace(' ', '_')}.csv"
            new_filepath = os.path.join(destination_folder, new_filename)

            with open(new_filepath, 'w', newline='', encoding=detected_encoding) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerows(data[1:])

            error_label.config(text="Column added successfully!")

        except (UnicodeDecodeError, FileNotFoundError) as e:
            error_label.config(text=f"Error processing file {file}: {str(e)}")
            continue

    error_label.config(text="Processing complete.")

root = tk.Tk()
root.title("CSV Column Appender")

select_file_button = tk.Button(root, text="Select CSV File", command=select_csv_file)
select_file_button.pack(pady=10)

select_folder_button = tk.Button(root, text="Select CSV Folder", command=select_csv_folder)
select_folder_button.pack(pady=10)

file_label = tk.Label(root, text="No file or folder selected")
file_label.pack()

destination_button = tk.Button(root, text="Select Destination Folder", command=select_destination_folder)
destination_button.pack(pady=10)

destination_label = tk.Label(root, text="No destination folder selected")
destination_label.pack()

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