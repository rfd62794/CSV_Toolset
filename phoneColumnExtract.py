import os
import pandas as pd
from tkinter import Tk, filedialog, Button, Label
import csv

def select_file():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        process_csv_files(file_path, select_destination_folder())

def select_folder():
    folder_path = filedialog.askdirectory(title="Select a Folder")
    if folder_path:
        process_csv_files(folder_path, select_destination_folder())

def select_destination_folder():
    return filedialog.askdirectory(title="Select Destination Folder")

def process_csv_files(source_path, destination_folder):
    if not destination_folder:
        print("No destination folder selected.")
        return

    if os.path.isfile(source_path):
        files = [source_path]
    else:
        files = [os.path.join(source_path, f) for f in os.listdir(source_path) if f.endswith('.csv') and not f.endswith('_Phone.csv')]

    for file in files:
        try:
            df = pd.read_csv(file, low_memory=False, sep=',', quoting=csv.QUOTE_MINIMAL, on_bad_lines='warn')
            if 'Phone' in df.columns:
                df['Phone'] = pd.to_numeric(df['Phone'], errors='coerce')
                phone_data = df[['Phone']].dropna().astype('Int64')
                new_filename = os.path.splitext(os.path.basename(file))[0] + "_Phone.csv"
                new_filepath = os.path.join(destination_folder, new_filename)
                phone_data.to_csv(new_filepath, index=False)
                print(f"Processed: {file} -> {new_filepath}")
            else:
                print(f"Column 'Phone' not found in {file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")

def create_gui():
    root = Tk()
    root.title("CSV Phone Column Extractor")

    label = Label(root, text="Select a File or Folder to Process")
    label.pack(pady=10)

    file_button = Button(root, text="Select File", command=select_file)
    file_button.pack(pady=5)

    folder_button = Button(root, text="Select Folder", command=select_folder)
    folder_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()