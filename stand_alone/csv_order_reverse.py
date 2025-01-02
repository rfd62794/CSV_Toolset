import csv
import tkinter as tk
from tkinter import filedialog

def reverse_csv_order():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select the input CSV file
    input_file_path = filedialog.askopenfilename(
        title="Select Input CSV File",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )

    if not input_file_path:
        print("No input file selected. Exiting.")
        return

    # Generate the default output file name
    default_output_file_name = input_file_path.rsplit('.', 1)[0] + "_Reverse_Order.csv"

    # Ask the user to select the output file location and name
    output_file_path = filedialog.asksaveasfilename(
        title="Select Output CSV File Location",
        defaultextension=".csv",
        initialfile=default_output_file_name,
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )

    if not output_file_path:
        print("No output file selected. Exiting.")
        return

    try:
        with open(input_file_path, 'r', newline='') as csvfile, \
                open(output_file_path, 'w', newline='') as outfile:

            reader = csv.reader(csvfile)
            writer = csv.writer(outfile)

            # Detect header
            header = next(reader)  # Read the first row
            csvfile.seek(0)  # Reset file pointer to the beginning
            has_header = csv.Sniffer().has_header(csvfile.read(1024))
            csvfile.seek(0)  # Reset again after sniffing

            # Read all rows into a list
            rows = list(reader)

            if has_header:
                # Write the header first
                writer.writerow(rows[0])
                # Write the remaining rows in reverse order (excluding the header)
                writer.writerows(reversed(rows[1:]))
            else:
                # Write the rows in reverse order
                writer.writerows(reversed(rows))

        print(f"CSV file successfully reversed and saved to {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    reverse_csv_order()
