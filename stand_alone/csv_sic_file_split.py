import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import os
import glob
import random

def select_source_folder():
    global source_folder
    source_folder = filedialog.askdirectory()
    source_folder_label.config(text=source_folder)

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    output_folder_label.config(text=output_folder)

def select_designator_file():
    global designator_file, columns
    designator_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    designator_file_label.config(text=designator_file)
    try:
        df = pd.read_csv(designator_file)
        columns = list(df.columns)
        sic_prefix_dropdown['values'] = columns
        gmb_nj_dropdown['values'] = columns
        gmb_ag_dropdown['values'] = columns
        osd_top_dropdown['values'] = columns
        osd_bottom_dropdown['values'] = columns
    except FileNotFoundError:
        messagebox.showerror("Error", "Designator file not found.")
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", "Designator file is empty.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_processing():
    try:
        df_designator = pd.read_csv(designator_file)

        sic_prefix_col = sic_prefix_dropdown.get()
        gmb_nj_col = gmb_nj_dropdown.get()
        gmb_ag_col = gmb_ag_dropdown.get()
        osd_top_col = osd_top_dropdown.get()
        osd_bottom_col = osd_bottom_dropdown.get()

        for index, row in df_designator.iterrows():
            sic_code = str(row[sic_prefix_col])
            gmb_nj_count = int(row[gmb_nj_col])  # Ensure integer for slicing
            gmb_ag_count = int(row[gmb_ag_col])
            osd_top_count = int(row[osd_top_col])
            osd_bottom_count = int(row[osd_bottom_col])

            file_pattern = os.path.join(source_folder, f"combined_matching_{sic_code}_*")
            matching_files = glob.glob(file_pattern)

            if matching_files:
                lead_file = matching_files[0]
                df_lead = pd.read_csv(lead_file)

                output_nj_folder = os.path.join(output_folder, "NJ")
                output_ag_folder = os.path.join(output_folder, "AG")
                output_osd_top_folder = os.path.join(output_folder, "OSD_Top")
                output_osd_bottom_folder = os.path.join(output_folder, "OSD_Bottom")

                os.makedirs(output_nj_folder, exist_ok=True)
                os.makedirs(output_ag_folder, exist_ok=True)
                os.makedirs(output_osd_top_folder, exist_ok=True)
                os.makedirs(output_osd_bottom_folder, exist_ok=True)

                header = list(df_lead.columns)
                write_output_file(df_lead, output_nj_folder, sic_code, "NJ", gmb_nj_count, header)
                write_output_file(df_lead, output_ag_folder, sic_code, "AG", gmb_ag_count, header)
                write_output_file(df_lead, output_osd_top_folder, sic_code, "OSD_Top", osd_top_count, header)
                write_output_file(df_lead, output_osd_bottom_folder, sic_code, "OSD_Bottom", osd_bottom_count, header)
            else:
                messagebox.showwarning("Warning", f"No matching file found for SIC Code: {sic_code}")

        messagebox.showinfo("Success", "Processing complete.")

    except FileNotFoundError:
        messagebox.showerror("Error", "Source or output folder not selected.")
    except ValueError:
        messagebox.showerror("Error", "Invalid count values in Designator CSV. Must be integers.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def write_output_file(df, output_folder, sic_code, server_name, row_count, header):
    if row_count > 0:
        output_file = os.path.join(output_folder, f"{sic_code}_{server_name}_{row_count}")

        # Randomly select rows
        if len(df) > row_count:  # Check if enough rows are available
            random_indices = random.sample(range(len(df)), row_count)
            df_sampled = df.iloc[random_indices]
        else:
            df_sampled = df  # Use all rows if not enough available

        df_sampled.to_csv(output_file, index=False, header=header)


root = tk.Tk()
root.title("Lead Data Processor")

source_folder_label = tk.Label(root, text="Source Folder:")
source_folder_label.grid(row=0, column=0, sticky="w")
source_folder_button = tk.Button(root, text="Select Source Folder", command=select_source_folder)
source_folder_button.grid(row=0, column=1)

output_folder_label = tk.Label(root, text="Output Folder:")
output_folder_label.grid(row=1, column=0, sticky="w")
output_folder_button = tk.Button(root, text="Select Output Folder", command=select_output_folder)
output_folder_button.grid(row=1, column=1)

designator_file_label = tk.Label(root, text="Designator File:")
designator_file_label.grid(row=2, column=0, sticky="w")
designator_file_button = tk.Button(root, text="Select Designator File", command=select_designator_file)
designator_file_button.grid(row=2, column=1)

columns = []

sic_prefix_label = tk.Label(root, text="SIC Prefix Column:")
sic_prefix_label.grid(row=3, column=0, sticky="w")
sic_prefix_dropdown = ttk.Combobox(root, values=columns)
sic_prefix_dropdown.grid(row=3, column=1)

gmb_nj_label = tk.Label(root, text="GMB NJ Column:")
gmb_nj_label.grid(row=4, column=0, sticky="w")
gmb_nj_dropdown = ttk.Combobox(root, values=columns)
gmb_nj_dropdown.grid(row=4, column=1)

gmb_ag_label = tk.Label(root, text="GMB AG Column:")
gmb_ag_label.grid(row=5, column=0, sticky="w")
gmb_ag_dropdown = ttk.Combobox(root, values=columns)
gmb_ag_dropdown.grid(row=5, column=1)

osd_top_label = tk.Label(root, text="OSD Top Column:")
osd_top_label.grid(row=6, column=0, sticky="w")
osd_top_dropdown = ttk.Combobox(root, values=columns)
osd_top_dropdown.grid(row=6, column=1)

osd_bottom_label = tk.Label(root, text="OSD Bottom Column:")
osd_bottom_label.grid(row=7, column=0, sticky="w")
osd_bottom_dropdown = ttk.Combobox(root, values=columns)
osd_bottom_dropdown.grid(row=7, column=1)

start_button = tk.Button(root, text="Start Processing", command=start_processing)
start_button.grid(row=8, column=0, columnspan=2)

root.mainloop()