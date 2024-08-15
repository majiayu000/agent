from typing import Dict, Any, Callable


class Tool:
    def __init__(self, name: str, function: Callable):
        self.name = name
        self.function = function

    def execute(self, *args, **kwargs) -> Any:
        return self.function(*args, **kwargs)


class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register_tool(self, name: str, function: Callable) -> None:
        self.tools[name] = Tool(name, function)

    def get_tool(self, name: str) -> Tool:
        return self.tools.get(name)

    def get_all_tools(self) -> Dict[str, Tool]:
        return self.tools
