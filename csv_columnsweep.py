import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def open_csv_file():
    """Opens a CSV file, reads the column names, and populates the listbox."""
    global file_path
    file_path = filedialog.askopenfilename(
        title="Select CSV File", filetypes=[("CSV Files", "*.csv")]
    )
    if file_path:
        try:
            # Try opening with different encodings
            encodings_to_try = ["utf-8", "latin-1", "cp1252"]
            for encoding in encodings_to_try:
                try:
                    with open(file_path, "r", newline="", encoding=encoding) as file:
                        reader = csv.reader(file)
                        columns = next(reader)  # Get column names
                        column_listbox.delete(0, tk.END)  # Clear listbox
                        for col in columns:
                            column_listbox.insert(tk.END, col)
                    break  # Break loop if successful
                except UnicodeDecodeError:
                    pass  # Try next encoding
            else:
                messagebox.showerror(
                    "Error", "Failed to open file: Could not determine file encoding."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")


def process_csv_data():
    """Removes rows with missing data in the selected column and saves to a new CSV file."""
    global file_path
    selected_column = column_listbox.get(tk.ANCHOR)
    if not selected_column:
        messagebox.showwarning("Warning", "Please select a column.")
        return

    try:
        filename = os.path.splitext(os.path.basename(file_path))[0]
        new_filename = f"{filename}_purged_{selected_column}.csv"

        # Try different encodings
        encodings_to_try = ["utf-8", "latin-1", "cp1252"]
        for encoding in encodings_to_try:
            try:
                with open(file_path, "r", newline="", encoding=encoding) as infile, open(
                    new_filename, "w", newline="", encoding=encoding
                ) as outfile:
                    reader = csv.DictReader(infile)
                    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    for row in reader:
                        if row[selected_column]:  # Check for non-empty value
                            writer.writerow(row)
                messagebox.showinfo(
                    "Success", f"Data processed and saved to {new_filename}"
                )
                return  # Stop trying encodings
            except UnicodeDecodeError:
                pass  # Try next encoding
        else:
            messagebox.showerror(
                "Error", "Failed to process data: Could not determine file encoding."
            )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process data: {e}")


def main():
    """Sets up the main application window and runs the Tkinter event loop."""
    global column_listbox
    root = tk.Tk()
    root.title("CSV Data Processor")

    open_button = tk.Button(root, text="Open CSV File", command=open_csv_file)
    open_button.pack(pady=10)

    process_button = tk.Button(root, text="Process Data", command=process_csv_data)
    process_button.pack(pady=10)

    column_listbox = tk.Listbox(root)
    column_listbox.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()