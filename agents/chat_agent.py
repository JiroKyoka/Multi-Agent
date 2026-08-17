from core.state import AgentState
from agents.base_agent import BaseAgent
from models.llm import ChatLLM
from core.message import Message
from prompts.base import SYSTEM_PROMPT
from core.schema import tool_schema
import json

class ChatAgent(BaseAgent):

    def __init__(self, name="chat_agent", description="负责普通问答、解释、总结和不需要工具的文本任务"):
        super().__init__(name, description)
        self.llm = ChatLLM()

    def run(self, state:AgentState):

        messages = [
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT
            }
        ]

        for msg in state["messages"]:
            messages.append(self.to_openai_message(msg))

        response = self.llm.invoke(messages)


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
