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
        
        # Split operation
        split_frame = ttk.LabelFrame(ops_frame, text="Split Column")
        split_frame.pack(fill=tk.X, pady=5)
        
        self.split_separator = tk.StringVar()
        ttk.Entry(
            split_frame,
            textvariable=self.split_separator,
            placeholder="Separator (optional)"
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            split_frame,
            text="Split Column",
            command=self.split_column
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Merge operation
        merge_frame = ttk.LabelFrame(ops_frame, text="Merge Columns")
        merge_frame.pack(fill=tk.X, pady=5)
        
        self.merge_separator = tk.StringVar()
        ttk.Entry(
            merge_frame,
            textvariable=self.merge_separator,
            placeholder="Separator"
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            merge_frame,
            text="Merge Selected",
            command=self.merge_columns
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Type conversion
        type_frame = ttk.LabelFrame(ops_frame, text="Convert Type")
        type_frame.pack(fill=tk.X, pady=5)
        
        self.new_type = tk.StringVar(value="string")
        types = ["string", "numeric", "datetime", "category", "boolean"]
        ttk.OptionMenu(
            type_frame,
            self.new_type,
            "string",
            *types
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            type_frame,
            text="Convert Type",
            command=self.convert_type
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
    
    def split_column(self):
        """Splits selected column"""
        selection = self.column_list.curselection()
        if not selection:
            self.show_error("Please select a column to split")
            return
            
        try:
            processor = ColumnProcessor()
            df = self.read_input_file()
            
            column = self.column_list.get(selection[0])
            separator = self.split_separator.get() or None
            
            result, stats = processor.split_column(df, column, separator)
            
            self.write_output_file(result)
            self.show_success(f"Column split: {stats['original_column']} → {', '.join(stats['new_columns'])}")
            
            # Update column list
            self.process_file()
            
        except Exception as e:
            self.show_error(f"Error splitting column: {str(e)}")
    
    def merge_columns(self):
        """Merges selected columns"""
        selection = self.column_list.curselection()
        if len(selection) < 2:
            self.show_error("Please select at least two columns to merge")
            return
            
        try:
            processor = ColumnProcessor()
            df = self.read_input_file()
            
            columns = [self.column_list.get(idx) for idx in selection]
            new_name = f"merged_{'_'.join(columns)}"[:63]  # Limit length
            separator = self.merge_separator.get()
            
            result, stats = processor.merge_columns(df, columns, new_name, separator)
            
            self.write_output_file(result)
            self.show_success(f"Columns merged: {', '.join(stats['merged_columns'])} → {stats['new_column']}")
            
            # Update column list
            self.process_file()
            
        except Exception as e:
            self.show_error(f"Error merging columns: {str(e)}")
    
    def convert_type(self):
        """Converts column type"""
        selection = self.column_list.curselection()
        if not selection:
            self.show_error("Please select a column to convert")
            return
            
        try:
            processor = ColumnProcessor()
            df = self.read_input_file()
            
            column = self.column_list.get(selection[0])
            new_type = self.new_type.get()
            
            result, stats = processor.convert_type(df, column, new_type)
            
            self.write_output_file(result)
            self.show_success(
                f"Column type converted: {stats['column']} "
                f"({stats['original_type']} → {stats['new_type']})"
            )
            
        except Exception as e:
            self.show_error(f"Error converting type: {str(e)}") 