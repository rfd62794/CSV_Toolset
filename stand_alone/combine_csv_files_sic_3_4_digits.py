import pandas as pd
import glob
import os
import re
import tkinter as tk
from tkinter import filedialog
import shutil

def combine_csvs(folder_path, output_folder):
    """Combines CSV files, saving combined files to a new subfolder."""

    dataframes = {}
    file_pattern = os.path.join(folder_path, "*_matching_*.csv")
    csv_files = glob.glob(file_pattern)

    for file_path in csv_files:
        filename = os.path.basename(file_path)
        match = re.search(r"_matching_(\d+)\.csv", filename)
        if match:
            sic_code = match.group(1)
            sic_code_4digit = sic_code.zfill(4)

            try:
                df = pd.read_csv(file_path)

                if sic_code_4digit in dataframes:
                    dataframes[sic_code_4digit] = pd.concat([dataframes[sic_code_4digit], df], ignore_index=True)
                    print(f"Appended {filename} to SIC code {sic_code_4digit}")
                else:
                    dataframes[sic_code_4digit] = df
                    print(f"Created dataframe for SIC code {sic_code_4digit} from {filename}")

            except pd.errors.EmptyDataError:
                print(f"Warning: File {filename} is empty. Skipping.")
            except Exception as e:
                print(f"Error reading file {filename}: {e}")

    # Save the combined dataframes to the output folder
    for sic_code, df in dataframes.items():
        output_filename = os.path.join(output_folder, f"combined_matching_{sic_code}.csv")
        df.to_csv(output_filename, index=False)
        print(f"Saved combined data for SIC code {sic_code} to {output_filename}")


def browse_folder():
    """Opens a file dialog to select the folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:  # Check if the user selected a folder
        output_folder = os.path.join(folder_path, "Combined")
        os.makedirs(output_folder, exist_ok=True) # Create "Combined" subfolder
        combine_csvs(folder_path, output_folder)
    else:
        print("No folder selected.")


# Create the main Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Call the browse_folder function to start the process
browse_folder()