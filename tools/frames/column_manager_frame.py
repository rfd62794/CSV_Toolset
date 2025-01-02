import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.column_processor import ColumnProcessor

class ColumnManagerFrame(BaseToolFrame):
    """Tool for managing CSV columns"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Column Manager"
    
    def create_tool_specific_widgets(self):
        # Column list
        list_frame = ttk.LabelFrame(self, text="Columns")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Column listbox with scrollbar
        self.column_list = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            exportselection=False
        )
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.column_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.column_list.yview)
        
        self.column_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Operations frame
        ops_frame = ttk.Frame(self)
        ops_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Column operations
        ttk.Label(ops_frame, text="Operations").pack(anchor=tk.W)
        
        # Rename operation
        rename_frame = ttk.LabelFrame(ops_frame, text="Rename Column")
        rename_frame.pack(fill=tk.X, pady=5)
        
        self.new_name_var = tk.StringVar()
        ttk.Entry(
            rename_frame,
            textvariable=self.new_name_var
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            rename_frame,
            text="Rename",
            command=self.rename_column
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Reorder operations
        reorder_frame = ttk.LabelFrame(ops_frame, text="Reorder")
        reorder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            reorder_frame,
            text="Move Up",
            command=lambda: self.move_column(-1)
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            reorder_frame,
            text="Move Down",
            command=lambda: self.move_column(1)
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Remove operations
        remove_frame = ttk.LabelFrame(ops_frame, text="Remove")
        remove_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            remove_frame,
            text="Remove Selected",
            command=self.remove_columns
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Add operations
        add_frame = ttk.LabelFrame(ops_frame, text="Add Column")
        add_frame.pack(fill=tk.X, pady=5)
        
        self.new_col_name = tk.StringVar()
        ttk.Entry(
            add_frame,
            textvariable=self.new_col_name
        ).pack(fill=tk.X, padx=5, pady=2)
        
        self.col_type = tk.StringVar(value="empty")
        types = ["empty", "sequence", "constant", "calculated"]
        ttk.OptionMenu(
            add_frame,
            self.col_type,
            "empty",
            *types
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            add_frame,
            text="Add Column",
            command=self.add_column
        ).pack(fill=tk.X, padx=5, pady=2)
    
    def process_file(self):
        """Processes the selected file"""
        if not self.validate_input():
            return
            
        try:
            df = self.read_input_file()
            
            # Update column list
            self.column_list.delete(0, tk.END)
            for col in df.columns:
                self.column_list.insert(tk.END, col)
                
        except Exception as e:
            self.show_error(f"Error loading file: {str(e)}")
    
    def rename_column(self):
        """Renames selected column"""
        selection = self.column_list.curselection()
        if not selection:
            self.show_error("Please select a column to rename")
            return
            
        new_name = self.new_name_var.get().strip()
        if not new_name:
            self.show_error("Please enter a new column name")
            return
            
        try:
            processor = ColumnProcessor()
            df = self.read_input_file()
            
            old_name = self.column_list.get(selection[0])
            result, stats = processor.rename_column(df, old_name, new_name)
            
            self.write_output_file(result)
            self.show_success(f"Column renamed: {stats['old_name']} → {stats['new_name']}")
            
            # Update list
            self.column_list.delete(selection[0])
            self.column_list.insert(selection[0], new_name)
            
        except Exception as e:
            self.show_error(f"Error renaming column: {str(e)}")
    
    def move_column(self, direction: int):
        """Moves selected column up or down"""
        selection = self.column_list.curselection()
        if not selection:
            self.show_error("Please select a column to move")
            return
            
        try:
            processor = ColumnProcessor()
            df = self.read_input_file()
            
            col_name = self.column_list.get(selection[0])
            new_pos = max(0, min(len(df.columns) - 1, selection[0] + direction))
            
            result, stats = processor.reorder_columns(
                df,
                {col_name: new_pos}
            )
            
            self.write_output_file(result)
            self.show_success(f"Column moved: {col_name}")
            
            # Update list
            self.column_list.delete(selection[0])
            self.column_list.insert(new_pos, col_name)
            self.column_list.selection_set(new_pos)
            
        except Exception as e:
            self.show_error(f"Error moving column: {str(e)}") 