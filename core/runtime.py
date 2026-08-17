from agents.base_agent import BaseAgent
from core.state import AgentState, ensure_state_defaults
from core.graph import GraphExecutor

class AgentRuntime:

    def __init__(self, graph:GraphExecutor=None):
        self.agent:dict[str, BaseAgent] = {}
        self.graph:GraphExecutor = graph

    #def register_agent(self, agent:BaseAgent):  链式时使用的方法，固定流程
    #    self.agent[agent.name] = agent

    def startup(self):
        for agent in self.agent.values():
            agent.initialize()

    def run(self, state:AgentState):
        state = ensure_state_defaults(state)

        return self.graph.invoke(state)

    def shutdown(self):
        for agent in self.agent.values():
            agent.shutdown()
