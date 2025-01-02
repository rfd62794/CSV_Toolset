import tkinter as tk
from tkinter import ttk

class ListSelector(ttk.LabelFrame):
    """Widget for selecting items from a list"""
    
    def __init__(self, parent, title="Select Items", multiple=False):
        super().__init__(parent, text=title)
        
        self.multiple = multiple
        
        # Create listbox with scrollbar
        self.list_frame = ttk.Frame(self)
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.listbox = tk.Listbox(
            self.list_frame,
            selectmode='multiple' if multiple else 'single',
            exportselection=False
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(
            self.list_frame,
            orient="vertical",
            command=self.listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Add select all/none buttons if multiple selection is enabled
        if multiple:
            self.button_frame = ttk.Frame(self)
            self.button_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(
                self.button_frame,
                text="Select All",
                command=self.select_all
            ).pack(side=tk.LEFT, padx=2)
            
            ttk.Button(
                self.button_frame,
                text="Select None",
                command=self.select_none
            ).pack(side=tk.LEFT, padx=2)
    
    def set_items(self, items: list):
        """Sets the list of available items"""
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
    
    def get_selected(self) -> list:
        """Gets selected items"""
        return [self.listbox.get(i) for i in self.listbox.curselection()]
    
    def select_all(self):
        """Selects all items"""
        self.listbox.select_set(0, tk.END)
    
    def select_none(self):
        """Clears selection"""
        self.listbox.selection_clear(0, tk.END)
    
    def set_selected(self, items: list):
        """Sets which items are selected"""
        self.select_none()
        for i in range(self.listbox.size()):
            if self.listbox.get(i) in items:
                self.listbox.selection_set(i) 