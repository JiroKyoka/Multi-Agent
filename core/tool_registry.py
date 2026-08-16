from tools.base import BaseTool

class ToolRegistry:

    def __init__(self):
        self.tools={}

    def register(self, tool:BaseTool):
        self.tools[tool.name] = tool

    def get(self, name:str):
        return self.tools[name]

    def list_tools(self):
        return self.tools.values()