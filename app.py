import tkinter as tk
from tkinter import ttk, messagebox
from csv_toolkit import CSVToolkit
from tools.preferences_dialog import ToolPreferencesDialog

class CSVToolkitApp(CSVToolkit):
    def __init__(self):
        super().__init__()
        
        # Load preferences
        self.preferences = ToolPreferencesDialog.load_preferences()
        if self.preferences is None:
            self.show_preferences_dialog()
            
        # Create menu
        self.create_menu()
        
        # Apply preferences
        self.apply_preferences()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Preferences", command=self.show_preferences_dialog, accelerator="Ctrl+,")
        
        # Bind keyboard shortcut
        self.root.bind("<Control-,>", lambda e: self.show_preferences_dialog())
        
    def show_preferences_dialog(self):
        dialog = ToolPreferencesDialog(self.root, self.categories, self.preferences)
        self.root.wait_window(dialog)
        if dialog.result:
            self.preferences = dialog.result
            self.apply_preferences()
            
    def apply_preferences(self):
        if not self.preferences:
            return
            
        # Show/hide tools based on preferences
        for category in self.categories.values():
            for tool_name in category["tools"]:
                visible = self.preferences.get(tool_name, True)
                if tool_name in self.tool_buttons:
                    if visible:
                        self.tool_buttons[tool_name].grid()
                        self.tool_labels[tool_name].grid()
                    else:
                        self.tool_buttons[tool_name].grid_remove()
                        self.tool_labels[tool_name].grid_remove()
                        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CSVToolkitApp()
    app.run() 