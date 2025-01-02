import tkinter as tk

class ToolTip:
    """Creates tooltips for widgets"""
    
    def __init__(self, widget_parent):
        self.widget_parent = widget_parent
        self.tip_window = None
    
    def bind_widget(self, widget, text):
        """Binds tooltip to a widget"""
        widget.bind('<Enter>', lambda e: self.show_tip(text))
        widget.bind('<Leave>', lambda e: self.hide_tip())
    
    def show_tip(self, text):
        """Shows tooltip"""
        if self.tip_window:
            return
            
        # Get position
        x, y, _, _ = self.widget_parent.bbox("insert")
        x = x + self.widget_parent.winfo_rootx() + 25
        y = y + self.widget_parent.winfo_rooty() + 25
        
        # Create tooltip window
        self.tip_window = tw = tk.Toplevel(self.widget_parent)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            tw, text=text, justify=tk.LEFT,
            background="#ffffe0", relief=tk.SOLID, borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)
    
    def hide_tip(self):
        """Hides tooltip"""
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy() 