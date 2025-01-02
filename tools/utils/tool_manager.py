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
        tool_class = self.registry.get_tool_class(tool_name)
        if not tool_class:
            raise ValueError(f"Tool not found: {tool_name}")
        
        # Create instance
        return tool_class(parent)
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Gets tool categories and their tools"""
        categories = {}
        for category in self.registry.CATEGORIES:
            tools = self.registry.get_tools(category)
            tool_names = [t.get_tool_name() for t in tools]
            if tool_names:  # Only include categories with tools
                categories[category] = tool_names
        return categories
    
    def get_category_description(self, category: str) -> str:
        """Gets category description"""
        return self.registry.CATEGORIES.get(category, "")
    
    def get_tool_config(self, tool_name: str) -> dict:
        """Gets tool configuration"""
        return self.registry.get_tool_config(tool_name)
    
    def save_tool_config(self, tool_name: str, config: dict):
        """Saves tool configuration"""
        self.registry.save_tool_config(tool_name, config) 