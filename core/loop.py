from agents.lead_agent import LeadAgent
from core.state import AgentState

class AgentLoop:

    def __init__(self, lead_agent: LeadAgent, max_steps=1):
        self.lead_agent = lead_agent
        self.max_steps = max_steps

    def run(self, state: AgentState):
        for _ in range(self.max_steps):
            state = self.lead_agent.run(state)
            break

        return state
