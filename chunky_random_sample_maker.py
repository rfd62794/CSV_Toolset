import csv
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import os
import random
import psutil
import time

def get_recommended_chunk_size():
    """
    Calculate recommended chunk sizes based on available system memory.
    Returns a dict with small, medium, and large chunk recommendations.
    """
    # Get available memory in bytes
    available_memory = psutil.virtual_memory().available
    
    # Estimate memory needed per row (assuming average CSV row ~500 bytes)
    estimated_row_size = 500  # bytes
    
    # Calculate different chunk sizes based on available memory
    # Use only 20% of available memory for large chunks to be safe
    max_safe_rows = int((available_memory * 0.2) / estimated_row_size)
    
    return {
        'small': min(5000, max_safe_rows),
        'medium': min(50000, max_safe_rows),
        'large': min(500000, max_safe_rows)
    }

def ask_chunk_size():
    """
    Prompt user to choose chunk size with recommendations.
    """
    chunk_sizes = get_recommended_chunk_size()
    
    # Create a custom dialog
    dialog = tk.Toplevel()
    dialog.title("Choose Chunk Size")
    dialog.geometry("400x300")
    
    # Center the window
    dialog.geometry("+%d+%d" % (
        dialog.winfo_screenwidth()/2 - 200,
        dialog.winfo_screenheight()/2 - 150))
    
    # Add explanation text
    tk.Label(dialog, text="Select chunk size for processing:", pady=10).pack()
    tk.Label(dialog, text="Larger chunks = faster but more memory usage\n"
             "Smaller chunks = slower but less memory usage", pady=5).pack()
    
    # Format memory sizes for display
    def format_size(num_rows):
        memory_usage = (num_rows * 500) / (1024 * 1024)  # Convert to MB
        return f"{num_rows:,} rows (~{memory_usage:.1f} MB)"
    
    selected_size = tk.StringVar(value=str(chunk_sizes['medium']))  # Default to medium
    
    # Add radio buttons for each option
    tk.Radiobutton(dialog, 
                   text=f"Small: {format_size(chunk_sizes['small'])}",
                   variable=selected_size,
                   value=str(chunk_sizes['small'])).pack(pady=5, anchor='w', padx=20)
    
    tk.Radiobutton(dialog, 
                   text=f"Medium: {format_size(chunk_sizes['medium'])}",
                   variable=selected_size,
                   value=str(chunk_sizes['medium'])).pack(pady=5, anchor='w', padx=20)
    
    tk.Radiobutton(dialog, 
                   text=f"Large: {format_size(chunk_sizes['large'])}",
                   variable=selected_size,
                   value=str(chunk_sizes['large'])).pack(pady=5, anchor='w', padx=20)
    
    # Custom size entry
    custom_frame = tk.Frame(dialog)
    custom_frame.pack(pady=10)
    custom_radio = tk.Radiobutton(custom_frame, text="Custom:", 
                                 variable=selected_size,
                                 value="custom")
    custom_radio.pack(side='left')
    custom_entry = tk.Entry(custom_frame, width=10)
    custom_entry.pack(side='left', padx=5)
    tk.Label(custom_frame, text="rows").pack(side='left')
    
    def on_custom_entry_click(event):
        custom_radio.select()
    
    custom_entry.bind('<Button-1>', on_custom_entry_click)
    custom_entry.bind('<Key>', on_custom_entry_click)
    
    result = {'chunk_size': None}
    
    def on_ok():
        try:
            if selected_size.get() == "custom":
                if not custom_entry.get().strip():
                    messagebox.showerror("Error", "Please enter a custom chunk size")
                    return
                result['chunk_size'] = int(custom_entry.get())
                if result['chunk_size'] <= 0:
                    messagebox.showerror("Error", "Chunk size must be positive")
                    return
            else:
                result['chunk_size'] = int(selected_size.get())
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def on_cancel():
        result['chunk_size'] = None
        dialog.destroy()
    
    # Add OK/Cancel buttons
    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="OK", command=on_ok, width=10).pack(side='left', padx=10)
    tk.Button(button_frame, text="Cancel", command=on_cancel, width=10).pack(side='left')
    
    dialog.transient(dialog.master)
    dialog.grab_set()
    dialog.wait_window()
    
    return result['chunk_size']

class ProgressWindow:
    def __init__(self, parent, total_rows):
        self.window = tk.Toplevel(parent)
        self.window.title("Processing")
        self.window.geometry("400x150")
        
        # Center the window
        self.window.geometry("+%d+%d" % (
            self.window.winfo_screenwidth()/2 - 200,
            self.window.winfo_screenheight()/2 - 75))
        
        # Make window stay on top
        self.window.transient(parent)
        self.window.grab_set()
        
        # Progress information
        self.total_rows = total_rows
        self.start_time = time.time()
        
        # Create and pack widgets
        self.status_label = tk.Label(self.window, text="Initializing...", pady=10)
        self.status_label.pack()
        
        self.progress_frame = ttk.Frame(self.window)
        self.progress_frame.pack(fill='x', padx=20)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            variable=self.progress_var, 
            maximum=100,
            length=300
        )
        self.progress_bar.pack(fill='x')
        
        # Detailed status labels
        self.details_frame = ttk.Frame(self.window)
        self.details_frame.pack(fill='x', padx=20, pady=10)
        
        # Row count status
        self.row_label = tk.Label(self.details_frame, text="Processed: 0 / 0 rows")
        self.row_label.pack(side='left')
        
        # Time remaining
        self.time_label = tk.Label(self.details_frame, text="Time remaining: calculating...")
        self.time_label.pack(side='right')
        
        self.window.update()
    
    def update(self, current_row, rows_selected):
        # Calculate progress percentage
        progress = (current_row / (self.total_rows - 1)) * 100
        self.progress_var.set(progress)
        
        # Calculate time remaining
        elapsed_time = time.time() - self.start_time
        if current_row > 0:
            rows_per_second = current_row / elapsed_time
            remaining_rows = self.total_rows - current_row
            remaining_time = remaining_rows / rows_per_second if rows_per_second > 0 else 0
            
            # Format time remaining
            if remaining_time < 60:
                time_str = f"{remaining_time:.1f} seconds"
            elif remaining_time < 3600:
                time_str = f"{remaining_time/60:.1f} minutes"
            else:
                time_str = f"{remaining_time/3600:.1f} hours"
        else:
            time_str = "calculating..."
        
        # Update labels
        self.status_label.config(
            text=f"Processing... {progress:.1f}% complete\n"
            f"Selected {rows_selected} rows so far"
        )
        self.row_label.config(text=f"Processed: {current_row:,} / {self.total_rows-1:,} rows")
        self.time_label.config(text=f"Time remaining: {time_str}")
        
        # Update the window
        self.window.update()
    
    def destroy(self):
        self.window.destroy()

def create_sample_csv():
    """
    Creates a sample CSV file with randomly selected rows using a chunked approach,
    balancing memory usage and speed.
    """
    root = tk.Tk()
    root.withdraw()

    # Get input file path from user
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )

    if not file_path:  # User canceled
        return

    # Get total number of rows in the CSV
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Get the header row
            total_rows = sum(1 for row in reader) + 1  # +1 to include the header
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read CSV file: {e}")
        return
    
    # Get desired sample size from user
    while True:
        try:
            sample_size = simpledialog.askinteger("Input", f"Enter the desired sample size (max {total_rows}):")
            if sample_size is None:  # User canceled
                return
            if sample_size > 0:
                break
            else:
                messagebox.showerror("Error", "Sample size must be a positive integer.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a positive integer.")

    # Determine the actual sample size (cannot exceed the total number of rows)
    actual_sample_size = min(sample_size, total_rows)

    # Construct output file path with actual sample size in the name
    filename, ext = os.path.splitext(os.path.basename(file_path))
    output_file_path = os.path.join(
        os.path.dirname(file_path), f"{filename}_sample_{actual_sample_size}{ext}"
    )

    try:
        chunk_size = ask_chunk_size()
        if chunk_size is None:  # User canceled
            return
        
        # Generate random indices for the entire file
        selected_indices = set(random.sample(range(total_rows - 1), actual_sample_size - 1))
        
        with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            # Write header
            header = next(reader)
            writer.writerow(header)
            
            # Process file in chunks
            chunk = []
            current_index = 0
            rows_selected = 0
            
            # Create progress window
            progress = ProgressWindow(root, total_rows)
            
            while True:
                chunk = []
                for _ in range(chunk_size):
                    try:
                        row = next(reader)
                        if current_index in selected_indices:
                            chunk.append(row)
                            rows_selected += 1
                        current_index += 1
                        # Update progress every 1000 rows to avoid excessive updates
                        if current_index % 1000 == 0:
                            progress.update(current_index, rows_selected)
                    except StopIteration:
                        break
                
                if chunk:
                    writer.writerows(chunk)
                
                if len(chunk) < chunk_size:
                    # Final progress update
                    progress.update(current_index, rows_selected)
                    break
            
            progress.destroy()
        
        messagebox.showinfo("Success", f"Random sample CSV file created at {output_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to create CSV file: {e}")

if __name__ == "__main__":
    create_sample_csv()