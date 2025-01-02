from typing import Dict, Type, List
from ..base.tool_frame import BaseToolFrame
from ..utils.tool_registry import ToolRegistry
import json
from pathlib import Path

class ToolManager:
    """Manages tool registration and creation"""
    
    def __init__(self):
        self.registry = ToolRegistry()
    
    def register_tool(self, tool_class: Type[BaseToolFrame], category: str):
        """Registers a tool"""
        try:
            dependencies = tool_class.get_dependencies()
        except AttributeError:
            # If get_dependencies not implemented, assume no dependencies
            dependencies = []
        
        self.registry.register_tool(tool_class, category, dependencies)
    
    def create_tool(self, tool_name: str, parent) -> BaseToolFrame:
        """Creates a tool instance with better error handling"""
        try:
            # Check if tool exists
            tool_class = self.registry.get_tool_class(tool_name)
            if not tool_class:
                raise ValueError(f"Tool not found: {tool_name}")
            
            # Check dependencies
            deps_ok, error = self.registry.check_dependencies(tool_name)
            if not deps_ok:
                raise ValueError(error)
            
            # Create instance
            tool = tool_class(parent)
            
            # Load saved configuration
            config = self.get_tool_config(tool_name)
            if hasattr(tool, 'config_panel'):
                tool.config_panel.set_config(config)
            
            return tool
            
        except Exception as e:
            raise RuntimeError(f"Error creating tool {tool_name}: {str(e)}")
    
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
        try:
            config_file = Path("config") / f"{tool_name.lower().replace(' ', '_')}.json"
            if config_file.exists():
                with open(config_file) as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load configuration for {tool_name}: {e}")
        return {}
    
    def save_tool_config(self, tool_name: str, config: dict):
        """Saves tool configuration"""
        try:
            # Create config directory if it doesn't exist
            config_dir = Path("config")
            config_dir.mkdir(exist_ok=True)
            
            # Save config to JSON file
            config_file = config_dir / f"{tool_name.lower().replace(' ', '_')}.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
                
        except Exception as e:
            print(f"Warning: Could not save configuration for {tool_name}: {e}") 