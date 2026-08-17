from agents.base_agent import BaseAgent
from agents.planner_agent import PlannerAgent
from core.registry import AgentRegistry

class LeadAgent(BaseAgent):

    def __init__(self, planner:PlannerAgent, agent_registry:AgentRegistry):
        super().__init__("lead_agent")

        self.planner = planner
        self.agent_registry = agent_registry

    def run(self, state):
        state = self.planner.run(state)

        for task in state["plan"].tasks:
            state["current_task"] = {
                "name": task.name,
                "agent": task.agent,
                "description": task.description
            }

            agent = self.agent_registry.get(task.agent)
            state = agent.run(state)

        state["current_task"] = None

        return state
