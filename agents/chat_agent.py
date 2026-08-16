from core.state import AgentState
from agents.base_agent import BaseAgent
from models.llm import ChatLLM
from core.message import Message
from prompts.base import SYSTEM_PROMPT
from core.schema import tool_schema
import json

class ChatAgent(BaseAgent):

    def __init__(self, name="chat_agent", tool_registry=None, tool_executor=None):
        super().__init__(name)
        self.llm = ChatLLM()
        self.tool_registry = tool_registry
        self.tool_executor = tool_executor

    def run(self, state:AgentState):

        messages = [
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT
            }
        ]

        schemas = []

        if self.tool_registry:
            tools = self.tool_registry.list_tools()

            for tool in tools:
                schemas.append(tool_schema(tool)) # 工具结构标准化，名字 描述 参数

        for msg in state["messages"]:
            messages.append(self.to_openai_message(msg))

        response = self.llm.invoke(messages, schemas)

        if response.tool_calls: # 一般只会返回工具调用或者content
            messages.append(response)

            for tool_call in response.tool_calls:
                function_call = tool_call.function
                arguments = json.loads(function_call.arguments)

                result = self.tool_executor.execute(function_call.name, arguments)
                messages.append(
                    {
                        "role" : "tool",
                        "tool_call_id" : tool_call.id,
                        "content" : result
                    }
                )

            final_response = self.llm.invoke(messages, schemas)
            state["result"] = final_response.content
            state["messages"].append(
                Message(
                    role="assistant",
                    content=final_response.content
                )
            )

        else:
            state["result"] = response.content
            state["messages"].append(
                Message(
                    role="assistant",
                    content=response.content
                )
            )

        return state

    def to_openai_message(self, msg):
        if isinstance(msg, dict):
            return msg

        return {
            "role" : msg.role,
            "content" : msg.content
        }
