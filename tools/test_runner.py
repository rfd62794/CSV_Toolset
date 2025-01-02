import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pathlib import Path

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

class TestRunnerTool:
    """Tool for running test suite"""
    
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        
        if not PYTEST_AVAILABLE:
            messagebox.showwarning(
                "Dependencies Missing",
                "pytest is not installed. Please install it to run tests:\n\n"
                "pip install pytest"
            )
            return
            
        self.create_window()
    
    def create_window(self):
        """Creates test runner window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Test Runner")
        self.window.geometry("400x300")
        
        # Create test selection frame
        select_frame = ttk.LabelFrame(self.window, text="Test Selection")
        select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add test category checkboxes
        self.categories = {
            "Analysis": tk.BooleanVar(value=True),
            "Data Cleaning": tk.BooleanVar(value=True),
            "Data Manipulation": tk.BooleanVar(value=True),
            "Data Formatting": tk.BooleanVar(value=True)
        }
        
        for category, var in self.categories.items():
            ttk.Checkbutton(
                select_frame,
                text=category,
                variable=var
            ).pack(anchor=tk.W, padx=5, pady=2)
        
        # Add run button
        ttk.Button(
            self.window,
            text="Run Tests",
            command=self.run_tests
        ).pack(pady=10)
        
        # Add results display
        results_frame = ttk.LabelFrame(self.window, text="Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(results_frame, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def run_tests(self):
        """Runs selected tests"""
        if not PYTEST_AVAILABLE:
            return
            
        # Get selected categories
        selected = [cat for cat, var in self.categories.items() if var.get()]
        
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select at least one test category"
            )
            return
        
        try:
            # Clear results
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert(tk.END, "Running tests...\n\n")
            self.window.update()
            
            # Run tests
            test_path = Path(__file__).parent / 'tests'
            result = pytest.main(['-v', str(test_path)])
            
            # Process results
            success = result == 0
            timestamp = datetime.now().isoformat()
            
            if self.callback:
                self.callback({
                    'timestamp': timestamp,
                    'success': success,
                    'categories': selected
                })
            
            # Show results
            result_text = "✓ All tests passed!" if success else "❌ Some tests failed"
            self.results_text.insert(tk.END, f"\n{result_text}")
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error running tests: {str(e)}"
            ) 