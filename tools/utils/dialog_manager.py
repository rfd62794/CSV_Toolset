import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, List, Tuple

class DialogManager:
    """Manages common dialog operations"""
    
    @staticmethod
    def show_error(message: str, title: str = "Error"):
        """Shows error dialog"""
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_warning(message: str, title: str = "Warning"):
        """Shows warning dialog"""
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_info(message: str, title: str = "Information"):
        """Shows info dialog"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def ask_yes_no(message: str, title: str = "Question") -> bool:
        """Shows yes/no dialog"""
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def get_file_path(title: str = "Select File",
                     filetypes: List[Tuple[str, str]] = None) -> Optional[str]:
        """Shows file selection dialog"""
        if filetypes is None:
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        return filedialog.askopenfilename(title=title, filetypes=filetypes)
    
    @staticmethod
    def get_save_path(title: str = "Save As",
                     filetypes: List[Tuple[str, str]] = None,
                     defaultextension: str = ".csv") -> Optional[str]:
        """Shows save file dialog"""
        if filetypes is None:
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        return filedialog.asksaveasfilename(
            title=title,
            filetypes=filetypes,
            defaultextension=defaultextension
        ) 