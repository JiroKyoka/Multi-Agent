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

    def list_names(self):
        return list(self.agents.keys())

    def list_agents(self):
        return self.agents.values()

    def list_specs(self):
        return [
            {
                "name": agent.name,
                "description": agent.description
            }
            for agent in self.agents.values()
        ]
    
