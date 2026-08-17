import json

from agents.base_agent import BaseAgent
from models.llm import ChatLLM
from core.schema import tool_schema
from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry
from core.state import AgentState

class ToolAgent(BaseAgent):

    def __init__(self, name="tool_agent", tool_registry:ToolRegistry=None, tool_executor:ToolExecutor=None):
        super().__init__(name)
        self.llm = ChatLLM()
        self.tool_registry = tool_registry
        self.tool_executor = tool_executor

    def run(self, state:AgentState):

        current_task = state["current_task"]

        schemas = []

        for tool in self.tool_registry.tools.values():
            schemas.append(tool_schema(tool))

        messages = [
            {
                "role": "system",
                "content": "你是工具执行agent。当任务需要使用工具时，选择合适的工具。"
            },
            {
                "role": "user",
                "content": current_task["description"]
            }
        ]

        response = self.llm.invoke(messages, tools=schemas)

        tool_call = response.tool_calls[0]

        arguments = json.loads(tool_call.function.arguments)

        tool_result = self.tool_executor.execute(tool_call.function.name, arguments)

        messages.append(
                            {
                                "role" : "tool",
                                "tool_call_id" : tool_call.id,
                                "content" : tool_result
                            }
        )

        result = str(tool_result)

        state["task_results"].append(
            {
                "task": current_task["name"],
                "agent": self.name,
                "result": result
            }
        )

        return state