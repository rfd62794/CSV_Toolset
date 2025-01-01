import tkinter as tk
from tkinter import ttk

class ListSelector(ttk.Frame):
    """Reusable list selection widget with scrollbar"""
    
    def __init__(self, master, title="Select Items", select_mode=tk.MULTIPLE):
        super().__init__(master)
        
        if title:
            ttk.Label(self, text=title).pack(anchor=tk.W, padx=5, pady=(5,0))
        
        # Create listbox with scrollbar
        self.listbox = tk.Listbox(
            self,
            selectmode=select_mode,
            exportselection=False
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
    
    def set_items(self, items):
        """Updates listbox items"""
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
    
    def get_selected(self):
        """Returns list of selected items"""
        return [self.listbox.get(i) for i in self.listbox.curselection()]
    
    def get_selected_indices(self):
        """Returns list of selected indices"""
        return self.listbox.curselection() 