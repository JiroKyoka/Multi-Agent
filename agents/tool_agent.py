import json

from agents.base_agent import BaseAgent
from models.llm import ChatLLM
from core.schema import tool_schema
from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry
from core.state import AgentState
from core.message import Message

class ToolAgent(BaseAgent):

    def __init__(
        self,
        name="tool_agent",
        tool_registry:ToolRegistry=None,
        tool_executor:ToolExecutor=None,
        description="负责需要调用工具完成的任务，例如数学计算、函数调用和外部工具执行"
    ):
        super().__init__(name, description)
        self.llm = ChatLLM()
        self.tool_registry = tool_registry
        self.tool_executor = tool_executor

    def run(self, state:AgentState):

        current_task = state["current_task"]
        if current_task is None:
            description = state["task"]
            if not description and state["messages"]:
                description = state["messages"][-1].content

            current_task = {
                "name": state["task"] or "tool_task",
                "description": description
            }
            state["current_task"] = current_task

        schemas = []

        if self.tool_registry is None:
            raise ValueError("ToolAgent requires a tool_registry")
        if self.tool_executor is None:
            raise ValueError("ToolAgent requires a tool_executor")

        for tool in self.tool_registry.list_tools():
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

        if not response.tool_calls:
            result = response.content or "没有选择可执行工具"
            state["result"] = result
            state["task_results"].append(
                {
                    "task": current_task["name"],
                    "agent": self.name,
                    "result": result
                }
            )
            state["messages"].append(
                Message(
                    role="assistant",
                    content=result
                )
            )
            return state

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
        state["result"] = result

        state["task_results"].append(
            {
                "task": current_task["name"],
                "agent": self.name,
                "result": result
            }
        )
        state["messages"].append(
            Message(
                role="assistant",
                content=result
            )
        )

        return state
