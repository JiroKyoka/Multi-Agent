from typing import Callable, Any
from core.state import AgentState

class GraphExecutor:
    def __init__(self, nodes:dict, edges:dict, conditional_edges:dict):
        self.nodes = nodes
        self.edges = edges
        self.conditional_edges = conditional_edges

    def invoke(self, state:AgentState):
        current = "start"
        current = self.edges.get(current, "end")

        while current !="end":
            node = self.nodes[current]
            state = node.run(state)
            if current in self.conditional_edges:
                current =  self.conditional_edges[current](state)
            else:
                current = self.edges.get(current, "end")
            
        return state

class Node:
    def __init__(self, name:str, func:Callable[[AgentState], Any]):
        self.name = name
        self.func = func

    def run(self, state:AgentState):
        return self.func(state)

class StateGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.conditional_edges = {}

    def add_node(self, name:str, func:Callable[[AgentState], Any]):
        self.nodes[name] = Node(name, func)

    def add_edge(self, start:str, end:str):
        self.edges[start] = end

    def add_conditional_edge(self, start:str, router:Callable):
        self.conditional_edges[start] = router

    def compile(self):
        return GraphExecutor(
            self.nodes,
            self.edges,
            self.conditional_edges
        )
    