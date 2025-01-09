import tkinter as tk
from csv_toolkit import CSVToolkit
from tools.preferences_dialog import ToolPreferencesDialog
from pathlib import Path

class CSVToolkitApp(CSVToolkit):
    def __init__(self):
        super().__init__()
        
        # Load preferences
        self.preferences = ToolPreferencesDialog.load_preferences()
        
        # Show preferences dialog on first run
        if self.preferences is None:
            self.show_preferences_dialog()
        
        # Apply preferences to tool visibility
        self.apply_tool_preferences()
        
        # Add preferences to menu
        self.add_preferences_menu()
    
    def show_preferences_dialog(self):
        """Show tool preferences dialog"""
        dialog = ToolPreferencesDialog(self, self.categories, self.preferences)
        self.wait_window(dialog.dialog)
        
        if dialog.result is not None:
            self.preferences = dialog.result
            ToolPreferencesDialog.save_preferences(self.preferences)
            self.apply_tool_preferences()
    
    def apply_tool_preferences(self):
        """Apply tool visibility preferences"""
        if not self.preferences:
            return
            
        for tool_name, info in self.tool_buttons.items():
            button = info['button'].master  # Get the tool frame
            if self.preferences.get(tool_name, True):
                button.grid()  # Show tool
            else:
                button.grid_remove()  # Hide tool
    
    def add_preferences_menu(self):
        """Add preferences to menu"""
        # Add preferences to Tools menu
        tools_menu = self.menubar.winfo_children()[1]  # Get Tools menu
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Tool Preferences",
            command=self.show_preferences_dialog,
            accelerator="Ctrl+,"
        )
        
        # Add keyboard shortcut
        self.bind_all("<Control-comma>", lambda e: self.show_preferences_dialog())

def main():
    app = CSVToolkitApp()
    app.mainloop()

if __name__ == "__main__":
    main() 