import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import os
import glob
import random

class LeadDataProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Lead Data Processor")
        self.root.geometry("500x400")  # Set window size
        
        # Initialize variables
        self.source_folder = ""
        self.output_folder = ""
        self.designator_file = ""
        self.columns = []
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        self.create_widgets(main_frame)
    
    def create_widgets(self, frame):
        # Folder selection section
        folder_frame = ttk.LabelFrame(frame, text="Folder Selection", padding="5")
        folder_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.source_folder_label = ttk.Label(folder_frame, text="No source folder selected")
        self.source_folder_label.grid(row=0, column=0, sticky="w", padx=5)
        ttk.Button(folder_frame, text="Select Source Folder", command=self.select_source_folder).grid(row=0, column=1, padx=5)
        
        self.output_folder_label = ttk.Label(folder_frame, text="No output folder selected")
        self.output_folder_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Button(folder_frame, text="Select Output Folder", command=self.select_output_folder).grid(row=1, column=1, padx=5)
        
        # File selection section
        file_frame = ttk.LabelFrame(frame, text="File Selection", padding="5")
        file_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.designator_file_label = ttk.Label(file_frame, text="No designator file selected")
        self.designator_file_label.grid(row=0, column=0, sticky="w", padx=5)
        ttk.Button(file_frame, text="Select Designator File", command=self.select_designator_file).grid(row=0, column=1, padx=5)
        
        # Column mapping section
        mapping_frame = ttk.LabelFrame(frame, text="Column Mapping", padding="5")
        mapping_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Create dropdowns
        self.sic_prefix_dropdown = self.create_mapping_row(mapping_frame, "SIC Prefix Column:", 0)
        self.gmb_nj_dropdown = self.create_mapping_row(mapping_frame, "GMB NJ Column:", 1)
        self.gmb_ag_dropdown = self.create_mapping_row(mapping_frame, "GMB AG Column:", 2)
        self.osd_top_dropdown = self.create_mapping_row(mapping_frame, "OSD Top Column:", 3)
        self.osd_bottom_dropdown = self.create_mapping_row(mapping_frame, "OSD Bottom Column:", 4)
        
        # Progress section
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(frame, textvariable=self.progress_var)
        progress_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Start button
        ttk.Button(frame, text="Start Processing", command=self.start_processing).grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_mapping_row(self, parent, label_text, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=2)
        dropdown = ttk.Combobox(parent, values=self.columns, width=30)
        dropdown.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        return dropdown
    
    def select_source_folder(self):
        self.source_folder = filedialog.askdirectory()
        if self.source_folder:
            self.source_folder_label.config(text=f"Selected: {os.path.basename(self.source_folder)}")
    
    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.output_folder_label.config(text=f"Selected: {os.path.basename(self.output_folder)}")
    
    def select_designator_file(self):
        self.designator_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.designator_file:
            self.designator_file_label.config(text=f"Selected: {os.path.basename(self.designator_file)}")
            try:
                df = pd.read_csv(self.designator_file)
                self.columns = list(df.columns)
                for dropdown in [self.sic_prefix_dropdown, self.gmb_nj_dropdown, 
                               self.gmb_ag_dropdown, self.osd_top_dropdown, 
                               self.osd_bottom_dropdown]:
                    dropdown['values'] = self.columns
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read designator file: {str(e)}")
    
    def validate_inputs(self):
        if not all([self.source_folder, self.output_folder, self.designator_file]):
            messagebox.showerror("Error", "Please select all required folders and files.")
            return False
        
        if not all([self.sic_prefix_dropdown.get(), self.gmb_nj_dropdown.get(),
                   self.gmb_ag_dropdown.get(), self.osd_top_dropdown.get(),
                   self.osd_bottom_dropdown.get()]):
            messagebox.showerror("Error", "Please map all required columns.")
            return False
        
        return True
    
    def write_output_file(self, df, output_folder, sic_code, server_name, row_count, header):
        if row_count > 0:
            output_file = os.path.join(output_folder, f"{sic_code}_{server_name}_{row_count}.csv")
            
            if len(df) > row_count:
                random_indices = random.sample(range(len(df)), row_count)
                df_sampled = df.iloc[random_indices]
            else:
                df_sampled = df
            
            df_sampled.to_csv(output_file, index=False, header=header)
            return len(df_sampled)
        return 0
    
    def start_processing(self):
        if not self.validate_inputs():
            return
        
        try:
            df_designator = pd.read_csv(self.designator_file)
            total_rows = len(df_designator)
            processed_rows = 0
            
            for index, row in df_designator.iterrows():
                sic_code = str(row[self.sic_prefix_dropdown.get()]).zfill(4)  # Ensure 4-digit SIC code
                counts = {
                    "NJ": int(row[self.gmb_nj_dropdown.get()]),
                    "AG": int(row[self.gmb_ag_dropdown.get()]),
                    "OSD_Top": int(row[self.osd_top_dropdown.get()]),
                    "OSD_Bottom": int(row[self.osd_bottom_dropdown.get()])
                }
                
                processed_rows += 1
                self.progress_var.set(f"Processing SIC {sic_code} ({processed_rows}/{total_rows})")
                self.root.update()
                
                file_pattern = os.path.join(self.source_folder, f"combined_matching_{sic_code}_*")
                matching_files = glob.glob(file_pattern)
                
                if not matching_files:
                    messagebox.showwarning("Warning", f"No matching file found for SIC Code: {sic_code}")
                    continue
                
                lead_file = matching_files[0]
                df_lead = pd.read_csv(lead_file)
                header = list(df_lead.columns)
                
                for server_name, count in counts.items():
                    output_folder = os.path.join(self.output_folder, server_name)
                    os.makedirs(output_folder, exist_ok=True)
                    rows_written = self.write_output_file(
                        df_lead, output_folder, sic_code, server_name, count, header
                    )
                    if rows_written < count:
                        messagebox.showwarning(
                            "Warning", 
                            f"Not enough rows in source file for SIC {sic_code} {server_name}. "
                            f"Requested: {count}, Available: {rows_written}"
                        )
            
            self.progress_var.set("Processing complete!")
            messagebox.showinfo("Success", "Processing complete!")
            
        except Exception as e:
            self.progress_var.set("Error occurred during processing")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LeadDataProcessor(root)
    root.mainloop()