from core.runtime import AgentRuntime
from core.message import Message
from core.state import AgentState
from core.graph import StateGraph
from agents.lead_agent import LeadAgent
from agents.planner_agent import PlannerAgent
from agents.init_sub_agent import init_sub_agent
from tools.init_tools import init_tools

tool_registry, tool_executor = init_tools()
agent_registry = init_sub_agent(tool_registry, tool_executor)

planner_agent = PlannerAgent(
    agent_specs=agent_registry.list_specs()
)
lead_agent = LeadAgent(planner_agent, agent_registry)

graph = StateGraph()

graph.add_node("lead", lead_agent.run)

graph.add_edge("start", "lead")
graph.add_edge("lead", "end")

executor = graph.compile()

runtime = AgentRuntime(executor)

user_task = "计算100+30"

state = AgentState(
    task=user_task,
    messages=[
        Message(
            role="user",
            content=user_task
        )
    ],
    result="",
    plan=None,
    current_task=None,
    task_results=[]
)

runtime.startup()

state = runtime.run(state)

#print(state["messages"][-1].content)
print(state["messages"])

runtime.shutdown()
