from typing import Dict, Type, List
from ..base.tool_frame import BaseToolFrame
from ..utils.tool_registry import ToolRegistry

class ToolManager:
    """Manages tool registration and creation"""
    
    def __init__(self):
        self.registry = ToolRegistry()
    
    def register_tool(self, tool_class: Type[BaseToolFrame], category: str):
        """Registers a tool"""
        dependencies = tool_class.get_dependencies()
        self.registry.register_tool(tool_class, category, dependencies)
    
    def create_tool(self, tool_name: str, parent) -> BaseToolFrame:
        """Creates a tool instance"""
        # Check dependencies
        deps_ok, error = self.registry.check_dependencies(tool_name)
        if not deps_ok:
            raise ValueError(error)
        
        # Find tool class
        tool_class = None
        for t in self.registry.get_tools():
            if t.get_tool_name() == tool_name:
                tool_class = t
                break
        
        if not tool_class:
            raise ValueError(f"Tool not found: {tool_name}")
        
        # Create instance
        return tool_class(parent)
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Gets tool categories"""
        categories = {}
        for category in self.registry.CATEGORIES:
            tools = self.registry.get_tools(category)
            categories[category] = [t.get_tool_name() for t in tools]
        return categories
    
    def get_tool_config(self, tool_name: str) -> dict:
        """Gets tool configuration"""
        return self.registry.get_tool_config(tool_name)
    
    def save_tool_config(self, tool_name: str, config: dict):
        """Saves tool configuration"""
        self.registry.save_tool_config(tool_name, config) 