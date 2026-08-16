from agents.base_agent import BaseAgent

class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, agent:BaseAgent):
        self.agents[
            agent.name
        ] = agent

    def get(self, name):
        return self.agents[name]
    