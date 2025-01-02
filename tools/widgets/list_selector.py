import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional

class ListSelector(ttk.LabelFrame):
    """Enhanced widget for selecting items from a list"""
    
    def __init__(self, parent, title="Select Items", multiple=False, grouping=False):
        super().__init__(parent, text=title)
        
        self.multiple = multiple
        self.grouping = grouping
        self.all_items = []  # Store all items for filtering
        self.groups = {}  # Store group information
        
        # Add search frame
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self._filter_items)
        
        ttk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            placeholder="Search items..."  # Requires themed tk
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            self.search_frame,
            text="×",
            width=3,
            command=self._clear_search
        ).pack(side=tk.RIGHT, padx=(2, 0))
        
        # Create listbox with scrollbar
        self.list_frame = ttk.Frame(self)
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.listbox = tk.Listbox(
            self.list_frame,
            selectmode='multiple' if multiple else 'single',
            exportselection=False
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Enable drag and drop
        self.listbox.bind('<Button-1>', self._on_click)
        self.listbox.bind('<B1-Motion>', self._on_drag)
        self.listbox.bind('<ButtonRelease-1>', self._on_drop)
        
        scrollbar = ttk.Scrollbar(
            self.list_frame,
            orient="vertical",
            command=self.listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Control buttons frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        if multiple:
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
        
        if grouping:
            ttk.Button(
                self.button_frame,
                text="Group",
                command=self._create_group
            ).pack(side=tk.RIGHT, padx=2)
            
            self.group_var = tk.StringVar(value="All")
            group_menu = ttk.OptionMenu(
                self.button_frame,
                self.group_var,
                "All",
                "All",
                command=self._on_group_changed
            )
            group_menu.pack(side=tk.RIGHT, padx=2)
        
        # Store drag state
        self.drag_data = {'item': None, 'index': None}
    
    def set_items(self, items: list, groups: Optional[Dict[str, List[str]]] = None):
        """Sets the list of available items with optional grouping"""
        self.all_items = items.copy()
        self.listbox.delete(0, tk.END)
        
        if groups:
            self.groups = groups
            if hasattr(self, 'group_var'):
                menu = self.button_frame.winfo_children()[-1]
                menu['menu'].delete(0, tk.END)
                menu['menu'].add_command(
                    label="All",
                    command=lambda: self.group_var.set("All")
                )
                for group in groups.keys():
                    menu['menu'].add_command(
                        label=group,
                        command=lambda g=group: self.group_var.set(g)
                    )
        
        self._update_display()
    
    def _update_display(self):
        """Updates the displayed items based on current filter and group"""
        self.listbox.delete(0, tk.END)
        items = self._get_filtered_items()
        
        if self.grouping and self.group_var.get() != "All":
            items = self.groups.get(self.group_var.get(), [])
        
        for item in items:
            self.listbox.insert(tk.END, item)
    
    def _filter_items(self, *args):
        """Filters items based on search text"""
        self._update_display()
    
    def _get_filtered_items(self) -> List[str]:
        """Gets items matching the current filter"""
        search_text = self.search_var.get().lower()
        if not search_text:
            return self.all_items
        return [item for item in self.all_items if search_text in item.lower()]
    
    def _clear_search(self):
        """Clears the search filter"""
        self.search_var.set("")
    
    def _on_click(self, event):
        """Handles start of drag operation"""
        if not self.multiple:  # Only allow drag in multiple selection mode
            return
            
        index = self.listbox.nearest(event.y)
        if index >= 0:
            self.drag_data['item'] = self.listbox.get(index)
            self.drag_data['index'] = index
    
    def _on_drag(self, event):
        """Handles drag operation"""
        if not self.drag_data['item']:
            return
            
        # Get the current mouse position relative to listbox
        new_index = self.listbox.nearest(event.y)
        if new_index >= 0 and new_index != self.drag_data['index']:
            # Move item to new position
            self.listbox.delete(self.drag_data['index'])
            self.listbox.insert(new_index, self.drag_data['item'])
            self.drag_data['index'] = new_index
    
    def _on_drop(self, event):
        """Handles end of drag operation"""
        self.drag_data = {'item': None, 'index': None}
    
    def _create_group(self):
        """Creates a new group from selected items"""
        if not self.grouping:
            return
            
        selected = self.get_selected()
        if not selected:
            return
            
        # Create dialog for group name
        dialog = tk.Toplevel(self)
        dialog.title("Create Group")
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Group Name:").pack(padx=5, pady=5)
        
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(padx=5, pady=5)
        
        def save_group():
            name = name_var.get()
            if name and name not in self.groups:
                self.groups[name] = selected
                menu = self.button_frame.winfo_children()[-1]
                menu['menu'].add_command(
                    label=name,
                    command=lambda: self.group_var.set(name)
                )
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_group).pack(pady=5)
    
    def _on_group_changed(self, group: str):
        """Handles group selection change"""
        self._update_display()
    
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