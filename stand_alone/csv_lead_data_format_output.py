import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
import chardet
import re

# Initialize the main window
window = tk.Tk()
window.title("Universal Lead Data Utility")

# --- Predefined Output Columns ---
output_columns = [
    "Business Name", "CRM Industry", "CRM Lead Source", "CRM URL", "Date Sold",
    "First Name", "Last Name", "GMB Review Count", "GMB Review Rating",
    "GMB URL Short", "Is Claimed", "NAICS Code", "Phone Type", "SIC Code",
    "SIC Description", "State", "Website URL", "Zip Code"
]

# --- Data Validation Rules ---
def validate_data(df, mapped_columns):
    # Initialize an empty list to store validation messages
    validation_messages = []

    # Iterate through the mapped columns and apply validation rules
    for col_name, map_to in mapped_columns.items():
        if map_to:
            # Apply validation based on the map_to column
            if map_to == "Business Name":
                # Check for non-empty string
                invalid_rows = df[col_name].isnull() | (df[col_name].str.strip() == "")
                if invalid_rows.any():
                    validation_messages.append(f"Invalid 'Business Name' found.")

            elif map_to in ("CRM Industry", "CRM Lead Source", "Phone Type"):
                # Check against predefined list (if available)
                # For now, assume the list is not available
                pass

            elif map_to in ("CRM URL", "GMB URL Short"):
                # Check for valid URL format using regex
                url_pattern = r"^(https?://|www\.)[^\s/$.?#].[^\s]*$"
                invalid_rows = ~df[col_name].astype(str).str.match(url_pattern)
                if invalid_rows.any():
                    validation_messages.append(f"Invalid URL format found in '{map_to}'.")

            elif map_to == "Date Sold":
                # Check for valid date format
                try:
                    pd.to_datetime(df[col_name])
                except ValueError:
                    validation_messages.append(f"Invalid 'Date Sold' format found.")

            elif map_to in ("First Name", "Last Name"):
                # Check for non-empty string
                invalid_rows = df[col_name].isnull() | (df[col_name].str.strip() == "")
                if invalid_rows.any():
                    validation_messages.append(f"Invalid '{map_to}' found.")

            elif map_to == "GMB Review Count":
                # Check for non-negative integer
                invalid_rows = (df[col_name] < 0) | (df[col_name].notnull() & ~df[col_name].astype(str).str.isdigit())
                if invalid_rows.any():
                    validation_messages.append(f"Invalid 'GMB Review Count' found.")

            elif map_to == "GMB Review Rating":
                # Check for float between 0 and 5
                invalid_rows = (df[col_name] < 0) | (df[col_name] > 5)
                if invalid_rows.any():
                    validation_messages.append(f"Invalid 'GMB Review Rating' found.")

            elif map_to == "Is Claimed":
                # Check for boolean (True/False)
                invalid_rows = df[col_name].notnull() & (~df[col_name].isin([True, False]))
                if invalid_rows.any():
                    validation_messages.append(f"Invalid 'Is Claimed' value found.")

            elif map_to in ("NAICS Code", "SIC Code"):
                # Check for valid code format (for now, assume any non-empty string is valid)
                invalid_rows = df[col_name].isnull() | (df[col_name].str.strip() == "")
                if invalid_rows.any():
                    validation_messages.append(f"Invalid '{map_to}' found.")

    # Return the list of validation messages
    return validation_messages

# --- File Handling ---
def import_csv():
    # Open a file dialog to select a CSV file
    filepath = filedialog.askopenfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        # Detect file encoding
        with open(filepath, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(filepath, encoding=encoding)

        # Display imported file information
        file_info.set(f"File: {filepath}\nRows: {len(df)}\nColumns: {len(df.columns)}")

        # Display input columns for matching
        display_columns(df)

    except Exception as e:
        file_info.set(f"Error importing file:\n{e}")

# --- Column Matching ---
def display_columns(df):
    # Clear existing column mapping
    for widget in column_mapping_frame.winfo_children():
        widget.destroy()

    # Create labels and dropdown menus for column mapping
    for i, col in enumerate(output_columns):
        ttk.Label(column_mapping_frame, text=col).grid(row=i, column=0, padx=5, pady=5)

        # Sort input column options
        options = [""] + sorted(df.columns)
        dropdown = ttk.Combobox(column_mapping_frame, values=options, state="readonly")
        dropdown.grid(row=i, column=1, padx=5, pady=5)

# --- Data Export ---
def export_csv(df, mapped_columns):
    # Open a file dialog to choose the export location and filename
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        # Create a dictionary to store the mapped columns
        selected_columns = {col: map_to for col, map_to in mapped_columns.items() if map_to}

        # Reorder columns according to output_columns
        selected_columns = {k: v for k, v in selected_columns.items() if v in output_columns}
        ordered_columns = [col for col in output_columns if col in selected_columns.values()]

        # Export selected and validated data to a new CSV file
        df_export = df[list(selected_columns.keys())].rename(columns=selected_columns)

        # Ensure all output columns are present, even if empty
        for col in output_columns:
            if col not in df_export.columns:
                df_export[col] = None

        # Export with the predefined column order
        df_export[ordered_columns].to_csv(filepath, index=False)

        # Display export success message
        file_info.set(f"File exported successfully to:\n{filepath}")

    except Exception as e:
        file_info.set(f"Error exporting file:\n{e}")

# --- GUI Elements ---
# Import CSV button
import_button = ttk.Button(window, text="Import CSV", command=import_csv)
import_button.pack(pady=10)

# Progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", mode="indeterminate")
progress_bar.pack(pady=10)

# File information display
file_info = tk.StringVar()
file_info_label = ttk.Label(window, textvariable=file_info)
file_info_label.pack(pady=10)

# Column mapping frame
column_mapping_frame = ttk.Frame(window)
column_mapping_frame.pack(pady=10)

# --- Core Functionality ---

def get_mapped_columns():
    """Retrieves the mapped columns from the dropdown menus."""
    mapped_columns = {}
    for i, col in enumerate(output_columns):
        dropdown = column_mapping_frame.grid_slaves(row=i, column=1)
        mapped_columns[dropdown.current()] = col
    return mapped_columns

def validate_data_command():
    """Validates the data based on the current column mapping."""
    mapped_columns = get_mapped_columns()
    validation_messages = validate_data(df, mapped_columns)
    if validation_messages:
        # Display validation messages in a new window
        validation_window = tk.Toplevel(window)
        validation_window.title("Validation Results")
        validation_text = tk.Text(validation_window)
        validation_text.pack(expand=True, fill="both")
        validation_text.insert("end", "\n".join(validation_messages))
        validation_text.config(state="disabled")
    else:
        file_info.set("Data validation successful!")

def export_csv_command():
    """Exports the data based on the current column mapping."""
    mapped_columns = get_mapped_columns()
    export_csv(df, mapped_columns)

# Validate Data button
validate_button = ttk.Button(window, text="Validate Data", command=validate_data_command)
validate_button.pack(pady=10)

# Export CSV button
export_button = ttk.Button(window, text="Export CSV", command=export_csv_command)
export_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()