from core.runtime import AgentRuntime
from agents.chat_agent import ChatAgent
from core.message import Message
from core.state import AgentState
from core.graph import StateGraph
from agents.lead_agent import LeadAgent
from agents.planner_agent import PlannerAgent
from tools.calculator import CalculatorTool
from core.tool_registry import ToolRegistry
from core.tool_executor import ToolExecutor
from rag.init_retriever import init_rag
from tools.need_rag import RAGTool

tool_registry = ToolRegistry()



tool_registry.register(
    CalculatorTool()
)

retriever = init_rag("paper.txt")

tool_registry.register(
    RAGTool(retriever)
)

tool_executor = ToolExecutor(tool_registry)

chat_agent = ChatAgent(
    "chat_agent",
    tool_registry,
    tool_executor
)
planner_agent = PlannerAgent()
lead_agent = LeadAgent(planner_agent)

graph = StateGraph()

graph.add_node("chat", chat_agent.run)
#graph.add_node("lead", lead_agent.run)

graph.add_edge("start", "chat")
graph.add_edge("chat", "end")

executor = graph.compile()

runtime = AgentRuntime(executor)

state = AgentState(
    task="",
    messages=[
        Message(
            role="user",
            content="计算100+30"
        )
    ],
    result="",
    plan=None
)

runtime.startup()

state = runtime.run(state)

#print(state["messages"][-1].content)
print(state["messages"])

runtime.shutdown()
