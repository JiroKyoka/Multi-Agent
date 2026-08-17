from abc import ABC, abstractmethod
from core.state import AgentState

class BaseAgent(ABC):

    def __init__(self, name:str):
        self.name = name

    @abstractmethod
    def run(self, state:AgentState):
        pass

    def initialize(self):
        pass

    def shutdown(self):
        pass