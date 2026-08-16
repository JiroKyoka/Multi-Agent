from core.tool_registry import ToolRegistry

class ToolExecutor:

    def __init__(self, registry:ToolRegistry):
        self.registry = registry

    def execute(self, name:str, arguments:dict):
        tool = self.registry.get(name)

        return tool.run(**arguments)