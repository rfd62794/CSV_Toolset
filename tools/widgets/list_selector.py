import tkinter as tk
from tkinter import ttk
from typing import List

class ListSelector(ttk.Frame):
    """Reusable list selection widget with scrollbar"""
    
    def __init__(self, master, title: str = None, select_mode=tk.MULTIPLE):
        super().__init__(master)
        
        if title:
            ttk.Label(self, text=title).pack(anchor=tk.W)
        
        # Create listbox with scrollbar
        self.listbox = tk.Listbox(
            self,
            selectmode=select_mode,
            exportselection=False
        )
        scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def set_items(self, items: List[str]):
        """Sets the items in the listbox"""
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
    
    def get_selected(self) -> List[str]:
        """Gets selected items"""
        return [self.listbox.get(i) for i in self.listbox.curselection()]
    
    def get_selected_indices(self):
        """Returns list of selected indices"""
        return self.listbox.curselection() 