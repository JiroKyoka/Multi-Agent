from abc import ABC, abstractmethod

class BaseTool(ABC):

    def __init__(self, name:str, description:str, parameters:dict):
        self.name = name
        self.description = description
        self.parameters = parameters

    @abstractmethod
    def run(self, **kwargs):
        pass