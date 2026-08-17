from agents.chat_agent import ChatAgent
from agents.tool_agent import ToolAgent
from core.registry import AgentRegistry

def init_sub_agent(tool_registry=None, tool_executor=None):
    agent_registry = AgentRegistry()

    agent_registry.register(
        ChatAgent(
            "chat_agent",
            "负责普通问答、解释、总结和不需要工具的文本任务"
        )
    )

    agent_registry.register(
        ToolAgent(
            "tool_agent",
            tool_registry,
            tool_executor,
            "负责需要调用工具完成的任务，例如数学计算、函数调用和外部工具执行"
        )
    )

    return agent_registry
