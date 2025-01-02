import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable
import pandas as pd

class TypePreviewDialog(tk.Toplevel):
    """Dialog for previewing and selecting column types"""
    
    def __init__(self, parent, df: pd.DataFrame, detected_types: Dict[str, str]):
        super().__init__(parent)
        self.title("Column Type Preview")
        self.df = df
        self.detected_types = detected_types
        self.selected_types = detected_types.copy()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
        # Center dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create preview tree
        self.tree = ttk.Treeview(
            main_frame,
            columns=('Column', 'Detected', 'Selected', 'Sample'),
            show='headings'
        )
        
        # Set column headings
        self.tree.heading('Column', text='Column')
        self.tree.heading('Detected', text='Detected Type')
        self.tree.heading('Selected', text='Selected Type')
        self.tree.heading('Sample', text='Sample Values')
        
        # Set column widths
        self.tree.column('Column', width=150)
        self.tree.column('Detected', width=100)
        self.tree.column('Selected', width=100)
        self.tree.column('Sample', width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add type selection on double click
        self.tree.bind('<Double-1>', self._on_double_click)
        
        # Add buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            button_frame,
            text="Apply",
            command=self._on_apply
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side=tk.RIGHT)
        
        # Populate tree
        self._populate_tree()
    
    def _populate_tree(self):
        """Populates the preview tree"""
        for col in self.df.columns:
            sample_values = ', '.join(str(x) for x in self.df[col].dropna().head(3))
            self.tree.insert('', tk.END, values=(
                col,
                self.detected_types[col],
                self.selected_types[col],
                sample_values
            ))
    
    def _on_double_click(self, event):
        """Handles double click on a column"""
        item = self.tree.selection()[0]
        col = self.tree.item(item)['values'][0]
        
        # Create type selection dialog
        dialog = TypeSelectionDialog(
            self,
            col,
            self.selected_types[col],
            self._on_type_selected
        )
    
    def _on_type_selected(self, column: str, type_: str):
        """Handles type selection"""
        self.selected_types[column] = type_
        # Update tree display
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == column:
                values = list(self.tree.item(item)['values'])
                values[2] = type_
                self.tree.item(item, values=values)
    
    def _on_apply(self):
        """Handles apply button click"""
        self.result = self.selected_types
        self.destroy()

class TypeSelectionDialog(tk.Toplevel):
    """Dialog for selecting a column type"""
    
    TYPES = ['string', 'integer', 'float', 'datetime', 'boolean']
    
    def __init__(self, parent, column: str, current_type: str, callback: Callable):
        super().__init__(parent)
        self.title(f"Select Type for {column}")
        self.column = column
        self.callback = callback
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Create widgets
        ttk.Label(
            self,
            text=f"Select type for column: {column}"
        ).pack(padx=10, pady=5)
        
        self.type_var = tk.StringVar(value=current_type)
        
        for type_ in self.TYPES:
            ttk.Radiobutton(
                self,
                text=type_,
                value=type_,
                variable=self.type_var
            ).pack(padx=10, pady=2, anchor=tk.W)
        
        ttk.Button(
            self,
            text="OK",
            command=self._on_ok
        ).pack(pady=10)
        
        # Center dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def _on_ok(self):
        """Handles OK button click"""
        self.callback(self.column, self.type_var.get())
        self.destroy() 