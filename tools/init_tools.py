from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry
from tools.calculator import CalculatorTool

def init_tools():
    tool_registry = ToolRegistry()

    tool_registry.register(
        CalculatorTool()
    )

    # 再此处添加工具

    tool_executor = ToolExecutor(tool_registry)

    return tool_registry, tool_executor
