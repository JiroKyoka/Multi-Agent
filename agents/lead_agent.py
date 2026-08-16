from agents.base_agent import BaseAgent
from agents.planner_agent import PlannerAgent

class LeadAgent(BaseAgent):

    def __init__(self, planner:PlannerAgent):
        super().__init__("lead_agent")

        self.planner = planner

    def run(self, state):
        return self.planner.run(state)