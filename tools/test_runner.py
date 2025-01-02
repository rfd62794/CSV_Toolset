import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path
from typing import List, Optional
import pytest
import threading
import queue

class TestRunnerTool(tk.Toplevel):
    """GUI tool for running tests"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.title("CSV Toolkit Test Runner")
        self.geometry("800x600")
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        if parent:
            x = parent.winfo_x() + (parent.winfo_width() - 800) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 600) // 2
            self.geometry(f"+{x}+{y}")
        
        self.output_queue = queue.Queue()
        self.create_widgets()
        self.update_output()
    
    def create_widgets(self):
        """Creates the UI elements"""
        # Test selection frame
        select_frame = ttk.LabelFrame(self, text="Test Selection")
        select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Test categories
        self.category_vars = {}
        categories_frame = ttk.Frame(select_frame)
        categories_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for category in ['unit', 'integration', 'performance']:
            var = tk.BooleanVar(value=True)
            self.category_vars[category] = var
            cb = ttk.Checkbutton(
                categories_frame,
                text=category.title(),
                variable=var
            )
            cb.pack(side=tk.LEFT, padx=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(self, text="Test Options")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Verbose output
        self.verbose_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Verbose Output",
            variable=self.verbose_var
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Stop on first failure
        self.fail_fast_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame,
            text="Stop on First Failure",
            variable=self.fail_fast_var
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Output frame
        output_frame = ttk.LabelFrame(self, text="Test Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Output text
        self.output_text = tk.Text(output_frame, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text['yscrollcommand'] = scrollbar.set
        
        # Control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Run button
        self.run_btn = ttk.Button(
            control_frame,
            text="Run Tests",
            command=self.run_tests
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        ttk.Button(
            control_frame,
            text="Clear Output",
            command=lambda: self.output_text.delete('1.0', tk.END)
        ).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.IntVar()
        self.progress = ttk.Progressbar(
            control_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Add close button
        ttk.Button(
            control_frame,
            text="Close",
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def run_tests(self):
        """Runs the selected tests"""
        self.run_btn['state'] = 'disabled'
        self.progress_var.set(0)
        self.output_text.delete('1.0', tk.END)
        
        # Build test arguments
        args = []
        if self.verbose_var.get():
            args.append('-v')
        if self.fail_fast_var.get():
            args.append('-x')
        
        # Add selected categories
        test_types = [cat for cat, var in self.category_vars.items() if var.get()]
        if test_types:
            markers = ' or '.join(test_types)
            args.extend(['-m', markers])
        
        # Run tests in separate thread
        thread = threading.Thread(
            target=self._run_tests_thread,
            args=(args,)
        )
        thread.start()
    
    def _run_tests_thread(self, args: List[str]):
        """Runs tests in separate thread"""
        try:
            # Add tests directory to path
            tests_dir = Path(__file__).parent.parent / 'tests'
            args.append(str(tests_dir))
            
            # Run tests
            result = pytest.main(args)
            
            # Update UI
            self.output_queue.put(('result', result))
            
        except Exception as e:
            self.output_queue.put(('error', str(e)))
        
        finally:
            self.output_queue.put(('done', None))
    
    def update_output(self):
        """Updates the output text from queue"""
        try:
            while True:
                msg_type, msg = self.output_queue.get_nowait()
                
                if msg_type == 'result':
                    self.show_result(msg)
                elif msg_type == 'error':
                    self.show_error(msg)
                elif msg_type == 'done':
                    self.run_btn['state'] = 'normal'
                    self.progress_var.set(100)
                
        except queue.Empty:
            pass
        
        finally:
            self.after(100, self.update_output)
    
    def show_result(self, result: int):
        """Shows test result"""
        if result == 0:
            messagebox.showinfo("Success", "All tests passed!")
        else:
            messagebox.showerror("Failed", f"Some tests failed (exit code: {result})")
    
    def show_error(self, error: str):
        """Shows error message"""
        messagebox.showerror("Error", f"Error running tests: {error}")

if __name__ == '__main__':
    app = TestRunnerTool()
    app.mainloop() 