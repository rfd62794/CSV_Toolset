import os
import pandas as pd
from tkinter import Tk, filedialog, simpledialog
import csv

def select_file_or_folder():
    root = Tk()
    root.withdraw()  # Hide the root window
    choice = simpledialog.askstring("Input", "Type 'File' to select a file or 'Folder' to select a folder:")
    
    if choice and choice.lower() == 'file':
        return filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv")])
    elif choice and choice.lower() == 'folder':
        return filedialog.askdirectory(title="Select a Folder")
    else:
        print("Invalid choice or no selection made.")
        return None

def select_destination_folder():
    root = Tk()
    root.withdraw()  # Hide the root window
    return filedialog.askdirectory(title="Select Destination Folder")

def process_csv_files(source_path, destination_folder):
    if os.path.isfile(source_path):
        files = [source_path]
    else:
        files = [os.path.join(source_path, f) for f in os.listdir(source_path) if f.endswith('.csv') and not f.endswith('_Phone.csv')]

    for file in files:
        try:
            df = pd.read_csv(file, low_memory=False, sep=',', quoting=csv.QUOTE_MINIMAL, error_bad_lines=False, warn_bad_lines=True)
            if 'Phone' in df.columns:
                # Attempt to convert 'Phone' column to numeric, coercing errors to NaN
                df['Phone'] = pd.to_numeric(df['Phone'], errors='coerce')
                phone_data = df[['Phone']].dropna().astype('Int64')  # Use 'Int64' to handle NaNs
                new_filename = os.path.splitext(os.path.basename(file))[0] + "_Phone.csv"
                new_filepath = os.path.join(destination_folder, new_filename)
                phone_data.to_csv(new_filepath, index=False)
                print(f"Processed: {file} -> {new_filepath}")
            else:
                print(f"Column 'Phone' not found in {file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    source_path = select_file_or_folder()
    if source_path:
        destination_folder = select_destination_folder()
        if destination_folder:
            process_csv_files(source_path, destination_folder)
        else:
            print("No destination folder selected.")
    else:
        print("No file or folder selected.")