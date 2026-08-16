from typing import TypedDict, List
from core.message import Message
from core.task import TaskPlan

class AgentState(TypedDict):
    task : str
    messages : List[Message]
    result : str
    plan : TaskPlan