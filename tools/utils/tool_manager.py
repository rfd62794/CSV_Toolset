from typing import Dict, Type
from ..base.tool_frame import BaseToolFrame

class ToolManager:
    """Manages tool registration and instantiation"""
    
    def __init__(self):
        self._tools: Dict[str, Type[BaseToolFrame]] = {}
        self._categories: Dict[str, list] = {}
    
    def register_tool(self, tool_class: Type[BaseToolFrame], category: str = "General"):
        """Registers a tool with optional category"""
        tool_name = tool_class.get_tool_name()
        self._tools[tool_name] = tool_class
        
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(tool_name)
    
    def get_tool_class(self, tool_name: str) -> Type[BaseToolFrame]:
        """Gets tool class by name"""
        return self._tools.get(tool_name)
    
    def get_categories(self) -> Dict[str, list]:
        """Gets all categories and their tools"""
        return self._categories
    
    def create_tool(self, tool_name: str, master) -> BaseToolFrame:
        """Creates instance of tool by name"""
        tool_class = self.get_tool_class(tool_name)
        if tool_class:
            return tool_class(master)
        raise ValueError(f"Tool not found: {tool_name}") 