from typing import Dict, List
import pandas as pd
import numpy as np
from .data_types import DataTypeDetector

class DataCleaner:
    """Utility class for suggesting data cleaning operations"""
    
    @classmethod
    def analyze_data(cls, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Analyzes data and returns cleaning suggestions"""
        suggestions = {}
        
        for col in df.columns:
            col_suggestions = []
            
            # Check for missing values
            missing = df[col].isna().sum()
            if missing > 0:
                col_suggestions.append(
                    f"Contains {missing} missing values. Consider:"
                    "\n- Removing rows with missing values"
                    "\n- Filling with mean/median (numeric)"
                    "\n- Filling with mode (categorical)"
                )
            
            # Check for whitespace
            if df[col].dtype == 'object':
                whitespace = (df[col].astype(str).str.strip() != df[col]).sum()
                if whitespace > 0:
                    col_suggestions.append(
                        f"Contains {whitespace} values with extra whitespace. Consider:"
                        "\n- Trimming whitespace"
                    )
            
            # Check for duplicates
            duplicates = df[col].duplicated().sum()
            if duplicates > 0:
                col_suggestions.append(
                    f"Contains {duplicates} duplicate values. Consider:"
                    "\n- Removing duplicate rows"
                    "\n- Checking for data entry errors"
                )
            
            # Check for case consistency
            if df[col].dtype == 'object':
                unique_values = df[col].dropna().unique()
                case_variations = {}
                for val in unique_values:
                    lower_val = str(val).lower()
                    if lower_val in case_variations:
                        case_variations[lower_val].append(val)
                    else:
                        case_variations[lower_val] = [val]
                
                inconsistent = [k for k, v in case_variations.items() if len(v) > 1]
                if inconsistent:
                    col_suggestions.append(
                        f"Contains inconsistent case in {len(inconsistent)} values. Consider:"
                        "\n- Standardizing case (upper/lower/title)"
                    )
            
            # Add suggestions if any found
            if col_suggestions:
                suggestions[col] = col_suggestions
        
        return suggestions

    @classmethod
    def show_suggestions(cls, parent, df: pd.DataFrame):
        """Shows cleaning suggestions in a dialog"""
        suggestions = cls.analyze_data(df)
        
        dialog = tk.Toplevel(parent)
        dialog.title("Data Cleaning Suggestions")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Create main frame
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget
        text = tk.Text(main_frame, wrap=tk.WORD, width=60, height=20)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=text.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.configure(yscrollcommand=scrollbar.set)
        
        # Add suggestions
        if suggestions:
            for col, col_suggestions in suggestions.items():
                text.insert(tk.END, f"\nColumn: {col}\n", "heading")
                for suggestion in col_suggestions:
                    text.insert(tk.END, f"- {suggestion}\n")
        else:
            text.insert(tk.END, "No cleaning suggestions found.")
        
        # Add close button
        ttk.Button(
            dialog,
            text="Close",
            command=dialog.destroy
        ).pack(pady=10)
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}') 