from abc import ABC, abstractmethod
from core.state import AgentState

class BaseAgent(ABC):

    def __init__(self, name:str, llm=None, tools=None, memory=None):
        self.name = name
        self.llm = llm
        self.tools = tools
        self.memory = memory

    @abstractmethod
    def run(self, state:AgentState):
        pass

    def initialize(self):
        pass

    def shutdown(self):
        pass